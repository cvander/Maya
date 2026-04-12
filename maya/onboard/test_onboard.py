"""Tests for the onboarding wizard (non-interactive mode only)."""

import json
import os
import tempfile
import unittest
from pathlib import Path

from maya.onboard.questions import (
    validate_bar_name,
    validate_bar_type,
    validate_date,
    validate_time,
    validate_currency,
    validate_level,
    validate_role,
    validate_music_policy,
    validate_answers,
    validate_staff_entry,
    validate_spirit_entry,
)
from maya.onboard.generator import Generator
from maya.onboard.main import run_non_interactive


# -- Fixtures --

COMPLETE_ANSWERS = {
    "bar_name": "The Rusty Nail",
    "bar_type": "dive-bar",
    "address": "123 Mission St, SF",
    "license_type": "Type 48",
    "hours": {"open": "16:00", "close": "02:00", "days": "Mon-Sun"},
    "staff": [
        {"name": "Alex", "role": "bartender", "max_hours": 40, "rbs_cert": True, "rbs_expiry": "2027-01-15"},
        {"name": "Jordan", "role": "barback", "max_hours": 25, "rbs_cert": False, "rbs_expiry": ""},
        {"name": "Sam", "role": "manager", "max_hours": 45, "rbs_cert": True, "rbs_expiry": "2027-06-01"},
    ],
    "vendors": [
        {
            "name": "Bay Area Distributors",
            "type": "distributor",
            "rep": "Mike",
            "phone": "415-555-0100",
            "email": "mike@bad.com",
            "account": "BAD-001",
            "categories": ["beer", "spirits"],
        },
        {
            "name": "Local Brewery Co",
            "type": "brewery",
            "rep": "Sarah",
            "phone": "415-555-0200",
            "email": "sarah@lbc.com",
            "account": "LBC-042",
            "categories": ["beer"],
        },
    ],
    "beer": [
        {"brewery": "Local Brew", "name": "Session IPA", "style": "IPA", "format": "1/2 bbl", "qty": 2, "reorder_at": 1, "par": 3},
        {"brewery": "Anchor", "name": "Steam", "style": "California Common", "format": "1/6 bbl", "qty": 1, "reorder_at": 1, "par": 2},
    ],
    "spirits": [
        {"category": "Bourbon", "brand": "House Pour", "size": "750ml", "qty": 3, "level": 0.5, "reorder_at": 2, "par": 4},
        {"category": "Vodka", "brand": "Smirnoff", "size": "1L", "qty": 2, "level": 0.75, "reorder_at": 1, "par": 3},
    ],
    "wine": [
        {"producer": "Local Winery", "name": "House Red", "type": "Red", "qty": 2, "reorder_at": 1, "par": 3, "price": 12},
    ],
    "menu": [
        {"name": "Old Fashioned", "category": "cocktail", "price": 12, "description": "Bourbon, sugar, bitters"},
        {"name": "House IPA", "category": "beer", "price": 7, "description": "Local Brew Session IPA on tap"},
        {"name": "House Red", "category": "wine", "price": 12, "description": "By the glass"},
        {"name": "Club Soda", "category": "non-alc", "price": 3, "description": ""},
    ],
    "music_policy": "jukebox",
    "compliance_dates": {
        "pest_inspection": "2026-03-15",
        "health_inspection": "2026-02-01",
        "fire_inspection": "2026-01-10",
    },
}

MINIMAL_ANSWERS = {
    "bar_name": "Tiny Bar",
    "bar_type": "dive-bar",
}

