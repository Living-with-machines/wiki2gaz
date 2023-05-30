7. Obtain GloVe and Entity Embeddings
=====================================

To effortlessly acquire both GloVe and Entity embeddings, run the
``download_and_merge_embeddings_databases.py`` script:

.. code-block:: bash

    $ python download_and_merge_embeddings_databases.py

The script enables download of GloVe and Entity embeddings without the need for
manual downloads or separate steps. The script automates the download and
aggregation of `GloVe <https://nlp.stanford.edu/projects/glove/>`_ and Entity
embeddings from `REL <https://github.com/informagi/REL>`_., enabling easy
access to the embeddings for various tasks, including semantic analysis, entity
representation, and information retrieval.

Using the downloaded Wikipedia dump, the GloVe embeddings, and the
Wikidata-based gazetteer, the script merges the embeddings into a single
database called ``resources/embeddings_database.db``, in two different tables:
``glove_embeddings`` and ``entity_embeddings``.

.. note::

    The script only keeps embeddings for entities appearing in the gazetteer
    and changes their key from ``ENTITY/Wikipedia_title`` to
    ``ENTITY/Wikidata_id``, to make things consistent across resources.
