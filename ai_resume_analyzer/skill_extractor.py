"""Find known skills in resume text using a small, editable CSV dictionary."""

import csv
import re
from pathlib import Path


def load_skill_dictionary(csv_path: Path) -> list[dict[str, str]]:
    with csv_path.open(encoding="utf-8-sig", newline="") as csv_file:
        return list(csv.DictReader(csv_file))


def find_skills(text: str, dictionary: list[dict[str, str]]) -> list[str]:
    """Return canonical skill names found as whole words or known aliases."""
    normalized = text.lower()
    found = set()
    for skill in dictionary:
        names = [skill["skill"], *skill["aliases"].split("|")]
        for name in names:
            name = name.strip().lower()
            if name and re.search(r"(?<![a-z0-9])" + re.escape(name) + r"(?![a-z0-9])", normalized):
                found.add(skill["skill"])
                break
    return sorted(found)
