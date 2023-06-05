5. Create a Wikidata-based gazetteer
====================================

To create a gazetteer based on Wikidata, run the ``create_wk_gazetteer.py``
script:

.. code-block:: bash

    $ python create_wk_gazetteer.py

The script handles the concatenation of CSV files, linking of alternate names
and mentions, and calculation of entity relevance. Here's what the script does:

#. The script **combines the CSV files** generated in the previous step, each
   representing geographical entities extracted from Wikidata, into a unified
   CSV file named ``wikidata_gazetteer.csv``. This file serves as the main
   gazetteer containing consolidated information about the entities.

#. The script **extracts alternate names and mentions** from the Wikipedia
   resources associated with each geographical entity and links them to the
   corresponding Wikidata locations. It performs the following tasks:
   
   * **Collect Alternate Names**: The script gathers alternate names or labels
     from the Wikipedia resources.

   * **Map Mentions to Wikidata IDs**: It creates a dictionary named
     ``mentions_to_wikidata.json`` that maps mentions to the corresponding
     Wikidata IDs. This dictionary provides the absolute count of mentions for
     each Wikidata ID.

     .. code-block:: py

         >>> data["London"]
         {'Q84': 76938, 'Q170027': 142, ...}

   * **Map Wikidata IDs to Mentions**: The script generates a dictionary named
     ``wikidata_to_mentions.json`` that maps Wikidata IDs to mentions. This
     dictionary provides the absolute count of mentions for each Wikidata entity.

     .. code-block:: py

         >>> data["Q84"]
         {'London': 76938, 'City of London': 1, ...}

   * **Normalise Mention-Wikidata ID Probabilities**: It creates two additional
     dictionaries, ``mentions_to_wikidata_normalized.json`` and
     ``wikidata_to_mentions_normalized.json``, which provide the probability of
     a mention referring to a particular Wikidata ID. These dictionaries offer
     a normalized measure of association.

     For example, the probability of London in Kiribati (``Q2477346``) of
     being referred to as ``"London"`` is ``0.80``, and that's the measure we
     are interested in here (note that this is different from the probability
     of the mention ``"London"`` referring to the location in Kiribati, which
     is close to ``0`` because of the high prominence of the English city).

     .. code-block:: py
         
         # mentions_to_wikidata_normalized.json
         >>> data["London"]
         {'Q84': 0.9762342820164698, 'Q170027': 0.02005083309799492, ...}
         
         # wikidata_to_mentions_normalized.json
         >>> data["Q84"]
         {'London': 0.9762342820164698, 'City of London: 1.2688584080902413e-05, ...}

#. The script produces a dictionary named ``overall_entity_freq_wikidata.json``
   that **maps each Wikidata entity to its overall frequency** in the Wikipedia
   corpus.