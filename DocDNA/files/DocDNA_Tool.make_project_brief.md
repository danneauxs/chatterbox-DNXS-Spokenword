# DocDNA_Tool.make_project_brief

> make_project_brief.py

## Public API


### Functions
- **is_excluded**
- **module_name_from_path**
- **read_text_safely**
- **get_module_summary** — Parse AST, extract module docstring, defs, imports, entrypoint flag.
- **detect_frameworks_and_side_effects**
- **build_local_import_graph** — Return graph edges: module -> set(dependencies) for local modules only.
- **topo_sort**
- **main**

## Imports (local guesses)
- ast, collections, json, os, pathlib, re, sys, typing, warnings

## Entrypoint
- Contains `if __name__ == '__main__':` block