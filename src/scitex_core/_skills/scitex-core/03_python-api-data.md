# Python API — data + reproducibility

Submodules: `dict`, `types`, `dt`, `parallel`, `repro`.

## dict

Shadows builtin `dict`; alias on import.

* `DotDict` — attribute-style access, recursive
* `listed_dict` — list-of-dicts to dict-of-lists transpose
* `flatten(d, sep=".")` — nested → flat
* `safe_merge(a, b)` — merge without silent overwrite
* `pop_keys(d, keys)` — bulk pop returning popped values
* `replace(d, mapping)` — value substitution
* `to_str(d)` — stable string representation

## types

Type aliases + validators:

* `ArrayLike` — union of list/tuple/ndarray/tensor
* `ColorLike` — str, RGB, RGBA
* `is_array_like(x)` — runtime check
* `is_list_of_type(xs, T)`, `is_listed_X(xs, T)` — element-type check

## dt — datetime helpers

* `linspace(start, end, n)` — evenly spaced `datetime` values between two instants

## parallel

* `run(func, iterable, n_jobs=1, backend="thread", ...)` — map across inputs; collects results in order

## repro — reproducibility

* `gen_id()` / `gen_ID` — unique short id
* `gen_timestamp()` / `timestamp` — ISO-ish timestamp string
* `hash_array(arr)` — stable hash of ndarray contents + dtype + shape
* `RandomStateManager` — seed numpy / python-random / torch together
* `get()`, `reset()` — module-level accessors to the global `RandomStateManager`
