from __future__ import annotations

import os
import argparse
from collections.abc import Sequence


def run_lrc(filenames: Sequence[str]) -> int:
    """
    Run the lrc command if the debian/copyright file exists.
    """
    retv = 0

    if os.path.exists("debian/copyright"):
        # Check if lrc is installed
        if os.system("command -v lrc > /dev/null 2>&1") != 0:
            print("lrc command not found. Please install it to use this hook.")
            return 1

        # Run the lrc command in the current directory
        retv = os.system("lrc")

    return retv


def main(argv: Sequence[str] | None = None) -> int:
    """
    Main function to parse arguments and run the lrc command.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'filenames', nargs='*',
        help='Filenames pre-commit believes are changed.',
    )

    args = parser.parse_args(argv)

    return run_lrc(args.filenames)


if __name__ == '__main__':
    raise SystemExit(main())
