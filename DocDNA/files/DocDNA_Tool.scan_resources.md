# DocDNA_Tool.scan_resources

> Scan non-Python assets and configs to enrich the DocDNA for AI reasoning.

## Public API


### Functions
- **should_skip**
- **safe_read_text**
- **summarize_json**
- **summarize_ini**
- **summarize_toml**
- **summarize_markdown**
- **summarize_text**
- **summarize_requirements**
- **summarize_script**
- **extract_env_vars**
- **summarize_config_constants**
- **main**
- **shape**
- **keys**

## Imports (local guesses)
- __future__, ast, configparser, json, os, pathlib, re, sys, tomllib, typing

## Side-effect signals
- sys_exit

## Entrypoint
- Contains `if __name__ == '__main__':` block