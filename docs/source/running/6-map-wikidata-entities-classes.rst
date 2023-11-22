6. Map Wikidata entities to classes
===================================

By default, ``wiki2gaz`` looks for your resources directory at ``./resources``.
After running step 5, we assume your directory set up is as follows:

::

    your_cwd
    ├──wiki2gaz
    └──resources    
        ├── wikipedia
        │   ├──processedWiki
        │   └──extractedResources
        └── wikidata
           ├──...
           └──extracted

.. note::
  If this is not your set up, you can use the ``-p`` flag with all scripts to set the path to your resources directory.

To map Wikidata entities to their most relevant classes, run the
``map_wikidata_to_classes.py`` script:

.. code-block:: bash

    $ python wiki2gaz/map_wikidata_to_classes.py

The script maps Wikidata entities to their most common entity class.
The script generates a dictionary, stored as
``resources/wikidata/entity2class.txt``, that maps each Wikidata entity
to its most relevant class.