#!/usr/bin/env python3
"""Compatibility wrapper for scripts/data/build_dataset_v1.py."""

from __future__ import annotations

import runpy
import sys
from pathlib import Path


def main() -> None:
    target = Path(__file__).resolve().parent / "data" / "build_dataset_v1.py"
    sys.argv[0] = str(target)
    runpy.run_path(str(target), run_name="__main__")


if __name__ == "__main__":
    main()
