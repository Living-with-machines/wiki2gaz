Getting started with Wiki2Gaz
=============================
Wiki2Gaz consists of seven scripts that need to be run in order.

.. toctree::
   :maxdepth: 1
   :caption: Steps:

   1-preprocess-wikipedia-dump
   2-extract-entities-mentions-frequency-counts-pages
   3-map-wikipedia-wikidata
   4-extract-locations-wikidata
   5-create-wikidata-gazetteer
   6-map-wikidata-entities-classes
   7-obtain-glove-entity-embeddings

Resulting Files
---------------
These scripts will produce the following outputs (note that entities are
percent encoded across all files):

- In ``resources/wikipedia/extractedResources/``:

    - A ``Pages/`` folder, containing a JSON file for each page available
      in the input Wikipedia dump. Note that due to the presence of specific
      characters of to the length of some pages titles, some titles have been
      hashed.
    - ``hashed_duplicates.csv``: just to check in case there are issues with
      duplicate hashed filenames. This file should remain empty.
    - A ``Store-Counts/`` folder, containing partial counts as JSON files.
    - ``entities_overall_dict.json``: this is a dictionary which maps each
      entity to a :py:class:`~collections.Counter` object of all possible
      mentions
    - ``mention_overall_dict.json``: this is a dictionary which maps each
      mention to a :py:class:`~collections.Counter` object of all possible
      associated entities.
    - ``overall_entity_freq.json``: this is a dictionary which simply maps an
      entity to its overall frequency in the Wikipedia corpus.
    - ``overall_mentions_freq.json``: this is a dictionary which simply maps a
      mention to its overall frequency in the Wikipedia corpus.
    - ``entity_inlink_dict.json``: this dictionary gives you a list of pages
      linking to each Wikipedia page.
    - ``entity_outlink_dict.json``: this dictionary gives you a list of pages
      linked from each Wikipedia page.
    - ``wikipedia2wikidata.json``: a dictionary mapping Wikipedia pages to
      Wikidata IDs.
    - ``wikidata2wikipedia.json``: a dictionary mapping Wikidata IDs to a list
      of Wikipedia pages with associated frequency.

- In ``resources/wikidata/extracted/``:

    - A list of CSV files, each containing 5,000 rows corresponding to
      geographical entities extracted from Wikidata, with names following the
      format ``till_<record ID>_item.csv``.
    - ``wikidata_gazetteer.csv``: The Wikidata-based gazetteer.
    - ``mentions_to_wikidata.json``: A dictionary that maps mentions to
      Wikidata IDs (absolute counts).
    - ``wikidata_to_mentions.json``: A dictionary that maps Wikidata IDs to
      mentions (absolute counts).
    - ``mentions_to_wikidata_normalized.json``: A dictionary that maps mentions
      to Wikidata IDs (normalized).
    - ``wikidata_to_mentions_normalized.json``: A dictionary that maps Wikidata
      IDs to mentions (normalized).
    - ``overall_entity_freq_wikidata.json``: this is a dictionary which simply
      maps a Wikidata entity to its overall frequency in the Wikipedia corpus.
    - ``gazetteer_entity_embeddings.npy``: Wikidata embeddings of entities in
      our gazetteer.
    - ``gazetteer_entity_ids.txt``: Mapped Wikidata IDs of the entities in our
      gazetteer.
    - ``gazetteer_wkdtclass_embeddings.npy``: Wikidata embeddings of entity
      classes in our gazetteer.
    - ``gazetteer_wkdtclass_ids.txt``: Mapped Wikidata IDs of the entity
      classes in our gazetteer.

- In ``resources/``:

    - ``embeddings_database.db``: A database containing GloVe and Entity
      embeddings.
