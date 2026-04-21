"""cost-analysis -- Calculate pour costs and margins from menu and inventory data."""

from __future__ import annotations

import re
from pathlib import Path

from skills._lib import MAYA_ROOT, io, log, md_table
from skills._lib.result import Result


_HIGH_POUR_COST_THRESHOLD = 0.30  # 30%
_LOW_MARGIN_THRESHOLD = 8.0  # $8


def _parse_price(val: str) -> float | None:
    """Parse a price string like '$14', '$8-10', '$12-14' into a float.

    For ranges, returns the midpoint.
    """
    if not val:
        return None
    val = val.strip().replace(",", "")
    # Range pattern: $8-10 or $12-14
    range_match = re.match(r"\$?([\d.]+)\s*-\s*\$?([\d.]+)", val)
    if range_match:
        low = float(range_match.group(1))
        high = float(range_match.group(2))
        return (low + high) / 2.0
    # Single value: $14
    single_match = re.match(r"\$?([\d.]+)", val)
    if single_match:
        return float(single_match.group(1))
    return None


def _parse_cocktails(text: str) -> list[dict]:
    """Parse cocktail recipes from current.md format.

    Each cocktail has: ### Name, ingredients, **Price:** $X
    """
    items = []
    current_name = None
    current_price = None
    ingredients = []

    for line in text.splitlines():
        h3_match = re.match(r"^###\s+(.+)", line)
        if h3_match:
            # Save previous cocktail
            if current_name and current_price is not None:
                items.append({
                    "name": current_name,
                    "category": "cocktails",
                    "price": current_price,
                    "ingredients": ingredients,
                })
            current_name = h3_match.group(1).strip()
            current_price = None
            ingredients = []
            continue

        price_match = re.match(r"\*\*Price:\*\*\s*\$?([\d.]+)", line)
        if price_match and current_name:
            current_price = float(price_match.group(1))
            continue

        # Ingredient line: - 2 oz bourbon (Evan Williams BiB, house pour)
        ingr_match = re.match(
            r"^-\s+([\d.]+(?:\s*-\s*[\d.]+)?)\s+oz\s+(.+)", line
        )
        if ingr_match and current_name:
            oz_str = ingr_match.group(1).strip()
            # Handle ranges like "2-3"
            if "-" in oz_str:
                parts = oz_str.split("-")
                oz = (float(parts[0]) + float(parts[1])) / 2.0
            else:
                oz = float(oz_str)
            spirit = ingr_match.group(2).strip()
            ingredients.append({"spirit": spirit, "oz": oz})

    # Save last cocktail
    if current_name and current_price is not None:
        items.append({
            "name": current_name,
            "category": "cocktails",
            "price": current_price,
            "ingredients": ingredients,
        })

    return items


def _extract_section(text: str, heading: str) -> str:
    """Extract text under a ## heading until the next ## or end of file."""
    lines = text.splitlines()
    in_section = False
    section_lines = []
    for line in lines:
        if re.match(r"^##\s+" + re.escape(heading), line):
            in_section = True
            continue
        if in_section and re.match(r"^##\s+", line):
            break
        if in_section:
            section_lines.append(line)
    return "\n".join(section_lines)


def _parse_category_menu(text: str, heading: str, category: str) -> list[dict]:
    """Parse pricing from a specific menu section's table."""
    section = _extract_section(text, heading)
    items = []
    for table in md_table.parse_tables(section):
        for row in table:
            what = row.get("what", "").strip()
            price = _parse_price(row.get("price", ""))
            if what and price is not None:
                items.append({
                    "name": what,
                    "category": category,
                    "price": price,
                })
    return items


def _parse_spirits_menu(text: str) -> list[dict]:
    """Parse spirits pricing from the Spirits section of the menu."""
    section = _extract_section(text, "Spirits (Neat/Rocks)")
    items = []
    for table in md_table.parse_tables(section):
        for row in table:
            tier = row.get("tier", "").strip()
            price = _parse_price(row.get("price", ""))
            if tier and price is not None:
                items.append({
                    "name": tier,
                    "category": "spirits",
                    "price": price,
                })
    return items


def _get_spirit_costs(text: str) -> dict[str, float]:
    """Parse spirit bottle costs from inventory files.

    Returns dict mapping lowercase brand name to cost per oz.
    Assumes 750ml = ~25.4 oz and uses the price column if available.
    """
    costs = {}
    for table in md_table.parse_tables(text):
        for row in table:
            brand = row.get("brand", "").strip().lower()
            price_str = row.get("price", "").strip()
            if not brand or not price_str:
                continue
            price = _parse_price(price_str)
            if price is not None:
                # Bottle price / ~25.4 oz per 750ml
                costs[brand] = price / 25.4
    return costs


def _estimate_cocktail_cost(
    ingredients: list[dict], spirit_costs: dict[str, float]
) -> float | None:
    """Estimate total pour cost for a cocktail based on ingredient oz and spirit costs.

    Uses a default cost of $0.50/oz for spirits without known costs (well tier).
    """
    total = 0.0
    for ingr in ingredients:
        oz = ingr["oz"]
        spirit_name = ingr["spirit"].lower()

        # Try to match against known costs
        matched = False
        for brand, cost_per_oz in spirit_costs.items():
            if brand in spirit_name or spirit_name in brand:
                total += oz * cost_per_oz
                matched = True
                break

        if not matched:
            # Default well spirit cost: ~$25/750ml = ~$1.00/oz
            total += oz * 1.00

    # Add modifier costs (bitters, garnish, etc.) as flat estimate
    total += 0.50

    return round(total, 2)


