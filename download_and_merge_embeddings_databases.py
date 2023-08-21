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
from argparse import ArgumentParser
import os

# Check if entity embeddings exist otherwise download them:

parser = ArgumentParser()
parser.add_argument("-p","--path", dest="path", help="path to resources directory", action="store", type=str, default="./resources/")

args = parser.parse_args()

resources_dir = args.path

if not os.path.exists(os.path.join(resources_dir,"rel_db/")):
    os.makedirs(os.path.join(resources_dir,"rel_db/"))

if not os.path.exists(os.path.join(resources_dir,"rel_db/wiki_2019/")):
    wget.download(
        "http://gem.cs.ru.nl/wiki_2019.tar.gz",
        os.path.join(resources_dir,"rel_db/"),
    )
    tar = tarfile.open(os.path.join(resources_dir,"rel_db/wiki_2019.tar.gz"))
    tar.extractall(os.path.join(resources_dir,"rel_db/"))
    tar.close()

# Check if glove embeddings exist otherwise download them:
if not os.path.exists(os.path.join(resources_dir,"rel_db/generic/")):
    os.makedirs(os.path.join(resources_dir,"rel_db/generic/"))

if not os.path.isfile(os.path.join(resources_dir,"rel_db/generic/common_crawl.db")):
    if not os.path.isfile(os.path.join(resources_dir,"rel_db/generic/glove.840B.300d.zip")):
        print("Downloading Glove Embeddings")
        wget.download(
            "https://nlp.stanford.edu/data/glove.840B.300d.zip",
            os.path.join(resources_dir,"rel_db/generic/"),
        )

    with zipfile.ZipFile(os.path.join(resources_dir,"rel_db/generic/glove.840B.300d.zip"), "r") as zip_file:
        # Get the name of the file inside the zip
        file_name = zip_file.namelist()[0]

        # Open the file inside the zip as a file object
        with io.TextIOWrapper(zip_file.open(file_name), encoding="utf8") as f:
            # Read the contents of the file into a dictionary
            embeddings = {
                "#SND/UNK#": np.asarray(
                    [
                        0.22418612241744995,
                        -0.2888180911540985,
                        0.13854354619979858,
                        0.003653974272310734,
                        -0.12870769202709198,
                        0.1024395003914833,
                        0.06162703037261963,
                        0.07317768782377243,
                        -0.06135387346148491,
                        -1.3476412296295166,
                        0.42038747668266296,
                        -0.06359579414129257,
                        -0.09683354943990707,
                        0.1808628886938095,
                        0.2370443195104599,
                        0.014126831665635109,
                        0.17009729146957397,
                        -1.149170160293579,
                        0.31498587131500244,
                        0.06622260808944702,
                        0.024688012897968292,
                        0.07669486105442047,
                        0.13851656019687653,
                        0.021301891654729843,
                        -0.06640639156103134,
                        -0.010336552746593952,
                        0.13523174822330475,
                        -0.0421435683965683,
                        -0.11938712745904922,
                        0.006949146743863821,
                        0.13333013653755188,
                        -0.18276233971118927,
                        0.05238557234406471,
                        0.008943230845034122,
                        -0.2395719736814499,
                        0.08500347286462784,
                        -0.006894187536090612,
                        0.0015865416498854756,
                        0.0633913055062294,
                        0.19177646934986115,
                        -0.1311332881450653,
                        -0.11295504868030548,
                        -0.14277435839176178,
                        0.03413935378193855,
                        -0.03428007662296295,
                        -0.05136607587337494,
                        0.18891511857509613,
                        -0.16673366725444794,
                        -0.05778509005904198,
                        0.036822736263275146,
                        0.08078762888908386,
                        0.022949082776904106,
                        0.03329665586352348,
                        0.011783703230321407,
                        0.05643303319811821,
                        -0.04277614504098892,
                        0.011959478259086609,
                        0.011552747339010239,
                        -0.0007970817969180644,
                        0.11300002783536911,
                        -0.031369760632514954,
                        -0.006155883427709341,
                        -0.009043721482157707,
                        -0.4153434932231903,
                        -0.1887020468711853,
                        0.13708816468715668,
                        0.005911772605031729,
                        -0.11303292959928513,
                        -0.030095556750893593,
                        -0.23909100890159607,
                        -0.05353950336575508,
                        -0.04490499943494797,
                        -0.20228320360183716,
                        0.006564571056514978,
                        -0.09579148888587952,
                        -0.07392080128192902,
                        -0.06487638503313065,
                        0.11173760890960693,
                        -0.04864859580993652,
                        -0.1656530350446701,
                        -0.05203676596283913,
                        -0.07896754145622253,
                        0.13685138523578644,
                        0.0757531225681305,
                        -0.006275638472288847,
                        0.286933034658432,
                        0.5201796293258667,
                        -0.08771556615829468,
                        -0.33010920882225037,
                        -0.13596132397651672,
                        0.11489495635032654,
                        -0.09744380414485931,
                        0.06269526481628418,
                        0.1211867481470108,
                        -0.08026119321584702,
                        0.35256704688072205,
                        -0.06001658737659454,
                        -0.04889918491244316,
                        -0.06828877329826355,
                        0.08874208480119705,
                        0.003964409697800875,
                        -0.0766303762793541,
                        0.12639199197292328,
                        0.0780944675207138,
                        -0.02316400036215782,
                        -0.5680661797523499,
                        -0.03789238631725311,
                        -0.1350950300693512,
                        -0.1135164275765419,
                        -0.11143247038125992,
                        -0.09050163626670837,
                        0.25173333287239075,
                        -0.1484188735485077,
                        0.03463583439588547,
                        -0.07334565371274948,
                        0.06319950520992279,
                        -0.03834318369626999,
                        -0.05413348227739334,
                        0.04219760000705719,
                        -0.09038133174180984,
                        -0.07052794098854065,
                        -0.009173871017992496,
                        0.009069793857634068,
                        0.14051611721515656,
                        0.029582079499959946,
                        -0.03643162176012993,
                        -0.08625560998916626,
                        0.04295022785663605,
                        0.08230835944414139,
                        0.09032970666885376,
                        -0.122795470058918,
                        -0.013900339603424072,
                        0.048119861632585526,
                        0.08678435534238815,
                        -0.14450816810131073,
                        -0.04425004497170448,
                        0.01831969991326332,
                        0.015026411041617393,
                        -0.10052651166915894,
                        0.060212425887584686,
                        0.7405944466590881,
                        -0.0016332970699295402,
                        -0.2496059536933899,
                        -0.023738248273730278,
                        0.01639590971171856,
                        0.11928761750459671,
                        0.13950896263122559,
                        -0.03162425383925438,
                        -0.016450410708785057,
                        0.14079703390598297,
                        -0.0002825950796250254,
                        -0.08052641898393631,
                        -0.0021309524308890104,
                        -0.02535022608935833,
                        0.08693722635507584,
                        0.14308641850948334,
                        0.17146047949790955,
                        -0.13943040370941162,
                        0.04879305139183998,
                        0.09275061637163162,
                        -0.053168028593063354,
                        0.031103068962693214,
                        0.012354841455817223,
                        0.2105841487646103,
                        0.326180636882782,
                        0.18016134202480316,
                        -0.1588113009929657,
                        0.1532336324453354,
                        -0.2255963385105133,
                        -0.04200682416558266,
                        0.008469111286103725,
                        0.038156796246767044,
                        0.1518801897764206,
                        0.13274385035037994,
                        0.11375755816698074,
                        -0.09527557343244553,
                        -0.04948951676487923,
                        -0.10266021639108658,
                        -0.2706456780433655,
                        -0.034566428512334824,
                        -0.018810611218214035,
                        -0.0010361404856666923,
                        0.1034015417098999,
                        0.13883134722709656,
                        0.21130722761154175,
                        -0.019809940829873085,
                        0.1833365559577942,
                        -0.1075163409113884,
                        -0.031288985162973404,
                        0.025182928889989853,
                        0.23233027756214142,
                        0.04205196723341942,
                        0.11731827259063721,
                        -0.1550654172897339,
                        0.006358014885336161,
                        -0.1542990356683731,
                        0.15116986632347107,
                        0.1274585872888565,
                        0.2576863467693329,
                        -0.2548536956310272,
                        -0.07094422727823257,
                        0.1798371523618698,
                        0.054028209298849106,
                        -0.09884487092494965,
                        -0.24594978988170624,
                        -0.09302578866481781,
                        -0.0282035730779171,
                        0.09439938515424728,
                        0.09234027564525604,
                        0.029291663318872452,
                        0.13110609352588654,
                        0.15683098137378693,
                        -0.016919273883104324,
                        0.2392807900905609,
                        -0.13432978093624115,
                        -0.22422641515731812,
                        0.14635199308395386,
                        -0.06499607861042023,
                        0.47036460041999817,
                        -0.02718997374176979,
                        0.06224842369556427,
                        -0.091361865401268,
                        0.2148997038602829,
                        -0.1956244260072708,
                        -0.10032516717910767,
                        -0.09057068079710007,
                        -0.06203768402338028,
                        -0.18876813352108002,
                        -0.10963419079780579,
                        -0.2773522734642029,
                        0.12616299092769623,
                        -0.022179925814270973,
                        -0.16058781743049622,
                        -0.08047454059123993,
                        0.02695314772427082,
                        0.11073178797960281,
                        0.014894072897732258,
                        0.09416890144348145,
                        0.14300113916397095,
                        -0.15940159559249878,
                        -0.06608017534017563,
                        -0.00799551047384739,
                        -0.11668665707111359,
                        -0.13081924617290497,
                        -0.09237651526927948,
                        0.14741156995296478,
                        0.09180161356925964,
                        0.08173615485429764,
                        0.3211158215999603,
                        -0.003655310021713376,
                        -0.047031477093696594,
                        -0.0231179092079401,
                        0.04896119236946106,
                        0.08670001477003098,
                        -0.06766346096992493,
                        -0.5002856850624084,
                        -0.048514630645513535,
                        0.14144542813301086,
                        -0.032995156943798065,
                        -0.11954562366008759,
                        -0.14929790794849396,
                        -0.23883464932441711,
                        -0.01988416351377964,
                        -0.15917156636714935,
                        -0.05208408087491989,
                        0.28009915351867676,
                        -0.002912110649049282,
                        -0.05458146706223488,
                        -0.4738474488258362,
                        0.17112277448177338,
                        -0.12066954374313354,
                        -0.04217442497611046,
                        0.13953189551830292,
                        0.26114872097969055,
                        0.012869438156485558,
                        0.009291584603488445,
                        -0.0026459486689418554,
                        -0.07533072680234909,
                        0.01784074306488037,
                        -0.268696129322052,
                        -0.2181970775127411,
                        -0.17085029184818268,
                        -0.1022816002368927,
                        -0.05528995394706726,
                        0.1351441740989685,
                        0.12362551689147949,
                        -0.10980717837810516,
                        0.13980041444301605,
                        -0.20233899354934692,
                        0.08813502639532089,
                        0.3849637806415558,
                        -0.10653764754533768,
                        -0.061995673924684525,
                        0.028849434107542038,
                        0.032302480190992355,
                        0.02385602705180645,
                        0.06994965672492981,
                        0.19310516119003296,
                        -0.07767657190561295,
                        -0.14481587707996368,
                    ],
                    dtype="float32",
                )
            }
            for line in f:
                values = line.split(" ")
                word = values[0]
                embedding = np.asarray(values[1:], dtype="float32")
                embeddings[word] = embedding

    # Set up a connection to SQLite
    conn = sqlite3.connect(os.path.join(resources_dir,"rel_db/generic/common_crawl.db"))
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
    os.path.join(resources_dir,"wikidata/wikidata_gazetteer.csv"),
    usecols=["wikidata_id"],
)

# Convert the gazetteer to a set of unique Wikidata IDs
gaz = set(gaz["wikidata_id"].to_list())


# Connect to the entity word embedding database
conn = sqlite3.connect(os.path.join(resources_dir,"rel_db/wiki_2019/generated/entity_word_embedding.db"))

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
path_to_db = os.path.join(resources_dir,"wikidata/index_enwiki-latest.db")
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
dest_conn = sqlite3.connect(os.path.join(resources_dir,"rel_db", "embeddings_database.db"))

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
dest_conn.execute(f"ATTACH DATABASE '{os.path.join(resources_dir,'/rel_db/generic/common_crawl.db')}' AS common_crawl;")
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
