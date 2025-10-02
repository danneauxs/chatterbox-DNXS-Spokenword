#!/usr/bin/env python3
"""
Config Audit: map config flags to usage sites to find unused toggles.

Outputs reports/spider/config_usage.json and a simple Markdown summary.
"""
from __future__ import annotations

import ast
import json
from pathlib import Path
from typing import Dict, Set


def extract_flags(config_py: Path) -> Set[str]:
    flags = set()
    try:
        tree = ast.parse(config_py.read_text(encoding='utf-8'), filename=str(config_py))
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                for t in node.targets:
                    if isinstance(t, ast.Name) and t.id.isupper():
                        flags.add(t.id)
    except Exception:
        pass
    return flags


def scan_usage(repo: Path, flags: Set[str]) -> Dict[str, Set[str]]:
    usage: Dict[str, Set[str]] = {f: set() for f in flags}
    for p in repo.rglob('*.py'):
        if any(part in ('oldvenv', 'BACKUPS', 'archive', '.git', '__pycache__') for part in p.parts):
            continue
        try:
            txt = p.read_text(encoding='utf-8', errors='ignore')
        except Exception:
            continue
        for flag in flags:
            if flag in txt:
                usage[flag].add(str(p.relative_to(repo)))
    return usage


def main():
    repo = Path(__file__).resolve().parents[1]
    out_dir = repo / 'reports' / 'spider'
    out_dir.mkdir(parents=True, exist_ok=True)

    config_py = repo / 'config' / 'config.py'
    flags = extract_flags(config_py) if config_py.exists() else set()
    usage = scan_usage(repo, flags)
    usage_json = {k: sorted(list(v)) for k, v in usage.items()}
    (out_dir / 'config_usage.json').write_text(json.dumps(usage_json, indent=2), encoding='utf-8')

    # Markdown summary
    lines = ["# Config Flags Usage\n"]
    for k in sorted(flags):
        files = usage_json.get(k, [])
        lines.append(f"- {k}: {len(files)} refs")
        if len(files) == 0:
            lines.append(f"  - UNUSED")
    (out_dir / 'config_usage.md').write_text('\n'.join(lines), encoding='utf-8')
    print(f"Wrote {out_dir/'config_usage.json'} and {out_dir/'config_usage.md'}")


if __name__ == '__main__':
    main()

