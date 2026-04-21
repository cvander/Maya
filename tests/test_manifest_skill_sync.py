"""Manifest <-> SKILL.md sync tests: verify fields match between the two files."""

import re
import tomllib
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = REPO_ROOT / "skills"

_EXCLUDE_DIRS = {"_lib", "_skeleton", "__pycache__"}


def _discover_skills() -> list[Path]:
    """Discover skill directories by finding all manifest.toml files."""
    skills = []
    for manifest in sorted(SKILLS_DIR.glob("*/manifest.toml")):
        skill_dir = manifest.parent
        if skill_dir.name in _EXCLUDE_DIRS:
            continue
        skills.append(skill_dir)
    return skills


def _parse_yaml_frontmatter(text: str) -> dict:
    """Parse YAML frontmatter from a SKILL.md file (between --- markers).

    Uses simple regex parsing to avoid external YAML dependency.
    Handles: strings (quoted/unquoted), lists, and nested keys (flattened).
    """
    match = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    if not match:
        return {}

    frontmatter = {}
    raw = match.group(1)

    for line in raw.splitlines():
        # Skip empty lines and deeply nested keys (indented with 4+ spaces)
        if not line.strip() or line.startswith("    "):
            continue
        # Match top-level "key: value" lines (no leading whitespace or 2-space indent for metadata)
        kv_match = re.match(r"^(\w[\w_]*):\s*(.+)$", line)
        if kv_match:
            key = kv_match.group(1)
            value = kv_match.group(2).strip()
            # Strip quotes
            if (value.startswith('"') and value.endswith('"')) or (
                value.startswith("'") and value.endswith("'")
            ):
                value = value[1:-1]
            frontmatter[key] = value

    return frontmatter


class TestManifestSkillSync(unittest.TestCase):
    """Verify manifest.toml fields match SKILL.md frontmatter for every skill."""

    _skills: list[Path] = []

    @classmethod
    def setUpClass(cls):
        cls._skills = _discover_skills()
        if not cls._skills:
            raise unittest.SkipTest("No skills found under skills/")

    def test_name_matches(self):
        """manifest.toml [skill].name must match SKILL.md frontmatter name."""
        mismatches = []
        skipped = []
        for s in self._skills:
            skill_md = s / "SKILL.md"
            if not skill_md.is_file():
                skipped.append(s.name)
                continue
            with (s / "manifest.toml").open("rb") as f:
                manifest = tomllib.load(f)
            manifest_name = manifest.get("skill", {}).get("name", "")
            fm = _parse_yaml_frontmatter(skill_md.read_text(encoding="utf-8"))
            skill_name = fm.get("name", "")
            if manifest_name != skill_name:
                mismatches.append(
                    "{dir}: manifest={m!r} vs SKILL.md={s!r}".format(
                        dir=s.name, m=manifest_name, s=skill_name,
                    )
                )
        self.assertEqual(
            mismatches, [],
            "Name mismatches:\n  " + "\n  ".join(mismatches) if mismatches else "",
        )

    def test_version_matches(self):
        """manifest.toml [skill].version must match SKILL.md frontmatter version."""
        mismatches = []
        for s in self._skills:
            skill_md = s / "SKILL.md"
            if not skill_md.is_file():
                continue
            with (s / "manifest.toml").open("rb") as f:
                manifest = tomllib.load(f)
            manifest_version = manifest.get("skill", {}).get("version", "")
            fm = _parse_yaml_frontmatter(skill_md.read_text(encoding="utf-8"))
            skill_version = fm.get("version", "")
            if str(manifest_version) != str(skill_version):
                mismatches.append(
                    "{dir}: manifest={m!r} vs SKILL.md={s!r}".format(
                        dir=s.name, m=manifest_version, s=skill_version,
                    )
                )
        self.assertEqual(
            mismatches, [],
            "Version mismatches:\n  " + "\n  ".join(mismatches) if mismatches else "",
        )

    def test_description_matches(self):
        """manifest.toml [skill].description must match SKILL.md frontmatter description."""
        mismatches = []
        for s in self._skills:
            skill_md = s / "SKILL.md"
            if not skill_md.is_file():
                continue
            with (s / "manifest.toml").open("rb") as f:
                manifest = tomllib.load(f)
            manifest_desc = manifest.get("skill", {}).get("description", "")
            fm = _parse_yaml_frontmatter(skill_md.read_text(encoding="utf-8"))
            skill_desc = fm.get("description", "")
            if manifest_desc != skill_desc:
                mismatches.append(
                    "{dir}:\n    manifest: {m!r}\n    SKILL.md: {s!r}".format(
                        dir=s.name, m=manifest_desc, s=skill_desc,
                    )
                )
        self.assertEqual(
            mismatches, [],
            "Description mismatches:\n  " + "\n  ".join(mismatches) if mismatches else "",
        )


if __name__ == "__main__":
    unittest.main()
