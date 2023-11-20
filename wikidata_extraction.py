import bz2
import json
import pandas as pd
import pydash
from tqdm import tqdm
import os
import pathlib
import glob
import re
from argparse import ArgumentParser

"""
Credit: This script is partially based on this code: https://akbaritabar.netlify.app/how_to_use_a_wikidata_dump.
"""

parser = ArgumentParser()

parser.add_argument(
    "-t",
    dest="test",
    choices=("True", "False"),
    help="Run in test mode.",
    default="True",
)
parser.add_argument("-p","--path", dest="path", help="path to resources directory", action="store", type=str, default="./resources/")

args = parser.parse_args()

resources_dir = args.path
# ------------------------------------------
# Wikidata input dump file and output processed files:
input_path = os.path.join(resources_dir, "wikidata/")
output_path = os.path.join(resources_dir, "wikidata/extracted/")
wikimapper_path = os.path.join(resources_dir, "wikipedia/extractedResources/")

if args.test == "True":
    output_path = os.path.join(resources_dir, "wikidata/test-extracted/")
    print("Running in test mode, set -t to False to disable the test mode.")

pathlib.Path(output_path).mkdir(parents=True, exist_ok=True)


# Check whether necessary input files exist:
if not glob.glob(input_path + "*.json.bz2"):
    print("Error! You need a Wikidata dump in " + input_path)
    exit()
if not glob.glob(wikimapper_path + "/wikidata2wikipedia.json"):
    print("Error! You need the Wikidata to Wikipedia mapper in " + wikimapper_path)
    exit()


# Load wikidata2wikipedia mapper:
with open(wikimapper_path + "wikidata2wikipedia.json", "r") as f:
    wikidata2wikipedia = json.load(f)


# Disable chained assignments
pd.options.mode.chained_assignment = None

languages = [
    "en",
    "cy",
    "sco",
    "gd",
    "ga",
    "kw",  # Main languages native to Ireland and GB
    "de",
    "fr",
    "it",
    "es",
    "uk",
    "pl",
    "pt",
    "tr",
    "ro",
    "nl",
]  # Most spoken European languages in Latin alphabet


# ==========================================
# Convert date format to year (int)
# ==========================================
def parse_date(date_expl):
    # This function gets the year (string) from the Wikidata date format.
    regex_date = r"\+([0-9]{4})\-[0-9]{2}\-[0-9]{2}T.*"
    date_expl = "" if not date_expl else date_expl
    if re.match(regex_date, date_expl):
        date_expl = re.match(regex_date, date_expl).group(1)
    return date_expl


# ==========================================
# Process bz2 wikidata dump
# ==========================================
def wikidata(filename):
    with bz2.open(filename, mode="rt") as f:
        f.read(2)  # skip first two bytes: "{\n"
        for line in f:
            try:
                yield json.loads(line.rstrip(",\n"))
            except json.decoder.JSONDecodeError:
                continue


