3. Map Wikipedia and Wikidata
=============================

By default, ``wiki2gaz`` looks for your resources directory at ``./resources``.
After running step 2, we assume your directory set up is as follows:

::

    your_cwd
    ├──wiki2gaz
    └──resources    
        └── wikipedia
            ├──processedWiki
            └──extractedResources

.. note::
  If this is not your set up, you can use the ``-p`` flag with all scripts to set the path to your resources directory.

To establish a mapping between Wikipedia pages and corresponding Wikidata entities, follow these steps:

Step 1: Obtain a Wikipedia/Wikidata Index
------------------------------------------------
To run the next steps, you need to have access to a Wikipedia/Wikidata
index required for the mapping process. This index is created by following 
`these instructions <https://www.github.com/jcklie/wikimapper#create-your-own-index>`_.
We have used a SQL dump from October 2021.

.. note:: wiki2gaz will expect your Wikidata to be saved in "./resources/wikidata/". You should rename your 'data' directory to align to this.

Step 2: Run the Mapping Script
------------------------------
Execute the provided script to perform the mapping of Wikipedia pages to
Wikidata entities:

.. code-block:: bash

    $ python wiki2gaz/map_wikidata_wikipedia.py

The script does the following:

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