# All expected file paths (relative to output dir)
EXPECTED_FILES = [
    "docs/inventory/beer.md",
    "docs/inventory/spirits.md",
    "docs/inventory/wine.md",
    "docs/vendors/README.md",
    "docs/menu/current.md",
    "docs/operations/opening.md",
    "docs/operations/closing.md",
    "docs/compliance/cooler-temps.md",
    "docs/compliance/pest-log.md",
    "docs/compliance/incidents.md",
    "docs/compliance/staff-certs.md",
    "docs/permits/README.md",
    "docs/calendar.md",
    "docs/schedule/README.md",
    "docs/schedule/current.md",
    "docs/schedule/staff.md",
    "data/close-out/README.md",
    "data/86/README.md",
]


class TestValidators(unittest.TestCase):
    """Test individual validators."""

    def test_bar_name_valid(self):
        display, slug = validate_bar_name("The Rusty Nail")
        self.assertEqual(display, "The Rusty Nail")
        self.assertEqual(slug, "the-rusty-nail")

    def test_bar_name_special_chars(self):
        display, slug = validate_bar_name("O'Malley's #1 Bar!")
        self.assertEqual(display, "O'Malley's #1 Bar!")
        self.assertEqual(slug, "omalleys-1-bar")

    def test_bar_name_empty(self):
        with self.assertRaises(ValueError):
            validate_bar_name("")

    def test_bar_name_too_long(self):
        with self.assertRaises(ValueError):
            validate_bar_name("x" * 65)

    def test_bar_name_all_special_chars(self):
        with self.assertRaises(ValueError):
            validate_bar_name("!!!###")

    def test_bar_name_path_traversal(self):
        """Bar name with path traversal attempts should be sanitized."""
        display, slug = validate_bar_name("../../../etc/passwd")
        # The slug should not contain path separators
        self.assertNotIn("/", slug)
        self.assertNotIn("\\", slug)
        self.assertNotIn("..", slug)

    def test_bar_type_valid(self):
        self.assertEqual(validate_bar_type("dive-bar"), "dive-bar")
        self.assertEqual(validate_bar_type("cocktail-lounge"), "cocktail-lounge")

    def test_bar_type_invalid(self):
        with self.assertRaises(ValueError):
            validate_bar_type("nightclub")

    def test_date_valid(self):
        self.assertEqual(validate_date("2026-03-15"), "2026-03-15")

    def test_date_invalid_format(self):
        with self.assertRaises(ValueError):
            validate_date("03/15/2026")

    def test_date_invalid_date(self):
        with self.assertRaises(ValueError):
            validate_date("2026-13-01")

    def test_date_empty(self):
        self.assertEqual(validate_date(""), "")

    def test_time_valid(self):
        self.assertEqual(validate_time("16:00"), "16:00")
        self.assertEqual(validate_time("02:00"), "02:00")

    def test_time_invalid(self):
        with self.assertRaises(ValueError):
            validate_time("4pm")

    def test_time_out_of_range(self):
        with self.assertRaises(ValueError):
            validate_time("25:00")

    def test_currency_valid(self):
        self.assertEqual(validate_currency(12), 12.0)
        self.assertEqual(validate_currency("12.50"), 12.5)
        self.assertEqual(validate_currency("$7"), 7.0)

    def test_currency_invalid(self):
        with self.assertRaises(ValueError):
            validate_currency("free")

    def test_currency_negative(self):
        with self.assertRaises(ValueError):
            validate_currency(-5)

    def test_level_valid(self):
        for v in (0, 0.25, 0.5, 0.75, 1.0):
            self.assertEqual(validate_level(v), v)

    def test_level_invalid(self):
        with self.assertRaises(ValueError):
            validate_level(0.3)
        with self.assertRaises(ValueError):
            validate_level(2.0)

    def test_role_valid(self):
        self.assertEqual(validate_role("bartender"), "bartender")
        self.assertEqual(validate_role("Barback"), "barback")

    def test_role_invalid(self):
        with self.assertRaises(ValueError):
            validate_role("DJ")

    def test_music_policy_valid(self):
        self.assertEqual(validate_music_policy("jukebox"), "jukebox")
        self.assertEqual(validate_music_policy("Live Music"), "live music")

    def test_music_policy_invalid(self):
        with self.assertRaises(ValueError):
            validate_music_policy("spotify")

    def test_staff_entry_bartender_needs_rbs(self):
        with self.assertRaises(ValueError) as ctx:
            validate_staff_entry({"name": "Test", "role": "bartender", "max_hours": 40, "rbs_cert": False})
        self.assertIn("RBS", str(ctx.exception))

    def test_spirit_entry_bad_level(self):
        with self.assertRaises(ValueError) as ctx:
            validate_spirit_entry({"category": "Bourbon", "brand": "Test", "level": 0.3, "qty": 1, "reorder_at": 1, "par": 2})
        self.assertIn("Level", str(ctx.exception))