def run(ctx: object) -> Result:
    """Main skill entry point."""
    log.event("cost_analysis.started")

    args = ctx.args
    category = args.category

    menu_file_arg = getattr(args, "menu_file", None)
    inventory_dir_arg = args.inventory_dir
    if inventory_dir_arg:
        inventory_dir = Path(inventory_dir_arg)
    else:
        inventory_dir = MAYA_ROOT / "docs" / "inventory"

    if menu_file_arg:
        menu_path = Path(menu_file_arg)
        menu_root = menu_path.parent
    else:
        menu_path = MAYA_ROOT / "docs" / "menu" / "current.md"
        menu_root = MAYA_ROOT / "docs"

    # Read menu
    resolved_menu = io.read_allowed_path(menu_path, allowlist_root=menu_root)
    if resolved_menu is None:
        log.event("cost_analysis.menu_missing")
        return {
            "skill": "cost-analysis",
            "status": "fail",
            "summary": "Menu file not found: docs/menu/current.md",
            "data": {},
            "findings": [],
            "metrics": {},
        }

    menu_text = resolved_menu.read_text(encoding="utf-8")

    # Read inventory files for cost data
    spirit_costs = {}
    inv_root = inventory_dir if inventory_dir_arg else MAYA_ROOT / "docs"
    for inv_file in ["spirits.md", "wine.md", "beer.md"]:
        inv_path = inventory_dir / inv_file
        resolved_inv = io.read_allowed_path(inv_path, allowlist_root=inv_root)
        if resolved_inv is not None:
            inv_text = resolved_inv.read_text(encoding="utf-8")
            spirit_costs.update(_get_spirit_costs(inv_text))

    # Parse menu items by category
    all_items = []

    if category in ("all", "cocktails"):
        all_items.extend(_parse_cocktails(menu_text))

    if category in ("all", "beer"):
        all_items.extend(_parse_category_menu(menu_text, "Beer", "beer"))

    if category in ("all", "wine"):
        all_items.extend(_parse_category_menu(menu_text, "Wine", "wine"))

    if category in ("all", "spirits"):
        all_items.extend(_parse_spirits_menu(menu_text))

    # Calculate costs and margins
    findings = []
    analyzed_items = []

    for item in all_items:
        price = item["price"]
        cost = None
        pour_cost_pct = None
        margin = None

        if item["category"] == "cocktails" and "ingredients" in item:
            cost = _estimate_cocktail_cost(item["ingredients"], spirit_costs)
            if cost is not None:
                pour_cost_pct = round(cost / price, 4) if price > 0 else None
                margin = round(price - cost, 2)
        elif item["category"] == "spirits":
            # For neat/rocks pours: 2 oz standard
            # Use average cost for the tier
            cost = round(2.0 * 1.00, 2)  # default $1/oz for well
            pour_cost_pct = round(cost / price, 4) if price > 0 else None
            margin = round(price - cost, 2)
        elif item["category"] in ("beer", "wine"):
            # Rough COGS estimate: 25-30% of price for beer/wine
            cost = round(price * 0.28, 2)
            pour_cost_pct = 0.28
            margin = round(price - cost, 2)

        entry = {
            "name": item["name"],
            "category": item["category"],
            "price": price,
            "estimated_cost": cost,
            "pour_cost_pct": pour_cost_pct,
            "margin": margin,
        }
        analyzed_items.append(entry)

        # Check thresholds
        if pour_cost_pct is not None and pour_cost_pct > _HIGH_POUR_COST_THRESHOLD:
            findings.append({
                "severity": "warn",
                "code": "HIGH_POUR_COST",
                "subject": "{cat}/{name}".format(cat=item["category"], name=item["name"]),
                "message": "{name}: pour cost {pct:.0%} exceeds {threshold:.0%} threshold.".format(
                    name=item["name"],
                    pct=pour_cost_pct,
                    threshold=_HIGH_POUR_COST_THRESHOLD,
                ),
            })

        if margin is not None and margin < _LOW_MARGIN_THRESHOLD:
            findings.append({
                "severity": "warn",
                "code": "LOW_MARGIN",
                "subject": "{cat}/{name}".format(cat=item["category"], name=item["name"]),
                "message": "{name}: margin ${margin:.2f} below ${threshold:.2f} threshold.".format(
                    name=item["name"],
                    margin=margin,
                    threshold=_LOW_MARGIN_THRESHOLD,
                ),
            })

    status = "warn" if findings else "ok"
    summary = "{count} item(s) analyzed, {findings} finding(s).".format(
        count=len(analyzed_items),
        findings=len(findings),
    )

    data = {
        "items_analyzed": len(analyzed_items),
        "category_filter": category,
        "items": analyzed_items,
    }

    log.event(
        "cost_analysis.finished",
        items_analyzed=len(analyzed_items),
        findings_count=len(findings),
    )

    return {
        "skill": "cost-analysis",
        "status": status,
        "summary": summary,
        "data": data,
        "findings": findings,
        "metrics": {},
    }
