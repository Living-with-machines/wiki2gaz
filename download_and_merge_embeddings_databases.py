import sqlite3
import pandas as pd
from utils import process_wikipedia
from multiprocessing import Pool
from functools import partial
import numpy as np
import os
import tarfile
import wget
import zipfile
import io

# Check if entity embeddings exist otherwise download them:

if not os.path.exists("resources/rel_db/"):
    os.makedirs("resources/rel_db/")

if not os.path.exists("resources/rel_db/wiki_2019/"):
    wget.download(
        "http://gem.cs.ru.nl/wiki_2019.tar.gz",
        "resources/rel_db/",
    )
    tar = tarfile.open("resources/rel_db/wiki_2019.tar.gz")
    tar.extractall("resources/rel_db/")
    tar.close()

# Check if glove embeddings exist otherwise download them:
if not os.path.exists("resources/rel_db/generic/"):
    os.makedirs("resources/rel_db/generic/")

if not os.path.isfile("resources/rel_db/generic/common_crawl.db"):
    if not os.path.isfile("resources/rel_db/generic/glove.840B.300d.zip"):
        print("Downloading Glove Embeddings")
        wget.download(
            "https://nlp.stanford.edu/data/glove.840B.300d.zip",
            "resources/rel_db/generic/",
        )

    with zipfile.ZipFile("resources/rel_db/generic/glove.840B.300d.zip", "r") as zip_file:
        # Get the name of the file inside the zip
        file_name = zip_file.namelist()[0]

        # Open the file inside the zip as a file object
        with io.TextIOWrapper(zip_file.open(file_name), encoding="utf8") as f:
            # Read the contents of the file into a dictionary
            embeddings = {}
            for line in f:
                values = line.split(" ")
                word = values[0]
                embedding = np.asarray(values[1:], dtype="float32")
                embeddings[word] = embedding

    # Set up a connection to SQLite
    conn = sqlite3.connect("resources/rel_db/generic/common_crawl.db")
    c = conn.cursor()

    # Create a table to store the embeddings
    c.execute(
        """CREATE TABLE embeddings
                (word text, emb text)"""
    )

    # Insert the embeddings into the table
    for word, embedding in embeddings.items():
        c.execute("INSERT INTO embeddings VALUES (?, ?)", (word, embedding.tostring()))

    # Add the index to the table
    c.execute("CREATE INDEX word_index ON embeddings (word)")

    # Commit the changes and close the connection
    conn.commit()
    conn.close()


# Load the gazetteer file
gaz = pd.read_csv(
    "resources/wikidata/extracted/wikidata_gazetteer.csv",
    usecols=["wikidata_id"],
)

# Convert the gazetteer to a set of unique Wikidata IDs
gaz = set(gaz["wikidata_id"].to_list())


# Connect to the entity word embedding database
conn = sqlite3.connect("resources/rel_db/wiki_2019/generated/entity_word_embedding.db")

# Execute a SELECT statement to retrieve all elements in a column
table_name = "embeddings"
column_name = "word"
sql_statement = f"SELECT {column_name} FROM {table_name}"
keys = conn.execute(sql_statement).fetchall()

keys = [key[0] for key in keys]

# Extract only the keys that start with "ENTITY/"
entities = [x for x in keys if x.startswith("ENTITY/")]


def process_entity(entity, path_to_db, gaz):
    """
    A function that processes an entity to find its corresponding Wikidata ID.

    Parameters:
    -----------
    entity: str
        The entity to be processed.
    path_to_db: str
        The path to the Wikipedia database.
    gaz: set
        A set of Wikidata IDs from the gazetteer.

    Returns:
    --------
    Tuple
        A tuple containing the original entity and its corresponding Wikidata ID,
        or None if the entity does not have a corresponding Wikidata ID in the gazetteer.
    """
    # Convert the entity to a Wikidata ID using the process_wikipedia module
    wikidata_entity = process_wikipedia.title_to_id(
        entity.replace("ENTITY/", ""), path_to_db=path_to_db
    )
    # Check if the Wikidata ID is in the gazetteer
    if wikidata_entity is not None and wikidata_entity in gaz:
        return entity, wikidata_entity


def parallel_process(entities, num_processes, path_to_db):
    """
    A function that processes a list of entities in parallel using multiple processes.

    Parameters:
    -----------
    entities: list
        A list of entities to be processed.
    num_processes: int
        The number of processes to use in parallel.
    path_to_db: str
        The path to the Wikipedia database.

    Returns:
    --------
    dict
        A dictionary containing the processed entities and their corresponding Wikidata IDs.
    """
    # Create a pool of processes
    pool = Pool(processes=num_processes)
    # Create a partial function that takes a single entity argument
    func = partial(process_entity, path_to_db=path_to_db, gaz=gaz)
    # Map the partial function to the list of entities using the pool of processes
    results = pool.map(func, entities)
    # Close the pool of processes
    pool.close()
    # Wait for the processes to complete
    pool.join()
    # Filter out the None values from the results and convert to a dictionary
    wikidata_entities = dict(filter(lambda x: x is not None, results))
    return wikidata_entities


# Set the path to the Wikipedia/Wikidata index database
path_to_db = "resources/wikidata/index_enwiki-latest.db"
# Set the number of processes to use in parallel
num_processes = 12

# Process the entities in parallel
wikidata_entities = parallel_process(entities, num_processes, path_to_db)

# Create a list of words (not entities) from the keys
words = [x for x in keys if not x.startswith("ENTITY/")]

# Combine the list of words with the list of wikidata entities to get all filtered keys
filtered_emb_keys = words + list(wikidata_entities.keys())

# Check if the embedding database file already exists, and if it does, delete it
if os.path.exists("embedding_database.db"):
    os.remove("embedding_database.db")

# Connect to the new embedding database
dest_conn = sqlite3.connect("resources/embeddings_database.db")

# Create a new table to store the embeddings
dest_conn.execute(
    """CREATE TABLE entity_embeddings
            (word text, emb text)"""
)

# Iterate through each embedding key and insert the corresponding embedding into the new database
for emb_key in filtered_emb_keys:
    # Retrieve the embedding for the current key from the source database
    result = conn.execute("SELECT emb FROM embeddings WHERE word=?", (emb_key,)).fetchone()

    # Convert the binary embedding to a numpy array
    embedding = np.frombuffer(result[0], dtype="float32")

    # If the embedding key is a wikidata entity, replace it with the corresponding wikidata ID
    if emb_key.startswith("ENTITY/"):
        emb_key = "ENTITY/" + wikidata_entities[emb_key]

    # Insert the word and embedding into the destination database
    dest_conn.execute(
        "INSERT INTO entity_embeddings VALUES (?, ?)", (emb_key, embedding.tobytes())
    )

# Add an index to the new table to speed up queries
dest_conn.execute("CREATE INDEX entity_index ON entity_embeddings (word)")

# Attach the common crawl database and create a new table to store its embeddings
dest_conn.execute("ATTACH DATABASE 'resources/rel_db/generic/common_crawl.db' AS common_crawl;")
dest_conn.execute(
    """CREATE TABLE glove_embeddings
             (word TEXT,
             emb TEXT);"""
)

# Insert the embeddings from the common crawl database into the new database
dest_conn.execute("INSERT INTO glove_embeddings (word, emb) SELECT * FROM common_crawl.embeddings")

# Add an index to the new table to speed up queries
dest_conn.execute("CREATE INDEX glove_index ON glove_embeddings (word)")

# Commit the changes to the new database and close the connections to both databases
dest_conn.commit()
dest_conn.close()
conn.close()