class TestValidateAnswers(unittest.TestCase):
    """Test full answer validation."""

    def test_complete_answers_valid(self):
        errors = validate_answers(COMPLETE_ANSWERS)
        self.assertEqual(errors, [])

    def test_minimal_answers_valid(self):
        errors = validate_answers(MINIMAL_ANSWERS)
        self.assertEqual(errors, [])

    def test_missing_bar_name(self):
        errors = validate_answers({"bar_type": "dive-bar"})
        self.assertTrue(any("bar_name" in e for e in errors))

    def test_missing_bar_type(self):
        errors = validate_answers({"bar_name": "Test"})
        self.assertTrue(any("bar_type" in e for e in errors))

    def test_bad_spirit_level(self):
        answers = dict(MINIMAL_ANSWERS)
        answers["spirits"] = [{"category": "X", "brand": "Y", "level": 0.3, "qty": 1, "reorder_at": 1, "par": 2}]
        errors = validate_answers(answers)
        self.assertTrue(any("spirits" in e for e in errors))

    def test_bad_date_in_compliance(self):
        answers = dict(MINIMAL_ANSWERS)
        answers["compliance_dates"] = {"pest_inspection": "not-a-date"}
        errors = validate_answers(answers)
        self.assertTrue(any("compliance_dates" in e for e in errors))

    def test_bad_staff_role(self):
        answers = dict(MINIMAL_ANSWERS)
        answers["staff"] = [{"name": "DJ Dave", "role": "dj", "max_hours": 20}]
        errors = validate_answers(answers)
        self.assertTrue(any("staff" in e for e in errors))


