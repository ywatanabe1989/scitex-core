"""scitex-core quickstart — exercises the public submodule surface.

Each block touches one submodule so the example doubles as smoke coverage
for `scitex_core.{logging, path, repro, sh, str, types, dict, parallel, dt}`.
"""

from __future__ import annotations


def main() -> int:
    import scitex_core as core

    # logging: structured logger class
    log = core.logging.SciTeXLogger("quickstart")
    log.info("scitex-core quickstart starting")

    # repro: deterministic id + timestamp
    rid = core.repro.gen_id()
    ts = core.repro.timestamp()
    assert isinstance(rid, str) and isinstance(ts, str)

    # path: locate this file
    here = core.path.get_this_path()
    assert here  # truthy path-like

    # sh: run a no-op shell command (list form, per signature)
    result = core.sh.sh_run(["echo", "hello"], verbose=False)
    assert "hello" in str(result)

    # str: color_text + clean_path round-trip
    assert isinstance(core.str.color_text("hi", "red"), str)
    assert isinstance(core.str.clean_path("/tmp/./x"), str)

    # types: list-of-type guard
    assert core.types.is_list_of_type([1, 2, 3], int)

    # dict: DotDict + flatten
    d = core.dict.DotDict({"a": {"b": 1}})
    assert d.a.b == 1
    assert core.dict.flatten({"a": {"b": 1}}) == {"a_b": 1}

    # parallel: trivial run with tuple-args (per scitex_core.parallel.run signature)
    out = core.parallel.run(lambda x: x * x, [(1,), (2,), (3,)], n_jobs=1)
    assert list(out) == [1, 4, 9]

    # dt: linspace between two datetimes
    from datetime import datetime, timedelta

    start = datetime(2024, 1, 1)
    pts = core.dt.linspace(start, start + timedelta(days=1), n_samples=3)
    assert len(pts) == 3

    log.info("scitex-core quickstart OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
