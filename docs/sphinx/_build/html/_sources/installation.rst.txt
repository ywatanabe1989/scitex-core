Installation
============

Requirements
------------

- Python >= 3.10

Basic Installation
------------------

.. code-block:: bash

   pip install scitex-core

This installs the core utilities (logging, path, repro, sh, str, types, dict,
parallel, dt, errors) along with the small set of runtime dependencies
(``numpy``, ``natsort``, ``colorama``, ``tqdm``, ``matplotlib``).

Development
-----------

.. code-block:: bash

   git clone https://github.com/ywatanabe1989/scitex-core.git
   cd scitex-core
   pip install -e ".[all]"

SciTeX Users
------------

If you use the umbrella ``scitex`` framework, ``scitex-core`` is already
installed as a transitive dependency::

   pip install scitex
