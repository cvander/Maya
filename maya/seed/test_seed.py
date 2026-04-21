"""Tests for the Maya seed generator."""

import os
import re
import shutil
import tempfile
import unittest

from maya.seed.main import generate, dry_run, list_types
from maya.seed.templates import TEMPLATES


# All files the seed generator should create
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

BAR_TYPES = ["dive-bar", "cocktail-lounge", "sports-bar", "wine-bar"]

# Regex for a markdown table row: | something | something | ... |
TABLE_ROW_RE = re.compile(r"^\|.*\|$")
# Regex for a markdown table separator: |---|---|...|
TABLE_SEP_RE = re.compile(r"^\|[-| :]+\|$")


class TestListTypes(unittest.TestCase):
    """Test --list-types functionality."""

    def test_list_types_returns_all_four(self):
        types = list_types()
        names = [name for name, _ in types]
        for bt in BAR_TYPES:
            self.assertIn(bt, names)

    def test_list_types_has_descriptions(self):
        types = list_types()
        for name, desc in types:
            self.assertTrue(len(desc) > 0, "Description empty for {}".format(name))


class TestDryRun(unittest.TestCase):
    """Test --dry-run functionality."""

    def test_dry_run_lists_all_expected_files(self):
        for bar_type in BAR_TYPES:
            with self.subTest(bar_type=bar_type):
                paths = dry_run(bar_type, "/tmp/test")
                basenames = [p.replace("/tmp/test/", "") for p in paths]
                for expected in EXPECTED_FILES:
                    self.assertIn(expected, basenames,
                                  "Missing {} in dry run for {}".format(expected, bar_type))

    def test_dry_run_does_not_write_files(self):
        tmpdir = tempfile.mkdtemp()
        try:
            dry_run("dive-bar", tmpdir)
            # The output dir should still be empty
            contents = os.listdir(tmpdir)
            self.assertEqual(contents, [],
                             "Dry run wrote files: {}".format(contents))
        finally:
            shutil.rmtree(tmpdir)

    def test_dry_run_unknown_type_raises(self):
        with self.assertRaises(ValueError):
            dry_run("tiki-bar", "/tmp/test")


class TestGenerate(unittest.TestCase):
    """Test actual file generation for each bar type."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def test_unknown_type_raises(self):
        with self.assertRaises(ValueError):
            generate("tiki-bar", self.tmpdir)

    def _test_bar_type_generates_all_files(self, bar_type):
        """Helper: verify all expected files are created for a bar type."""
        files = generate(bar_type, self.tmpdir)
        self.assertEqual(len(files), len(EXPECTED_FILES),
                         "Wrong file count for {}".format(bar_type))
        for expected in EXPECTED_FILES:
            full_path = os.path.join(self.tmpdir, expected)
            self.assertTrue(os.path.exists(full_path),
                            "Missing {} for {}".format(expected, bar_type))
            # File should not be empty
            size = os.path.getsize(full_path)
            self.assertGreater(size, 0,
                               "Empty file {} for {}".format(expected, bar_type))

    def test_dive_bar_generates_all_files(self):
        self._test_bar_type_generates_all_files("dive-bar")

    def test_cocktail_lounge_generates_all_files(self):
        self._test_bar_type_generates_all_files("cocktail-lounge")

    def test_sports_bar_generates_all_files(self):
        self._test_bar_type_generates_all_files("sports-bar")

    def test_wine_bar_generates_all_files(self):
        self._test_bar_type_generates_all_files("wine-bar")


class TestMarkdownTables(unittest.TestCase):
    """Test that generated files contain valid markdown tables."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def _find_tables(self, content):
        """Find all markdown tables in content. Returns list of (header, separator, rows)."""
        lines = content.split("\n")
        tables = []
        i = 0
        while i < len(lines) - 1:
            # A table starts with a header row followed by a separator row
            if TABLE_ROW_RE.match(lines[i].strip()) and i + 1 < len(lines) and TABLE_SEP_RE.match(lines[i + 1].strip()):
                header = lines[i].strip()
                separator = lines[i + 1].strip()
                rows = []
                j = i + 2
                while j < len(lines) and TABLE_ROW_RE.match(lines[j].strip()):
                    rows.append(lines[j].strip())
                    j += 1
                tables.append((header, separator, rows))
                i = j
            else:
                i += 1
        return tables

    def test_inventory_files_have_valid_tables(self):
        """Verify inventory files contain properly formatted markdown tables."""
        for bar_type in BAR_TYPES:
            generate(bar_type, self.tmpdir)
            for inv_file in ["docs/inventory/beer.md", "docs/inventory/spirits.md", "docs/inventory/wine.md"]:
                with self.subTest(bar_type=bar_type, file=inv_file):
                    path = os.path.join(self.tmpdir, inv_file)
                    with open(path) as f:
                        content = f.read()
                    tables = self._find_tables(content)
                    self.assertGreater(len(tables), 0,
                                       "No tables in {} for {}".format(inv_file, bar_type))
                    for header, sep, rows in tables:
                        # Column count should match between header, separator, and rows
                        header_cols = len(header.split("|"))
                        sep_cols = len(sep.split("|"))
                        self.assertEqual(header_cols, sep_cols,
                                         "Column mismatch in {} for {}".format(inv_file, bar_type))
                        for row in rows:
                            row_cols = len(row.split("|"))
                            self.assertEqual(row_cols, header_cols,
                                             "Row column mismatch in {} for {}: {}".format(
                                                 inv_file, bar_type, row))
            # Clean up for next bar type
            shutil.rmtree(self.tmpdir)
            self.tmpdir = tempfile.mkdtemp()

    def test_schedule_has_valid_table(self):
        """Verify schedule files have properly formatted markdown tables."""
        for bar_type in BAR_TYPES:
            generate(bar_type, self.tmpdir)
            for sched_file in ["docs/schedule/current.md", "docs/schedule/staff.md"]:
                with self.subTest(bar_type=bar_type, file=sched_file):
                    path = os.path.join(self.tmpdir, sched_file)
                    with open(path) as f:
                        content = f.read()
                    tables = self._find_tables(content)
                    self.assertGreater(len(tables), 0,
                                       "No tables in {} for {}".format(sched_file, bar_type))
            shutil.rmtree(self.tmpdir)
            self.tmpdir = tempfile.mkdtemp()


