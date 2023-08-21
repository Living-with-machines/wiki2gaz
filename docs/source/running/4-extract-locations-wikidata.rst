4. Extract locations from Wikidata
==================================

By default, ``wiki2gaz`` looks for your resources directory at ``./resources``.
After running step 3, we assume your directory set up is as follows:

::

    your_cwd
    ├──wiki2gaz
    └──resources    
        ├── wikipedia
        │   ├──processedWiki
        │   └──extractedResources
        └── wikidata
           ├──enwiki-latest-page.sql.gz
           ├──...
           └──index_enwiki-latest.db

.. note::
  If this is not your set up, you can use the ``-p`` flag with all scripts to set the path to your resources directory.

To extract locations from Wikidata along with their relevant properties,
if they have a corresponding page on Wikipedia, follow these steps:

Step 1: Obtain the Wikidata Dump
--------------------------------
Download a full Wikidata dump file ``latest-all.json.bz2`` from the
`Wikimedia's dump directory <https://dumps.wikimedia.org/wikidatawiki/entities>`_,
and store it in the ``resources/wikidata/`` directory.

.. code-block:: bash

    $ wget -P ./resources/wikidata/ https://dumps.wikimedia.org/wikidatawiki/entities/latest-all.json.bz2

Step 2: Run the Extraction Script
---------------------------------
Execute the provided script to extract locations from the Wikidata dump:

.. code-block:: bash

    $ python wiki2gaz/wikidata_extraction.py

.. note::

    This script is partially based on `this code <https://akbaritabar.netlify.app/how_to_use_a_wikidata_dump>`_.

.. note::

    By default, the script runs on test mode. You can change this behaviour by
    setting ``-t`` to ``False``:

    .. code-block:: bash
    
        $ python wikidata_extraction.py -t 'False'

The script performs the following tasks:

* **Filtering Locations**: The script focuses on extracting geographical entities
  from the Wikidata dump. It identifies entities with latitude and longitude.

* **Partial Extraction**: Due to the large size of the Wikidata dump, the script
  processes the data in smaller portions. It generates multiple CSV files, each
  containing 5,000 rows of geographical entities.

.. warning::

    Beware that this step will take about 2 full days.

Output files
--------------------------------
After running the extraction script, you will find the extracted data stored
in the ``resources/wikidata/extracted/`` folder. The resulting CSV files
consist of 5,000 rows representing geographical entities extracted from
Wikidata. These files provide structured information about the entities,
including:

* ``wikidata_id``: The unique identifier assigned to each geographical entity
  in the Wikidata knowledge base.

* ``english_label``: The English label or name of the geographical entity.

* ``instance_of``: The Wikidata classes of the entity.

* ``alias_dict``: A dictionary of alternative labels or names for the entity,
  providing additional variations or synonyms.

* ``nativelabel``: A list of names of the entity in its native or local
  language.

* ``hcounties``: The historical counties associated with the entity.

* ``countries``: The countries to which the geographical entity belongs or is
  associated with.

* ``latitude``: The latitude coordinate of the geographical entity's location.

* ``longitude``: The longitude coordinate of the geographical entity's
  location.