from collections import Counter
import json, urllib, hashlib
from operator import itemgetter
import glob
import pandas as pd
from pathlib import Path
from ast import literal_eval
from argparse import ArgumentParser
import os

parser = ArgumentParser()
parser.add_argument("-p","--path", dest="path", help="path to resources directory", action="store", type=str, default="./resources/")

args = parser.parse_args()

resources_dir = args.path

# ---------------
# 1. WIKIDATA GAZETTEER
# Concatenate the different Wikidta csv files into a unified csv if it does not exist yet.
# ---------------

# Load Wikidata resource:
print("Loading the wikidata gazetteer.")
wikidata_path = os.path.join(resources_dir, "wikidata/")
df = pd.DataFrame()
if not Path(wikidata_path + "wikidata_gazetteer.csv").exists():
    all_files = glob.glob(wikidata_path + "extracted/*.csv")

    li = []
    for filename in all_files:
        df_temp = pd.read_csv(filename, index_col=None, header=0)
        li.append(df_temp)

    df = pd.concat(li, axis=0, ignore_index=True)
    df = df.drop(columns=["Unnamed: 0"])

    df.to_csv(wikidata_path + "wikidata_gazetteer.csv", index=False)

else:
    df = pd.read_csv(wikidata_path + "wikidata_gazetteer.csv", low_memory=False)


# ---------------
# 2. ALTNAMES
# Collect altnames and mentions and link them to Wikidata locations.
# ---------------