class TestGeneratorComplete(unittest.TestCase):
    """Test full generation with complete answers."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_generates_all_expected_files(self):
        gen = Generator(COMPLETE_ANSWERS)
        files = gen.generate(self.tmpdir)

        self.assertEqual(len(files), len(EXPECTED_FILES))
        for expected in EXPECTED_FILES:
            full_path = Path(self.tmpdir) / expected
            self.assertTrue(full_path.exists(), "Missing: {}".format(expected))

    def test_beer_md_has_valid_table(self):
        gen = Generator(COMPLETE_ANSWERS)
        gen.generate(self.tmpdir)

        content = (Path(self.tmpdir) / "docs" / "inventory" / "beer.md").read_text()
        self.assertIn("# Beer Inventory", content)
        self.assertIn("| # |", content)
        self.assertIn("Local Brew", content)
        self.assertIn("Session IPA", content)
        # Check table has separator row
        self.assertIn("|---|", content)

    def test_spirits_md_has_level_column(self):
        gen = Generator(COMPLETE_ANSWERS)
        gen.generate(self.tmpdir)

        content = (Path(self.tmpdir) / "docs" / "inventory" / "spirits.md").read_text()
        self.assertIn("Level", content)
        self.assertIn("0.5", content)
        self.assertIn("0.75", content)

    def test_wine_md_has_price(self):
        gen = Generator(COMPLETE_ANSWERS)
        gen.generate(self.tmpdir)

        content = (Path(self.tmpdir) / "docs" / "inventory" / "wine.md").read_text()
        self.assertIn("$12", content)
        self.assertIn("House Red", content)

    def test_vendors_md_has_entries(self):
        gen = Generator(COMPLETE_ANSWERS)
        gen.generate(self.tmpdir)

        content = (Path(self.tmpdir) / "docs" / "vendors" / "README.md").read_text()
        self.assertIn("Bay Area Distributors", content)
        self.assertIn("Local Brewery Co", content)

    def test_menu_groups_by_category(self):
        gen = Generator(COMPLETE_ANSWERS)
        gen.generate(self.tmpdir)

        content = (Path(self.tmpdir) / "docs" / "menu" / "current.md").read_text()
        self.assertIn("## Cocktails", content)
        self.assertIn("## Beer", content)
        self.assertIn("## Wine", content)
        self.assertIn("## Non-Alcoholic", content)
        self.assertIn("Old Fashioned", content)

    def test_staff_certs_has_entries(self):
        gen = Generator(COMPLETE_ANSWERS)
        gen.generate(self.tmpdir)

        content = (Path(self.tmpdir) / "docs" / "compliance" / "staff-certs.md").read_text()
        self.assertIn("Alex", content)
        self.assertIn("Active", content)
        self.assertIn("Pending", content)

    def test_permits_has_bar_name(self):
        gen = Generator(COMPLETE_ANSWERS)
        gen.generate(self.tmpdir)

        content = (Path(self.tmpdir) / "docs" / "permits" / "README.md").read_text()
        self.assertIn("The Rusty Nail", content)
        self.assertIn("Type 48", content)
        self.assertIn("123 Mission St", content)

    def test_calendar_has_compliance_dates(self):
        gen = Generator(COMPLETE_ANSWERS)
        gen.generate(self.tmpdir)

        content = (Path(self.tmpdir) / "docs" / "calendar.md").read_text()
        self.assertIn("2026-03-15", content)
        self.assertIn("2026-02-01", content)
        self.assertIn("2026-01-10", content)

    def test_opening_has_hours(self):
        gen = Generator(COMPLETE_ANSWERS)
        gen.generate(self.tmpdir)

        content = (Path(self.tmpdir) / "docs" / "operations" / "opening.md").read_text()
        self.assertIn("16:00", content)

    def test_closing_has_last_call(self):
        gen = Generator(COMPLETE_ANSWERS)
        gen.generate(self.tmpdir)

        content = (Path(self.tmpdir) / "docs" / "operations" / "closing.md").read_text()
        self.assertIn("01:30", content)
        self.assertIn("02:00", content)

    def test_schedule_staff_has_entries(self):
        gen = Generator(COMPLETE_ANSWERS)
        gen.generate(self.tmpdir)

        content = (Path(self.tmpdir) / "docs" / "schedule" / "staff.md").read_text()
        self.assertIn("Alex", content)
        self.assertIn("Bartender", content)
        self.assertIn("Jordan", content)

    def test_pest_log_has_last_inspection(self):
        gen = Generator(COMPLETE_ANSWERS)
        gen.generate(self.tmpdir)

        content = (Path(self.tmpdir) / "docs" / "compliance" / "pest-log.md").read_text()
        self.assertIn("2026-03-15", content)

    def test_markdown_tables_well_formed(self):
        """Verify all generated .md files with tables have proper separator rows."""
        gen = Generator(COMPLETE_ANSWERS)
        gen.generate(self.tmpdir)

        for expected in EXPECTED_FILES:
            if not expected.endswith(".md"):
                continue
            full_path = Path(self.tmpdir) / expected
            content = full_path.read_text()
            lines = content.split("\n")
            for i, line in enumerate(lines):
                if line.startswith("|") and i + 1 < len(lines):
                    next_line = lines[i + 1]
                    if next_line.startswith("|") and "---" in next_line:
                        # Table header followed by separator - good
                        # Verify separator has correct column count
                        header_cols = line.count("|") - 1
                        sep_cols = next_line.count("|") - 1
                        self.assertEqual(
                            header_cols, sep_cols,
                            "Column mismatch in {}: header has {}, separator has {}".format(
                                expected, header_cols, sep_cols
                            ),
                        )


class TestGeneratorMinimal(unittest.TestCase):
    """Test generation with minimal answers (only required fields)."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_generates_all_expected_files(self):
        gen = Generator(MINIMAL_ANSWERS)
        files = gen.generate(self.tmpdir)

        self.assertEqual(len(files), len(EXPECTED_FILES))
        for expected in EXPECTED_FILES:
            full_path = Path(self.tmpdir) / expected
            self.assertTrue(full_path.exists(), "Missing: {}".format(expected))

    def test_beer_md_has_empty_table(self):
        gen = Generator(MINIMAL_ANSWERS)
        gen.generate(self.tmpdir)

        content = (Path(self.tmpdir) / "docs" / "inventory" / "beer.md").read_text()
        self.assertIn("# Beer Inventory", content)
        self.assertIn("|---|", content)

    def test_staff_certs_has_empty_row(self):
        gen = Generator(MINIMAL_ANSWERS)
        gen.generate(self.tmpdir)

        content = (Path(self.tmpdir) / "docs" / "compliance" / "staff-certs.md").read_text()
        self.assertIn("| | | | | | |", content)


