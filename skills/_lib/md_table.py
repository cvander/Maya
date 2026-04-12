"""Pipe-table parser for markdown files. Stdlib only, with size caps."""

_MAX_FILE_BYTES = 262144  # 256 KB
_MAX_ROWS_PER_TABLE = 500
_MAX_CELLS_PER_ROW = 20


def _is_separator_row(line: str) -> bool:
    """Check if a line is a markdown table separator (e.g. |---|---|)."""
    cells = line.strip().strip("|").split("|")
    return all(c.strip().replace("-", "") == "" for c in cells)


def _parse_row(line: str, max_cells: int) -> list[str]:
    """Split a pipe-delimited row into stripped cell values."""
    stripped = line.strip()
    if stripped.startswith("|"):
        stripped = stripped[1:]
    if stripped.endswith("|"):
        stripped = stripped[:-1]
    cells = stripped.split("|")
    return [c.strip() for c in cells[:max_cells]]


def parse_tables(text: str) -> list[list[dict[str, str]]]:
    """Parse all pipe tables from markdown text.

    Returns a list of tables, where each table is a list of row dicts
    keyed by lowercased, stripped header names.

    Caps: 262144 bytes max input, 500 rows max per table, 20 cells max per row.
    Malformed tables are skipped silently.
    """
    if len(text.encode("utf-8")) > _MAX_FILE_BYTES:
        return []

    lines = text.split("\n")
    tables: list[list[dict[str, str]]] = []
    i = 0

    while i < len(lines):
        line = lines[i]
        # Look for a potential header row
        if "|" not in line:
            i += 1
            continue

        cells = _parse_row(line, _MAX_CELLS_PER_ROW)
        if len(cells) < 2:
            i += 1
            continue

        # Next line must be a separator
        if i + 1 >= len(lines) or not _is_separator_row(lines[i + 1]):
            i += 1
            continue

        headers = [c.lower().strip() for c in cells]
        i += 2  # skip header + separator

        rows: list[dict[str, str]] = []
        while i < len(lines) and len(rows) < _MAX_ROWS_PER_TABLE:
            row_line = lines[i]
            if "|" not in row_line:
                break
            if _is_separator_row(row_line):
                i += 1
                continue
            row_cells = _parse_row(row_line, _MAX_CELLS_PER_ROW)
            row_dict = {}
            for idx, header in enumerate(headers):
                if idx < len(row_cells):
                    row_dict[header] = row_cells[idx]
                else:
                    row_dict[header] = ""
            rows.append(row_dict)
            i += 1

        if rows:
            tables.append(rows)
        # Don't increment i here; the while loop will re-check current line

    return tables
