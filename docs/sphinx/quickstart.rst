Quickstart
==========

The example below exercises every public submodule of ``scitex-core``. The
same script lives at ``examples/quickstart.py`` in the repository.

.. code-block:: python

   import scitex_core as core

   # logging: structured logger
   log = core.logging.SciTeXLogger("quickstart")
   log.info("scitex-core quickstart starting")

   # repro: deterministic id + timestamp
   rid = core.repro.gen_id()
   ts = core.repro.timestamp()

   # path: locate this file
   here = core.path.get_this_path()

   # sh: run a shell command
   result = core.sh.sh_run(["echo", "hello"], verbose=False)

   # str: helpers
   core.str.color_text("hi", "red")
   core.str.clean_path("/tmp/./x")

   # types: guards
   core.types.is_list_of_type([1, 2, 3], int)

   # dict: DotDict + flatten
   d = core.dict.DotDict({"a": {"b": 1}})
   d.a.b                      # 1
   core.dict.flatten({"a": {"b": 1}})  # {"a_b": 1}

   # parallel: parallel map
   out = core.parallel.run(lambda x: x * x, [(1,), (2,), (3,)], n_jobs=1)
   # out -> [1, 4, 9]

   # dt: datetime utilities
   from datetime import datetime, timedelta
   start = datetime(2024, 1, 1)
   pts = core.dt.linspace(start, start + timedelta(days=1), n_samples=3)


Submodule Overview
------------------

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Submodule
     - Purpose
   * - ``logging``
     - Structured logger (``SciTeXLogger``) with consistent formatting.
   * - ``path``
     - Path resolution helpers (``get_this_path``, etc.).
   * - ``repro``
     - Reproducibility primitives — IDs, timestamps, seed helpers.
   * - ``sh``
     - Subprocess helpers (``sh_run``) with sane defaults.
   * - ``str``
     - String utilities (color, path cleaning, formatting).
   * - ``types``
     - Lightweight type guards.
   * - ``dict``
     - ``DotDict`` plus flatten/unflatten utilities.
   * - ``parallel``
     - ``run()`` for joblib/threading-style parallel maps.
   * - ``dt``
     - Datetime utilities (``linspace`` between datetimes, etc.).
   * - ``errors``
     - Common exception classes used across the SciTeX ecosystem.