class TestNonInteractiveMode(unittest.TestCase):
    """Test the non-interactive CLI flow."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.answers_file = os.path.join(self.tmpdir, "answers.json")

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_non_interactive_complete(self):
        output_dir = os.path.join(self.tmpdir, "output")
        with open(self.answers_file, "w") as f:
            json.dump(COMPLETE_ANSWERS, f)

        files = run_non_interactive(self.answers_file, output_dir)
        self.assertEqual(len(files), len(EXPECTED_FILES))

    def test_non_interactive_minimal(self):
        output_dir = os.path.join(self.tmpdir, "output")
        with open(self.answers_file, "w") as f:
            json.dump(MINIMAL_ANSWERS, f)

        files = run_non_interactive(self.answers_file, output_dir)
        self.assertEqual(len(files), len(EXPECTED_FILES))

    def test_non_interactive_invalid_answers(self):
        output_dir = os.path.join(self.tmpdir, "output")
        with open(self.answers_file, "w") as f:
            json.dump({"bar_name": ""}, f)

        with self.assertRaises(ValueError):
            run_non_interactive(self.answers_file, output_dir)

    def test_non_interactive_missing_file(self):
        output_dir = os.path.join(self.tmpdir, "output")
        with self.assertRaises(FileNotFoundError):
            run_non_interactive("/nonexistent/answers.json", output_dir)


class TestBarNameSanitization(unittest.TestCase):
    """Test bar name sanitization edge cases (security requirement)."""

    def test_spaces_become_hyphens(self):
        _, slug = validate_bar_name("My Cool Bar")
        self.assertEqual(slug, "my-cool-bar")

    def test_special_chars_stripped(self):
        _, slug = validate_bar_name("Bar & Grill #1!")
        self.assertNotIn("&", slug)
        self.assertNotIn("!", slug)
        self.assertIn("bar", slug)
        self.assertIn("grill", slug)

    def test_unicode_stripped(self):
        _, slug = validate_bar_name("Cafe Soleil")
        self.assertEqual(slug, "cafe-soleil")

    def test_path_traversal_blocked(self):
        """Ensure path traversal sequences are neutralized."""
        _, slug = validate_bar_name("test..bar")
        self.assertNotIn("..", slug)

    def test_max_length(self):
        name = "A" * 64
        display, slug = validate_bar_name(name)
        self.assertEqual(len(display), 64)

    def test_over_max_length(self):
        with self.assertRaises(ValueError):
            validate_bar_name("A" * 65)


if __name__ == "__main__":
    unittest.main()