# ==========================================
# Parse wikidata entry
# ==========================================
def parse_record(record):
    # Wikidata ID:
    wikidata_id = record["id"]

    # ==========================================
    # Place description and definition
    # ==========================================

    # Main label:
    english_label = pydash.get(record, "labels.en.value")

    # Location is instance of
    instance_of_dict = pydash.get(record, "claims.P31")
    instance_of = None
    if instance_of_dict:
        instance_of = [
            pydash.get(r, "mainsnak.datavalue.value.id") for r in instance_of_dict
        ]

    # Aliases and labels:
    aliases = pydash.get(record, "aliases")
    labels = pydash.get(record, "labels")
    alias_dict = dict()
    for x in aliases:
        if x in languages or x.startswith("en-"):
            for y in aliases[x]:
                if "value" in y:
                    if (
                        not y["value"].isupper()
                        and not y["value"].islower()
                        and any(x.isalpha() for x in y["value"])
                    ):
                        if x in alias_dict:
                            if not y["value"] in alias_dict[x]:
                                alias_dict[x].append(y["value"])
                        else:
                            alias_dict[x] = [y["value"]]
    for x in labels:
        if x in languages or x.startswith("en-"):
            if "value" in labels[x]:
                if (
                    not labels[x]["value"].isupper()
                    and not labels[x]["value"].islower()
                    and any(z.isalpha() for z in labels[x]["value"])
                ):
                    if x in alias_dict:
                        if not labels[x]["value"] in alias_dict[x]:
                            alias_dict[x].append(labels[x]["value"])
                    else:
                        alias_dict[x] = [labels[x]["value"]]

    # Native label
    nativelabel_dict = pydash.get(record, "claims.P1705")
    nativelabel = None
    if nativelabel_dict:
        nativelabel = [
            pydash.get(c, "mainsnak.datavalue.value.text") for c in nativelabel_dict
        ]

    # ==========================================
    # Historical information
    # ==========================================

    # Historical counties
    hcounties_dict = pydash.get(record, "claims.P7959")
    hcounties = []
    if hcounties_dict:
        hcounties = [
            pydash.get(hc, "mainsnak.datavalue.value.id") for hc in hcounties_dict
        ]

    # Country: sovereign state of this item
    country_dict = pydash.get(record, "claims.P17")
    countries = dict()
    if country_dict:
        for r in country_dict:
            countryname = pydash.get(r, "mainsnak.datavalue.value.id")
            if countryname:
                entity_start_time = pydash.get(
                    r, "qualifiers.P580[0].datavalue.value.time"
                )
                entity_end_time = pydash.get(
                    r, "qualifiers.P582[0].datavalue.value.time"
                )
                entity_start_time = parse_date(entity_start_time)
                entity_end_time = parse_date(entity_end_time)
                countries[countryname] = (entity_start_time, entity_end_time)

    # ==========================================
    # Coordinates
    # ==========================================

    # Latitude and longitude:
    latitude = pydash.get(record, "claims.P625[0].mainsnak.datavalue.value.latitude")
    longitude = pydash.get(record, "claims.P625[0].mainsnak.datavalue.value.longitude")
    if latitude and longitude:
        latitude = round(latitude, 6)
        longitude = round(longitude, 6)

    # ==========================================
    # Store records in a dictionary
    # ==========================================
    dict_record = {
        "wikidata_id": wikidata_id,
        "english_label": english_label,
        "instance_of": instance_of,
        "alias_dict": alias_dict,
        "nativelabel": nativelabel,
        "hcounties": hcounties,
        "countries": countries,
        "latitude": latitude,
        "longitude": longitude,
    }

    df_record = pd.DataFrame.from_dict(dict_record, orient="index").T

    return df_record


# ==========================================
# Parse all WikiData
# ==========================================

path = output_path
pathlib.Path(path).mkdir(parents=True, exist_ok=True)

df_record_all = pd.DataFrame(
    columns=[
        "wikidata_id",
        "english_label",
        "instance_of",
        "alias_dict",
        "nativelabel",
        "hcounties",
        "countries",
        "latitude",
        "longitude",
    ]
)

header = True
i = 0
for record in tqdm(wikidata(input_path + "latest-all.json.bz2")):
    # Only extract items that have a wikipedia mapping:
    if record["id"] in wikidata2wikipedia:
        # Only extract items with geographical coordinates (P625)
        if pydash.has(record, "claims.P625"):
            # ==========================================
            # Store records in a csv
            # ==========================================
            df_record = parse_record(record)
            df_record_all = pd.concat([df_record_all, df_record], ignore_index=True)
            i += 1
            if i % 5000 == 0:
                pd.DataFrame.to_csv(
                    df_record_all,
                    path_or_buf=path + "/till_" + record["id"] + "_item.csv",
                )
                print("i = " + str(i) + " item " + record["id"] + "  Done!")
                print("CSV exported")
                df_record_all = pd.DataFrame(
                    columns=[
                        "wikidata_id",
                        "english_label",
                        "instance_of",
                        "alias_dict",
                        "nativelabel",
                        "hcounties",
                        "countries",
                        "latitude",
                        "longitude",
                    ]
                )

                # If we are in test mode, exit the loop after having created the first file:
                if args.test == "True":
                    break

            else:
                continue


pd.DataFrame.to_csv(
    df_record_all, path_or_buf=path + "final_csv_till_" + record["id"] + "_item.csv"
)
print("i = " + str(i) + " item " + record["id"] + "  Done!")
print("All items finished, final CSV exported!")