if not Path(wikidata_path + "mentions_to_wikidata.json").exists():
    # ---------------
    # Load resources
    # ---------------

    # Load Wikipedia resources:
    wikipedia_path = os.path.join(resources_dir, "wikipedia/extractedResources/")

    print("Loading mention_overall_dict.")
    with open(wikipedia_path + "mention_overall_dict.json", "r") as f:
        mention_overall_dict = json.load(f)
        mention_overall_dict = {x: Counter(y) for x, y in mention_overall_dict.items()}

    print("Loading wikipedia2wikidata.")
    with open(wikipedia_path + "wikipedia2wikidata.json", "r") as f:
        wikipedia2wikidata = json.load(f)

    print("Loading wikidata2wikipedia.")
    with open(wikipedia_path + "wikidata2wikipedia.json", "r") as f:
        wikidata2wikipedia = json.load(f)

    # all_wikidata_keys is the set of all wikidata entries that have a
    # corresponding wikipedia entry:
    all_wikidata_keys = set(list(wikidata2wikipedia.keys()))

    # all_wikidata_locs is the set of all wikidata entries that have
    # a corresponding wikipedia entry and coordinates (i.e. all
    # wikidata entries in our wikidata df). all_wikidata_locs should
    # be a subset of all_wikidata_keys.
    all_wikidata_locs = set(list(df["wikidata_id"].unique()))

    # Collect altnames from the Wikidata dataframe (columns alias_dict,
    # english_label, and nativelabel). Create a dictionary where the
    # altname is the key and a counter of Wikidata entries potentially
    # referred to by this altname is the value:
    print("Collecting Wikidata altnames.")
    wikidata_altnames = dict()
    for i, row in df.iterrows():
        wk = row["wikidata_id"]
        try: 
            alias_dict = literal_eval(row["alias_dict"])
        except ValueError:
            continue
        
        for lang in alias_dict:
            for al in alias_dict[lang]:
                if al in wikidata_altnames:
                    wikidata_altnames[al].append(wk)
                else:
                    wikidata_altnames[al] = [wk]
        
        if row["english_label"] in wikidata_altnames:
            wikidata_altnames[row["english_label"]].append(wk)
        else:
            wikidata_altnames[row["english_label"]] = [wk]
        
        if type(row["nativelabel"]) == list:
            try:
                for nl in literal_eval(row["nativelabel"]):
                    if nl in wikidata_altnames:
                        wikidata_altnames[nl].append(wk)
                    else:
                        wikidata_altnames[nl] = [wk]
            except ValueError:
                continue

    wikidata_altnames_counter = dict()
    for aln in wikidata_altnames:
        wikidata_altnames_counter[aln] = Counter(wikidata_altnames[aln])

    # Collect altnames from the mention_overall_dict dictionary.

    # mentions_to_wikidata is a dictionary where the key is a
    # mention and the value is a Counter object with the wikidata
    # id as key and the count as value. The count is the number
    # times the WikidataId is referred to with a particular mention
    # (from the mention_overall_dict dictionary) plus the number
    # of times the WikidataId is assigned this particular mention
    # as an alternate name in the Wikidata df.
    print("Creating the mentions2wikidata dictionary.")
    mentions_to_wikidata = dict()
    for m in list(mention_overall_dict.keys()):
        for wk in mention_overall_dict[m]:
            if wk in wikipedia2wikidata:
                if wikipedia2wikidata[wk] in all_wikidata_locs:
                    if m in mentions_to_wikidata:
                        if wikipedia2wikidata[wk] in mentions_to_wikidata[m]:
                            mentions_to_wikidata[m][
                                wikipedia2wikidata[wk]
                            ] += mention_overall_dict[m][wk]
                        else:
                            mentions_to_wikidata[m][wikipedia2wikidata[wk]] = mention_overall_dict[
                                m
                            ][wk]
                    else:
                        mentions_to_wikidata[m] = {
                            wikipedia2wikidata[wk]: mention_overall_dict[m][wk]
                        }
    for m in mentions_to_wikidata:
        mentions_to_wikidata[m] = Counter(mentions_to_wikidata[m])
        if m in wikidata_altnames_counter:
            mentions_to_wikidata[m] += wikidata_altnames_counter[m]

    # wikidata_to_mentions is the reverse dictionary of mentions_to_wikidata:
    print("Creating the wikidata2mentions dictionary.")
    wikidata_to_mentions = dict()
    for m in mentions_to_wikidata:
        for wk in mentions_to_wikidata[m]:
            if wk in wikidata_to_mentions:
                wikidata_to_mentions[wk][m] = mentions_to_wikidata[m][wk]
            else:
                wikidata_to_mentions[wk] = {m: mentions_to_wikidata[m][wk]}

    # wikidata_to_mentions_normalized is the normalized version of
    # wikidata_to_mentions: each wikidata ID has one or more mentions
    # with a relative frequency that adds up to one, indicating the
    # probabilities of a certain wikidata ID to being referred by the
    # different possible mentions:
    print("Creating the normalized wikidata2mentions dictionary.")
    wikidata_to_mentions_normalized = dict()
    for wk in wikidata_to_mentions:
        factor = 1.0 / sum(wikidata_to_mentions[wk].values())
        wikidata_to_mentions_normalized[wk] = Counter(
            {key: value * factor for key, value in wikidata_to_mentions[wk].items()}
        )

    # mentions_to_wikidata_normalized is the normalized version of
    # mentions_to_wikidata. For a given mention, each Wikidata ID
    # is provided with the probability of it being referred to by
    # such mention (being referred to by this is not the same as
    # how likely a wikipedia ID is given a certain mention. I.e.
    # the probability of London in Kiribati (Q2477346) of being
    # referred to as "London" is 0.80, and that's the measure
    # we are interested in here; the probability of having the London
    # in Kiribati entry given the mention "London" would be close to 0,
    # because most "London" mentions refer to the city in England.):
    print("Creating the normalized mentions2wikidata dictionary.")
    mentions_to_wikidata_normalized = dict()
    for m in mentions_to_wikidata:
        for wk in mentions_to_wikidata[m]:
            if m in mentions_to_wikidata_normalized:
                mentions_to_wikidata_normalized[m][wk] = wikidata_to_mentions_normalized[wk][m]
            else:
                mentions_to_wikidata_normalized[m] = {wk: wikidata_to_mentions_normalized[wk][m]}

    print("Storing the dictionaries.")
    with open(wikidata_path + "mentions_to_wikidata_normalized.json", "w") as fp:
        json.dump(mentions_to_wikidata_normalized, fp)
    with open(wikidata_path + "wikidata_to_mentions_normalized.json", "w") as fp:
        json.dump(wikidata_to_mentions_normalized, fp)

    with open(wikidata_path + "mentions_to_wikidata.json", "w") as fp:
        json.dump(mentions_to_wikidata, fp)
    with open(wikidata_path + "wikidata_to_mentions.json", "w") as fp:
        json.dump(wikidata_to_mentions, fp)

# ---------------
# 3. RELEVANCE
# Create a dictionary of Wikidata entity relevance
# ---------------


if not Path(wikidata_path + "overall_entity_freq_wikidata.json").exists():
    print("Creating the wikidata overall frequency dictionary.")

    wikipedia_path = os.path.join(resources_dir, "wikipedia/extractedResources/")

    with open(wikipedia_path + "overall_entity_freq.json", "r") as f:
        overall_entity_freq = json.load(f)

    with open(wikipedia_path + "wikipedia2wikidata.json", "r") as f:
        wikipedia2wikidata = json.load(f)

    # Dictionary overall_entity_freq_wikidata:
    overall_entity_freq_wikidata = dict()
    for wk in wikipedia2wikidata:
        if wikipedia2wikidata[wk] in overall_entity_freq_wikidata:
            overall_entity_freq_wikidata[wikipedia2wikidata[wk]] += overall_entity_freq[wk]
        else:
            overall_entity_freq_wikidata[wikipedia2wikidata[wk]] = overall_entity_freq[wk]

    print("Storing the wikidata overall frequency dictionary.")
    with open(wikidata_path + "overall_entity_freq_wikidata.json", "w") as fp:
        json.dump(overall_entity_freq_wikidata, fp)
