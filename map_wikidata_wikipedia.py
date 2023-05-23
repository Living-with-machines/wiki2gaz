import json
import os
import pathlib
import sqlite3
import sys
from argparse import ArgumentParser

from tqdm import tqdm

# Add "../.." to path to import utils
sys.path.insert(0, os.path.abspath(os.path.join(os.path.pardir, os.path.pardir)))

from utils import process_wikipedia

# as usual, we can run it in test mode if the extracted folders are available
parser = ArgumentParser()
parser.add_argument(
    "-t", "--test", dest="test", help="run in test mode", action="store_true"
)

args = parser.parse_args()

if args.test:
    path = "resources/wikipedia/test-extractedResources/"

else:
    path = "resources/wikipedia/extractedResources/"

# https://github.com/jcklie/wikimapper#create-your-own-index
mapper = "resources/wikidata/index_enwiki-latest.db"

if pathlib.Path(path).is_dir() == False:
    print("Error! You need to have extracted entity and mention counts in " + path)
    exit()


# we take the list of available entities
with open(path + "overall_entity_freq.json", "r") as f:
    overall_entity_freq = json.load(f)


mapper = "resources/wikidata/index_enwiki-latest.db"

with sqlite3.connect(mapper) as conn:
    c = conn.cursor()
    c.execute("ALTER TABLE mapping ADD COLUMN lower_wikipedia_title")
    c.execute(
        "UPDATE or IGNORE mapping SET lower_wikipedia_title = lower(wikipedia_title)"
    )
    c.execute("DROP INDEX IF EXISTS idx_wikipedia_title")
    c.execute("CREATE INDEX idx_wikipedia_title ON mapping(wikipedia_title);")
    c.execute(
        "CREATE INDEX lower_idx_wikipedia_title ON mapping(lower_wikipedia_title);"
    )

wikidata2wikipedia = {}

wikipedia2wikidata = {}

for entity in tqdm(overall_entity_freq.keys()):
    # we also take the entity frequency in wikipedia in case of multiple wikipedia pages for a single wikidata id
    freq = overall_entity_freq[entity]
    prepare_entity = process_wikipedia.make_wikipedia2wikidata_consisent(entity)
    wikidata_id = process_wikipedia.title_to_id(
        prepare_entity, lower=True, path_to_db=mapper
    )

    # for each wikidata id we save a list of related wikipedia pages, with their frequency (they are probably multiple redicteds of the same entry)
    if wikidata_id:
        if wikidata_id not in wikidata2wikipedia:
            wikidata2wikipedia[wikidata_id] = [{"title": entity, "freq": freq}]
        else:
            wikidata2wikipedia[wikidata_id].append({"title": entity, "freq": freq})

        # and here we map the opposite, each wikipedia page to a single wikidata id
        wikipedia2wikidata[entity] = wikidata_id


with open(path + "wikidata2wikipedia.json", "w") as fp:
    json.dump(wikidata2wikipedia, fp)

with open(path + "wikipedia2wikidata.json", "w") as fp:
    json.dump(wikipedia2wikidata, fp)
