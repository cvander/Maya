"""Eval: validate every skill's SKILL.md parses correctly with required fields."""

import re
import unittest
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[2]
SKILLS_DIR = REPO_ROOT / "skills"

# Directories to exclude (templates, shared libs)
_EXCLUDE = {"_skeleton", "_lib"}

# Skills discovered dynamically via manifest.toml
SKILL_DIRS = sorted(
    p.parent for p in SKILLS_DIR.glob("*/manifest.toml")
    if p.parent.name not in _EXCLUDE
)

REQUIRED_FRONTMATTER = {"name", "description", "version", "author", "license", "platforms"}
REQUIRED_SECTIONS = {"When to Use", "Procedure", "Verification"}


def _parse_skill_md(skill_md_path: Path) -> tuple:
    """Parse SKILL.md into (frontmatter_dict, body_str).

    Returns (None, None) if parsing fails.
    """
    text = skill_md_path.read_text(encoding="utf-8")
    # Extract YAML frontmatter between --- markers
    match = re.match(r"^---\n(.*?\n)---\n(.*)$", text, re.DOTALL)
    if not match:
        return None, None
    frontmatter_text = match.group(1)
    body = match.group(2)
    try:
        frontmatter = yaml.safe_load(frontmatter_text)
    except yaml.YAMLError:
        return None, None
    return frontmatter, body


def _extract_h2_sections(body: str) -> set:
    """Extract all ## section headings from markdown body."""
    return set(re.findall(r"^## (.+)$", body, re.MULTILINE))


class TestSkillMdValidity(unittest.TestCase):
    """Validate SKILL.md for every skill with a manifest.toml."""

    def test_all_skills_have_skill_md(self):
        """Every skill with manifest.toml should have SKILL.md."""
        missing = []
        for skill_dir in SKILL_DIRS:
            skill_md = skill_dir / "SKILL.md"
            if not skill_md.is_file():
                missing.append(skill_dir.name)
        self.assertEqual(missing, [], "Skills missing SKILL.md: {}".format(missing))

    def test_frontmatter_parses(self):
        """YAML frontmatter between --- markers parses correctly."""
        failures = []
        for skill_dir in SKILL_DIRS:
            skill_md = skill_dir / "SKILL.md"
            if not skill_md.is_file():
                continue
            fm, body = _parse_skill_md(skill_md)
            if fm is None:
                failures.append(skill_dir.name)
        self.assertEqual(failures, [], "SKILL.md frontmatter parse failures: {}".format(failures))

    def test_required_frontmatter_fields(self):
        """Required frontmatter fields are present in every SKILL.md."""
        failures = []
        for skill_dir in SKILL_DIRS:
            skill_md = skill_dir / "SKILL.md"
            if not skill_md.is_file():
                continue
            fm, _ = _parse_skill_md(skill_md)
            if fm is None:
                continue
            missing = REQUIRED_FRONTMATTER - set(fm.keys())
            if missing:
                failures.append("{}: missing {}".format(skill_dir.name, missing))
        self.assertEqual(failures, [], "Missing frontmatter fields:\n{}".format("\n".join(failures)))

    def test_hermes_metadata_exists(self):
        """metadata.hermes section exists with tags."""
        failures = []
        for skill_dir in SKILL_DIRS:
            skill_md = skill_dir / "SKILL.md"
            if not skill_md.is_file():
                continue
            fm, _ = _parse_skill_md(skill_md)
            if fm is None:
                continue
            metadata = fm.get("metadata", {})
            hermes = metadata.get("hermes", {}) if metadata else {}
            if not hermes:
                failures.append("{}: no metadata.hermes section".format(skill_dir.name))
            elif "tags" not in hermes:
                failures.append("{}: metadata.hermes missing tags".format(skill_dir.name))
            # Accept either requires_tools or requires_toolsets
            has_tools = "requires_tools" in hermes or "requires_toolsets" in hermes
            if not has_tools:
                failures.append("{}: metadata.hermes missing requires_tools/requires_toolsets".format(skill_dir.name))
        self.assertEqual(failures, [], "Hermes metadata issues:\n{}".format("\n".join(failures)))

    def test_required_sections_present(self):
        """Markdown body has required sections: When to Use, Procedure, Verification."""
        failures = []
        for skill_dir in SKILL_DIRS:
            skill_md = skill_dir / "SKILL.md"
            if not skill_md.is_file():
                continue
            _, body = _parse_skill_md(skill_md)
            if body is None:
                continue
            sections = _extract_h2_sections(body)
            missing = REQUIRED_SECTIONS - sections
            if missing:
                failures.append("{}: missing sections {}".format(skill_dir.name, missing))
        self.assertEqual(failures, [], "Missing sections:\n{}".format("\n".join(failures)))

    def test_procedure_has_python_command(self):
        """Procedure section contains a python -m skills. command."""
        failures = []
        for skill_dir in SKILL_DIRS:
            skill_md = skill_dir / "SKILL.md"
            if not skill_md.is_file():
                continue
            _, body = _parse_skill_md(skill_md)
            if body is None:
                continue
            # Extract Procedure section content (between ## Procedure and next ##)
            proc_match = re.search(
                r"## Procedure\n(.*?)(?=\n## |\Z)", body, re.DOTALL
            )
            if not proc_match:
                failures.append("{}: no Procedure section body".format(skill_dir.name))
                continue
            proc_text = proc_match.group(1)
            if "python -m skills." not in proc_text:
                failures.append("{}: Procedure missing 'python -m skills.' command".format(skill_dir.name))
        self.assertEqual(failures, [], "Procedure issues:\n{}".format("\n".join(failures)))


if __name__ == "__main__":
    unittest.main()
