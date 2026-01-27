import re
import sys
import os


def get_package_name():
    """Extracts the Source package name from debian/control."""
    if not os.path.exists("debian/control"):
        return None
    with open("debian/control", "r") as f:
        content = f.read()
        match = re.search(r"^Source:\s*(.*)", content, re.MULTILINE)
        return match.group(1).strip() if match else None


def fix_version(version):
    """
    Checks if version is A.BB.CC~* If not, tries to convert numbers to
    that format (padding with zeros).
    Example: 1.2.3 -> 1.02.03
    """
    # Regex for exactly A.BB.CC (where A is 1+ digits, BB and CC are exactly 2)
    target_pattern = r"^\d+\.\d{2}\.\d{2}(~.*)?$"

    if re.match(target_pattern, version):
        return version, False  # Already correct

    # Try to extract the numeric parts to fix them
    # Matches: (Major).(Minor).(Patch)(Optional Suffix)
    parts_match = re.match(r"^(\d+)\.(\d+)\.(\d+)(~.*)?$", version)
    if parts_match:
        major = parts_match.group(1)
        minor = parts_match.group(2).zfill(2)
        patch = parts_match.group(3).zfill(2)
        suffix = parts_match.group(4) if parts_match.group(4) else ""

        new_v = f"{major}.{minor}.{patch}{suffix}"
        return new_v, True

    return version, False  # Cannot safely auto-fix


def main():
    package_name = get_package_name()
    if not package_name or not package_name.startswith("televic-article-"):
        return 0

    changelog_path = "debian/changelog"
    if not os.path.exists(changelog_path):
        return 0

    with open(changelog_path, "r") as f:
        lines = f.readlines()

    if not lines:
        return 0

    # Debian changelog first line format: package (version) distribution;
    # urgency=xxx
    first_line = lines[0]
    match = re.search(r"\((.*?)\)", first_line)

    if match:
        old_v = match.group(1)
        new_v, fixed = fix_version(old_v)

        if fixed:
            print(
                f"Fixed version in {changelog_path}: {old_v} -> {new_v}")
            lines[0] = first_line.replace(
                f"({old_v})", f"({new_v})")
            with open(changelog_path, "w") as f:
                f.writelines(lines)
            return 1  # Return 1 so the user knows the file was modified

        # If it wasn't fixed but still doesn't match the required format
        if not re.match(r"^\d+\.\d{2}\.\d{2}(~.*)?$", new_v):
            print(
                f"Error: Version '{old_v}' does not match A.BB.CC format.")
            return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
