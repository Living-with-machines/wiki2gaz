1. Pre-process a Wikipedia Dump
===============================

The pre-processing of a Wikipedia dump involves the following steps:

Step 1: Download the Wikipedia Dump
-----------------------------------

Start by downloading a Wikipedia dump file. In our example, we use the
``enwiki-20211001`` dump. You can obtain the dump file from
`Wikimedia <https://dumps.wikimedia.org/enwiki>`_.

Step 2: Process the Dump with WikiExtractor
-------------------------------------------

To extract the desired information from the Wikipedia dump, we will use the
WikiExtractor tool. Follow these steps:

#. Clone the WikiExtractor repository:

   .. code-block:: bash

       $ git clone https://github.com/attardi/wikiextractor.git

#. Switch to a specific version of the code:

   .. code-block:: bash

       $ cd wikiextractor
       $ git checkout e4abb4cbd019b0257824ee47c23dd163919b731b

   The reason we have to use this specific version is because the current
   version of the WikiExtractor the possibility of keeping sections is no
   longer offered. Instead, we use the version of the code from March 2020.

#. Run the WikiExtractor tool to process the Wikipedia dump:

   .. code-block:: bash

       $ python WikiExtractor.py -l -s \
         -o ../resources/wikipedia/processedWiki/ \
         [path-to-Wikipedia-Dump.xml.bz2]
   
   This will process the dump and store the result in the
   ``resources/wikipedia/processedWiki/`` folder.

   .. warning::

       Replace ``[path-to-Wikipedia-Dump.xml.bz2]`` with the actual path to
       the downloaded Wikipedia dump file.

   .. note::
       * The ``-l`` flag keeps the links in the extracted text.
       * The ``-s`` flag retains the sections in the extracted text.
