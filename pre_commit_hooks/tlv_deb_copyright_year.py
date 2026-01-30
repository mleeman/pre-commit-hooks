from __future__ import annotations

import os
import re
import argparse
from datetime import datetime
from collections.abc import Sequence


def check_debian_copyright(filenames: Sequence[str]) -> int:
    retv = 0
    filepath = "debian/copyright"

    if os.path.exists(filepath):
        with open(filepath, "r+") as cp_file:
            content = cp_file.read()
            current_year = datetime.now().year

            # Check for DEP-5 Format header
            dep5_pattern = r"^Format:\s+https?://www\.debian\.org/doc/packaging-manuals/copyright-format/\d+\.\d+/"
            if not re.search(dep5_pattern, content, re.MULTILINE):
                print(
                    f"Error: {filepath} is not in DEP-5 format (missing valid Format header).")
                return 1

            # Update year ranges (e.g., 2020-2025 -> 2020-2026)
            # This regex looks for 'Copyright: ' followed by a start year and an old end year
            # Group 1: 'Copyright: ' + optional whitespace
            # Group 2: The start year and dash (e.g., '2020-')
            # Group 3: The old end year that needs replacing
            range_pattern = r"(Copyright:\s+.*?\d{4}-)(\d{4})"

            def year_repl(match):
                prefix = match.group(1)
                old_year = match.group(2)
                if old_year != str(current_year):
                    return f"{prefix}{current_year}"
                return match.group(0)

            new_content = re.sub(range_pattern, year_repl, content)

            # Handle cases where it's a single year (e.g., Copyright: 2024 -> 2024-2026)
            # This is optional but often desired in DEP-5
            single_year_pattern = rf"(Copyright:\s+.*?)(\d{{4}})(?![-\d])"

            def single_repl(match):
                prefix = match.group(1)
                year = match.group(2)
                if year != str(current_year):
                    return f"{prefix}{year}-{current_year}"
                return match.group(0)

            new_content = re.sub(single_year_pattern, single_repl, new_content)

            if content != new_content:
                print(f"Updating {filepath} to year {current_year}")
                cp_file.seek(0)
                cp_file.write(new_content)
                cp_file.truncate()
                retv = 1

            # Check if current year is mentioned at all (legacy check)
            if str(current_year) not in new_content:
                print(
                    f"Warning: {current_year} still not found in {filepath} after adjustment.")
                retv = 1

    return retv


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames changed.')
    args = parser.parse_args(argv)
    return check_debian_copyright(args.filenames)


if __name__ == '__main__':
    raise SystemExit(main())
