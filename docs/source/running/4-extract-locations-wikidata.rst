4. Extract locations from Wikidata
==================================

To extract locations from Wikidata along with their relevant properties,
if they have a corresponding page on Wikipedia, follow these steps:

Step 1: Obtain the Wikidata Dump
--------------------------------
Ensure that you have downloaded a full Wikidata dump file named
``latest-all.json.bz2``, placed in the ``resources/wikidata/`` directory.

If you haven't downloaded this dump file yet, you can acquire it from
`Wikimedia's dump directory <https://dumps.wikimedia.org/wikidatawiki/entities>`_.

Step 2: Run the Extraction Script
---------------------------------
Execute the provided script to extract locations from the Wikidata dump:

.. code-block:: bash

    $ python wikidata_extraction.py

.. note::

    This script is partially based on `this code <https://akbaritabar.netlify.app/how_to_use_a_wikidata_dump>`_.

    By default, the script runs on test mode. You can change this behaviour by
    setting ``-t`` to ``False``:

    .. code-block:: bash
    
        $ python wikidata_extraction.py -t 'False'

The script performs the following tasks:

* **Filtering Locations**: The script focuses on extracting geographical entities
  from the Wikidata dump. It identifies entities with location-related
  properties, such as latitude and longitude, indicating their geographical
  relevance.

* **Partial Extraction**: Due to the large size of the Wikidata dump, the script
  processes the data in smaller portions. It generates multiple CSV files, each
  containing 5,000 rows of geographical entities.

.. warning::

    Beware that this step will take about 2 full days.

Step 3: Store the Extracted Data
--------------------------------
After running the extraction script, you will find the extracted data stored
in the ``resources/wikidata/extracted/`` folder. Make sure to check this
folder for multiple CSV files. This series of CSV files, each consisting of
5,000 rows representing geographical entities extracted from Wikidata.
These files provide structured information about the entities, including:

* ``wikidata_id``: The unique identifier assigned to each geographical entity
  in the Wikidata knowledge base.

* ``english_label``: The English label or name of the geographical entity.

* ``instance_of``: The type or category of the entity, indicating its
  classification or nature.

* ``description_set``: A set of descriptions or brief explanations associated
  with the entity.

* ``alias_dict``: A dictionary of alternative labels or names for the entity,
  providing additional variations or synonyms.

* ``nativelabel``: The label or name of the entity in its native or local
  language.

* ``population_dict``: A dictionary containing information about the population
  of the geographical entity.

* ``area``: The area or size of the geographical entity.

* ``hcounties``: The historical counties associated with the entity.

* ``date_opening``: The date when the entity was opened, established, or
  inaugurated.

* ``date_closing``: The date when the entity was closed, ceased operations, or
  discontinued.

* ``inception_date``: The date of the entity's inception or creation,
  representing its starting point or establishment.

* ``dissolved_date``: The date of dissolution or termination of the entity,
  signifying its end or discontinuation.

* ``follows``: The entity that the current entity follows or succeeds in a
  particular context or sequence.

* ``replaces``: The entity that the current entity replaces or takes the
  position of in a particular context or sequence.

* ``adm_regions``: The administrative regions or subdivisions associated with
  the geographical entity, providing information about its hierarchical
  administrative structure.

* ``countries``: The countries to which the geographical entity belongs or is
  associated with.

* ``continents``: The continents to which the geographical entity belongs or is
  located in.

* ``capital_of``: The entity for which the geographical entity serves as the
  capital city or administrative center.

* ``borders``: TODO

* ``near_water``: An indication of whether the geographical entity is located
  near or adjacent to a body of water.

* ``latitude``: The latitude coordinate of the geographical entity's location.

* ``longitude``: The longitude coordinate of the geographical entity's
  location.

* ``wikititle``: The title of the corresponding Wikipedia page for the
  geographical entity.

* ``geonamesIDs``: The Geonames IDs associated with the geographical entity,
  providing further identification or linkage.

* ``connectswith``: Other entities or elements with which the geographical
  entity is connected or associated.

* ``street_address``: The street address or location information associated
  with the entity, if applicable.

* ``street_located``: The street or road where the entity is located, if
  applicable.

* ``postal_code``: The postal code associated with the geographical entity, if
  applicable.