class TestBarTypePersonalities(unittest.TestCase):
    """Test that each bar type has distinct personality traits."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def _read_file(self, bar_type, relpath):
        generate(bar_type, self.tmpdir)
        path = os.path.join(self.tmpdir, relpath)
        with open(path) as f:
            return f.read()

    def test_dive_bar_has_no_cocktail_menu(self):
        content = self._read_file("dive-bar", "docs/menu/current.md")
        self.assertNotIn("### Old Fashioned", content)
        self.assertNotIn("### Daiquiri", content)

    def test_cocktail_lounge_has_cocktails(self):
        shutil.rmtree(self.tmpdir)
        self.tmpdir = tempfile.mkdtemp()
        content = self._read_file("cocktail-lounge", "docs/menu/current.md")
        self.assertIn("### Old Fashioned", content)
        self.assertIn("### Daiquiri", content)
        self.assertIn("### Last Word", content)

    def test_sports_bar_has_food(self):
        shutil.rmtree(self.tmpdir)
        self.tmpdir = tempfile.mkdtemp()
        content = self._read_file("sports-bar", "docs/menu/current.md")
        self.assertIn("Wings", content)
        self.assertIn("Nachos", content)

    def test_wine_bar_has_extensive_wine_list(self):
        shutil.rmtree(self.tmpdir)
        self.tmpdir = tempfile.mkdtemp()
        content = self._read_file("wine-bar", "docs/inventory/wine.md")
        # Wine bar should have significantly more wines than other types
        self.assertIn("Scribe Winery", content)
        self.assertIn("Ridge Vineyards", content)
        self.assertIn("Hirsch Vineyards", content)
        self.assertIn("Flight", self._read_file_cached("wine-bar", "docs/menu/current.md"))

    def _read_file_cached(self, bar_type, relpath):
        """Read a file that was already generated (no re-generation)."""
        path = os.path.join(self.tmpdir, relpath)
        with open(path) as f:
            return f.read()


class TestDoesNotModifyExistingDocs(unittest.TestCase):
    """Verify the generator writes to the specified output dir, not the project root."""

    def test_generates_to_temp_dir(self):
        tmpdir = tempfile.mkdtemp()
        try:
            files = generate("dive-bar", tmpdir)
            for f in files:
                self.assertTrue(str(f).startswith(tmpdir),
                                "File {} not under tmpdir {}".format(f, tmpdir))
        finally:
            shutil.rmtree(tmpdir)


if __name__ == "__main__":
    unittest.main()
