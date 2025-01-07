#!/usr/bin/env python3

from __future__ import annotations

import os
import argparse
from collections.abc import Sequence


def main(argv: Sequence[str] | None = None) -> int:
    os.environ["GIT_AUTHOR_NAME"] = "Marc Leeman"
    os.environ["GIT_AUTHOR_EMAIL"] = "m.leeman@televic.com"

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
