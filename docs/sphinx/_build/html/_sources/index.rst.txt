SciTeX Core
===========

**scitex-core** provides core infrastructure and fundamental utilities shared
across the SciTeX ecosystem: logging, path handling, reproducibility helpers,
shell utilities, string/dict/datetime helpers, type guards, parallel execution,
and a unified error hierarchy.

.. code-block:: python

   import scitex_core as core

   log = core.logging.SciTeXLogger("my_experiment")
   log.info("hello")

   rid = core.repro.gen_id()
   ts = core.repro.timestamp()

   d = core.dict.DotDict({"a": {"b": 1}})
   d.a.b  # 1


.. toctree::
   :maxdepth: 2
   :caption: Getting Started

   installation
   quickstart

.. toctree::
   :maxdepth: 2
   :caption: API Reference

   api/logging
   api/path
   api/repro
   api/sh
   api/str
   api/types
   api/dict
   api/parallel
   api/dt
   api/errors


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
