import hashlib
import json
import multiprocessing as mp
import os
import pathlib
import sys
import urllib
from argparse import ArgumentParser

from tqdm import tqdm

# Add "../.." to path to import utils
sys.path.insert(0, os.path.abspath(os.path.join(os.path.pardir, os.path.pardir)))

from utils import process_wikipedia

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-t", "--test", dest="test", help="run in test mode", action="store_true")
    parser.add_argument("-p","--path", dest="path", help="path to resources directory", action="store", type=str, default="./resources/")

    args = parser.parse_args()

    resources_dir = args.path

    # this is where we have stored the output of the WikiExtractor
    if args.test:
        path = os.path.join(resources_dir,"wikipedia/test-extractedResources/")
        processed_docs = os.path.join(resources_dir,"wikipedia/test-processedWiki/")

    else:
        path = os.path.join(resources_dir,"wikipedia/extractedResources/")
        processed_docs = os.path.join(resources_dir,"wikipedia/processedWiki/")

    if pathlib.Path(processed_docs).is_dir() == False:
        print("Error! You need a processed dump in " + processed_docs)
        exit()

    # we setup these folders for acquiring the output of this script
    pathlib.Path(path + "Pages/").mkdir(parents=True, exist_ok=True)
    pathlib.Path(path + "Store-Counts/").mkdir(parents=True, exist_ok=True)

    # the number of cpus
    N = mp.cpu_count()

    # this is just to doublecheck in case we have duplicate hashed files (it shouldn't happen)
    out = open(path + "hashed_duplicates.csv", "w")

    # a Wikipedia dump is divided in subparts, which the WikiExtractor maps to different folders
    folders = list(os.listdir(processed_docs))

    for i in tqdm(range(len(folders))):
        folder = folders[i]
        # we set up multiple processes to go through all files in each folder
        with mp.Pool(processes=N) as p:
            paths = [
                processed_docs + folder + "/" + filename
                for filename in os.listdir(processed_docs + folder)
            ]
            pages = p.map(process_wikipedia.process_doc, paths)

        pages = [page for group in pages for page in group]

        # separating frequency counts from aspects
        freq_counts = [x[0][:-1] for x in pages]
        pages_with_sections = [x[0][-1] for x in pages]

        # saving pages with sections
        for page_with_sect in pages_with_sections:
            # hashing the title and checking if too long or containing /

            # we % encode the title, so it's consistent with the entities formats in the stored json files
            try:
                percent_encoded_title = urllib.parse.quote(page_with_sect["title"])

                if "/" in percent_encoded_title or len(percent_encoded_title) > 200:
                    percent_encoded_title = hashlib.sha224(
                        percent_encoded_title.encode("utf-8")
                    ).hexdigest()
                    # just checking if there are multiple titles with the same hash (it should not happen)
                    if percent_encoded_title + ".json" in set(os.listdir(path + "Pages/")):
                        out.write(page_with_sect["title"] + "," + percent_encoded_title + "\n")
                        continue

                sections = page_with_sect["sections"]

                # saving the page with sections
                with open(path + "Pages/" + percent_encoded_title + ".json", "w") as fp:
                    json.dump(sections, fp)
            
            except KeyError:
                continue

        # storing counts, still divided in folders
        with open(path + "Store-Counts/" + str(i) + ".json", "w") as fp:
            json.dump(freq_counts, fp)

    out.close()
