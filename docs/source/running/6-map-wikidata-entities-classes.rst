6. Map Wikidata entities to classes
===================================

To map Wikidata entities to their most relevant classes, run the
``map_wikidata_to_classes.py`` script:

.. code-block:: bash

    $ python map_wikidata_to_classes.py

The script maps Wikidata entities to their most common entity class.
The script generates a dictionary, stored as
``resources/wikidata/entity2class.txt``, that maps each Wikidata entity
to its most relevant class.