3. Map Wikipedia and Wikidata
=============================

To establish a mapping between Wikipedia pages and corresponding Wikidata
entities, follow these steps:

Step 1: Availability of Wikipedia/Wikidata Index
------------------------------------------------
Ensure that you have access to a specific Wikipedia/Wikidata index required
for the mapping process. This index is created by following the instructions
outlined in `these instructions <https://www.github.com/jcklie/wikimapper#create-your-own-index>`_.
We have previously used and tested the script with a SQL dump from
October 2021.

Step 2: Run the Mapping Script
------------------------------
Execute the provided script to perform the mapping of Wikipedia pages to
Wikidata entities:

.. code-block:: bash

    $ python map_wikidata_wikipedia.py

The script facilitates the following:

* **Lowercasing Wikipedia page titles**: To ensure consistency and improve
  matching accuracy, the script converts the Wikipedia page titles to lowercase
  in the database.

* **Generate JSON files for mapping**: The script produces two JSON files to
  establish the mapping:

    * ``wikipedia2wikidata.json``: This dictionary maps each Wikipedia page to
      its corresponding Wikidata ID. The keys in this dictionary represent
      Wikipedia page titles, while the values denote the associated Wikidata
      IDs.

    * ``wikidata2wikipedia.json``: This dictionary maps each Wikidata ID to a
      list of Wikipedia pages associated with that entity, along with their
      respective frequencies.

.. note::
    Note that you can run the script in **test mode** using the flag ``-t``,
    which will consider only a sub-part of the corpus.
