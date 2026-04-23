# Python API — stdlib-style utilities

Submodules that mirror / extend Python stdlib: `errors`, `logging`,
`sh`, `path`, `str`.

## errors

Rich exception hierarchy used across SciTeX packages (context-aware
messages, optional suggestions). Import the classes you need from
`scitex_core.errors`.

## logging

Drop-in replacement for stdlib `logging` with extra levels and
auto-configured file output.

* `getLogger(name)` — returns a configured logger
* Levels: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`, `SUCCESS`, `FAIL`
* `configure(level, enable_file, enable_console, capture_prints)` — reconfigure
* `get_log_path()` — current rotating-log path
* `Tee`, `tee` — split stdout/stderr to file
* `log_to_file(path)` — context manager

Auto-configured on import (level from `SCITEX_CORE_LOG_LEVEL`, file enabled).

## sh — safe shell

* `sh(command_list, verbose=True, return_as="dict"|"str", timeout=None, stream_output=False)`
* `quote(s)`, `validate_command(cmd)`, `execute(cmd, ...)` — lower-level helpers
* `ShellResult`, `CommandInput`, `ReturnFormat` — types

List-form only. For pipes, chain subprocesses in Python.

## path

* `find_file(root, pattern)`, `find_dir(root, pattern)`, `find_git_root(start)`
* `this_path()`, `get_this_path()` — caller-file introspection
* `clean(path)` — normalize
* Symlink utilities: `symlink`, `is_symlink`, `readlink`, `resolve_symlinks`,
  `create_relative_symlink`, `unlink_symlink`, `list_symlinks`, `fix_broken_symlinks`

## str

Shadows builtin `str`; alias on import. Categories:

* ANSI color: `color_text`, `ct`, `remove_ansi`
* Search / grep: `grep`, `search`, `parse`
* LaTeX: `latex_style`, `to_latex_style`, `safe_to_latex_style`,
  `latex_to_mathtext`, `latex_to_unicode`, `check_latex_capability`,
  `latex_fallback_decorator`, `enable_latex_fallback`, `disable_latex_fallback`,
  `get_fallback_mode`, `set_fallback_mode`, `reset_latex_cache`, `safe_latex_render`
* Plot text: `format_plot_text`, `format_axis_label`, `format_title`,
  `axis_label`, `title`, `scientific_text`, `check_unit_consistency`
* Numeric formatting: `factor_out_digits`, `auto_factor_axis`, `smart_tick_formatter`,
  `readable_bytes`
* Misc: `clean_path`, `decapitalize`, `squeeze_spaces`, `printc`,
  `print_debug`, `replace`, `mask_api`
