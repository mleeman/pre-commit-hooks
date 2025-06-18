from __future__ import annotations

import os
import re
import argparse
from datetime import datetime
from collections.abc import Sequence


def check_debian_copyright(filenames: Sequence[str]) -> int:
    """
    Check if the debian/copyright file contains the current year.
    """
    retv = 0

    if os.path.exists("debian/copyright"):
        with open("debian/copyright", "r") as cp_file:
            current_year = datetime.now().year
            txt = cp_file.read()
            if not re.findall(f"Copyright.*{current_year}", txt):
                print(
                    f"debian/copyright should include \"{current_year}\"")
                retv = 1

    return retv


def main(argv: Sequence[str] | None = None) -> int:
    """
    Main function to parse arguments and check the debian/copyright file.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'filenames', nargs='*',
        help='Filenames pre-commit believes are changed.',
    )

    args = parser.parse_args(argv)

    return check_debian_copyright(args.filenames)


if __name__ == '__main__':
    raise SystemExit(main())
