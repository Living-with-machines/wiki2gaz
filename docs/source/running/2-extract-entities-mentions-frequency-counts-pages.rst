2. Extract entities/mentions frequency counts and pages
=======================================================

Ensure that you have completed the pre-processing step for the Wikipedia dump
using the WikiExtractor tool. The processed data should be available in the
``resources/wikipedia/processedWiki/`` folder. To extract entity and mention
statistics from the processed Wikipedia dump, follow these steps:

Step 1: Extract Entity and Mention Statistics
---------------------------------------------
Run the script provided to extract entity and mention statistics from the
processed Wikipedia dump, e.g., how many times the mention ``London`` is
pointing to Wikipedia page of the capital of the UK and how many times to
``London,_Ontario``:

.. code-block:: bash

    $ python extract_freq_and_pages.py

The script performs the following tasks:

* **Divides statistics in the n-folders** constituting the output of the
  WikiExtractor and will be saved in the ``resources/wikipedia/
  extractedResources/Store-Counts/`` folder as JSON files.

* **Counts the frequency of entities and mentions**: The script analyzes the
  processed Wikipedia data and calculates the frequency of entities and
  mentions throughout the corpus.

* **Generates pages for entities**: The script creates a ``Pages/`` folder
  containing a JSON file for each page available in the processed Wikipedia
  data. These files contain detailed information about each page, including
  sections and other relevant aspects. For more information about Entity-Aspect
  Linking, see `"EAL: A Toolkit and Dataset for Entity-Aspect Linking" <https://madoc.bib.uni-mannheim.de/49596/1/EAL.pdf>`_

.. note::
    Note that you can run the script in **test mode** using the
    flag ``-t``, which will consider only a sub-part of the corpus.

.. note::
    A previous version of these scripts can be found in
    `fedenanni/Reimplementing-TagMe <https://github.com/fedenanni/Reimplementing-TagMe>`_.

Step 2: Aggregate all entity and mention counts
-----------------------------------------------

Run the script provided to aggregate all entity and mention counts:

.. code-block:: bash

    $ python aggregate_all_counts.py

* **Generates JSON files for entity and mention statistics**: The script
  produces two JSON files:

   * ``entities_overall_dict.json``: This dictionary maps each entity to a
     :py:class:`~collections.Counter` object, representing the count of all
     possible mentions associated with that entity.

   * ``mention_overall_dict.json``: This dictionary maps each mention to a
     :py:class:`~collections.Counter` object, representing the count of all
     possible associated entities.

* **Generates other files for entity-related statistics**: The script also
  creates additional JSON files:

   * ``overall_entity_freq.json``: This dictionary maps each entity to its
     overall frequency in the Wikipedia corpus.

   * ``overall_mentions_freq.json``: This dictionary maps each mention to its
     overall frequency in the Wikipedia corpus.

.. note::
    Note that, like above, you can run the script in **test mode** using the
    flag ``-t``, which will consider only a sub-part of the corpus.

.. note::
    A previous version of these scripts can be found in
    `fedenanni/Reimplementing-TagMe <https://github.com/fedenanni/Reimplementing-TagMe>`_.

Output files
------------------------
After running the script, you will find the generated output files in the
``resources/wikipedia/extractedResources/`` folder.