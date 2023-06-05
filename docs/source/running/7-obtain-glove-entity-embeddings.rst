7. Obtain GloVe and Entity Embeddings
=====================================

This step allows you to create a sqlite3 database which contains
both GloVe word embeddings and Wikipedia2vec entity (represented
by the corresponding Wikidata ID) and word embeddings. Run the
script as follows:

.. code-block:: bash

    $ python download_and_merge_embeddings_databases.py

The script automates the download and aggregation of
`GloVe <https://nlp.stanford.edu/projects/glove/>`_ embeddings and
embeddings from the `Radboud Entity Linker (REL) <https://github.com/informagi/REL>`_.

The script merges the embeddings into a single database called
``resources/embeddings_database.db``, in two different tables:
``glove_embeddings`` (containing GloVe word embeddings) and
``entity_embeddings`` (containing Wikipedia2vec entity and word
embeddings).

.. note::

    The script only keeps entity embeddings for entities appearing
    in the gazetteer and changes their key from ``ENTITY/Wikipedia_title``
    to ``ENTITY/Wikidata_id``, to make things consistent across resources.
