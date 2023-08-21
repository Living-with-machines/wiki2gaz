7. Obtain GloVe and Entity Embeddings
=====================================

By default, ``wiki2gaz`` looks for your resources directory at ``./resources``.
After running step 6, we assume your directory set up is as follows:

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

This step allows you to create a sqlite3 database which contains
both GloVe word embeddings and Wikipedia2vec entity (represented
by the corresponding Wikidata ID) and word embeddings. Run the
script as follows:

.. code-block:: bash

    $ python wiki2gaz/download_and_merge_embeddings_databases.py

The script automates the download and aggregation of
`GloVe <https://nlp.stanford.edu/projects/glove/>`_ embeddings and
embeddings from the `Radboud Entity Linker (REL) <https://github.com/informagi/REL>`_.

The script merges the embeddings into a single database called
``resources/rel_db/embeddings_database.db``, in two different tables:
``glove_embeddings`` (containing GloVe word embeddings) and
``entity_embeddings`` (containing Wikipedia2vec entity and word
embeddings).

.. note::

    The script only keeps entity embeddings for entities appearing
    in the gazetteer and changes their key from ``ENTITY/Wikipedia_title``
    to ``ENTITY/Wikidata_id``, to make things consistent across resources.
