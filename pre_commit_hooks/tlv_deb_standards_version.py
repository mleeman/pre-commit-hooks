from __future__ import annotations

import os
import re
import argparse
from collections.abc import Sequence

# Define the latest Standards-Version as a constant for easy updating
LATEST_STANDARDS_VERSION = "4.7.2"


def check_debian_control(filenames: Sequence[str]) -> int:
    """
    Check if the debian/control file complies with the latest
    Standards-Version.
    """
    retv = 0
    c_path = "debian/control"

    if os.path.exists(c_path):
        with open(c_path, "r") as ctrl_file:
            txt = ctrl_file.read()

            # Search for the Standards-Version line
            # This regex looks for 'Standards-Version:' followed by the
            # version string
            match = re.search(r"Standards-Version:\s*([\d.]+)", txt)

            if not match:
                print(f"{c_path} is missing a Standards-Version field.")
                retv = 1
            elif match.group(1) != LATEST_STANDARDS_VERSION:
                found_version = match.group(1)
                print(
                    f"{c_path} reports Standards-Version {found_version}. "
                    f"It should be updated to {LATEST_STANDARDS_VERSION}."
                )
                retv = 1

    return retv


def main(argv: Sequence[str] | None = None) -> int:
    """
    Main function to parse arguments and check the debian/control file.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'filenames', nargs='*',
        help='Filenames pre-commit believes are changed.',
    )

    args = parser.parse_args(argv)

    return check_debian_control(args.filenames)


if __name__ == '__main__':
    raise SystemExit(main())
