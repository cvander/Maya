"""Generate docs/ and data/ tree from onboarding answers."""

from pathlib import Path

from maya.onboard.questions import validate_bar_name, validate_answers


class Generator:
    """Generates the complete docs/ + data/ file tree from user answers."""

    def __init__(self, answers):
        self.answers = answers
        errors = validate_answers(answers)
        if errors:
            raise ValueError("Invalid answers:\n  " + "\n  ".join(errors))
        display_name, slug = validate_bar_name(answers["bar_name"])
        self.display_name = display_name
        self.slug = slug

    def generate(self, output_dir):
        """Write all files to output_dir. Returns list of Path objects created."""
        output_dir = Path(output_dir)
        files = []

        files.append(self._write_beer(output_dir))
        files.append(self._write_spirits(output_dir))
        files.append(self._write_wine(output_dir))
        files.append(self._write_vendors(output_dir))
        files.append(self._write_menu(output_dir))
        files.append(self._write_opening(output_dir))
        files.append(self._write_closing(output_dir))
        files.append(self._write_cooler_temps(output_dir))
        files.append(self._write_pest_log(output_dir))
        files.append(self._write_incidents(output_dir))
        files.append(self._write_staff_certs(output_dir))
        files.append(self._write_permits(output_dir))
        files.append(self._write_calendar(output_dir))
        files.append(self._write_schedule_readme(output_dir))
        files.append(self._write_schedule_current(output_dir))
        files.append(self._write_schedule_staff(output_dir))
        files.append(self._write_closeout_readme(output_dir))
        files.append(self._write_86_readme(output_dir))

        return files

    # -- Helpers --

    def _write(self, path, content):
        """Write content to path, creating parent dirs as needed."""
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
        return path

    def _get(self, key, default=None):
        return self.answers.get(key, default)

    # -- File writers --

    def _write_beer(self, root):
        path = root / "docs" / "inventory" / "beer.md"
        lines = ["# Beer Inventory", "", "Last counted: ____-__-__", ""]

        beers = self._get("beer", [])
        if beers:
            lines.append("## Inventory")
            lines.append("")
            lines.append("| # | Brewery | Beer | Style | Format | Qty | Reorder at | Par |")
            lines.append("|---|---------|------|-------|--------|-----|------------|-----|")
            for i, b in enumerate(beers, 1):
                lines.append("| {} | {} | {} | {} | {} | {} | {} | {} |".format(
                    i, b.get("brewery", ""), b.get("name", ""),
                    b.get("style", ""), b.get("format", ""),
                    b.get("qty", ""), b.get("reorder_at", ""), b.get("par", ""),
                ))
            lines.append("")
        else:
            lines.append("## Inventory")
            lines.append("")
            lines.append("| # | Brewery | Beer | Style | Format | Qty | Reorder at | Par |")
            lines.append("|---|---------|------|-------|--------|-----|------------|-----|")
            lines.append("| | | | | | | | |")
            lines.append("")

        lines.append("## Notes")
        lines.append("")
        lines.append("- Count weekly, order Monday.")
        lines.append("- Par is the target quantity to have on hand.")
        lines.append("- Reorder when stock hits the reorder-at number.")
        lines.append("")

        return self._write(path, "\n".join(lines))

    def _write_spirits(self, root):
        path = root / "docs" / "inventory" / "spirits.md"
        lines = ["# Spirits & Bottles Inventory", "", "Last counted: ____-__-__", ""]

        spirits = self._get("spirits", [])
        if spirits:
            lines.append("## Inventory")
            lines.append("")
            lines.append("| Category | Brand | Size | Qty | Level | Reorder at | Par |")
            lines.append("|----------|-------|------|-----|-------|------------|-----|")
            for s in spirits:
                lines.append("| {} | {} | {} | {} | {} | {} | {} |".format(
                    s.get("category", ""), s.get("brand", ""),
                    s.get("size", ""), s.get("qty", ""),
                    s.get("level", ""), s.get("reorder_at", ""), s.get("par", ""),
                ))
            lines.append("")
        else:
            lines.append("## Inventory")
            lines.append("")
            lines.append("| Category | Brand | Size | Qty | Level | Reorder at | Par |")
            lines.append("|----------|-------|------|-----|-------|------------|-----|")
            lines.append("| | | | | | | |")
            lines.append("")

        lines.append("## Notes")
        lines.append("")
        lines.append("- Count weekly, order Monday.")
        lines.append("- Level is 0 to 1.0 in quarter increments (0, 0.25, 0.5, 0.75, 1.0).")
        lines.append("- Par is the target quantity to have on hand.")
        lines.append("- Reorder when stock hits the reorder-at number.")
        lines.append("")

        return self._write(path, "\n".join(lines))

    def _write_wine(self, root):
        path = root / "docs" / "inventory" / "wine.md"
        lines = ["# Wine Inventory", "", "Last counted: ____-__-__", ""]

        wines = self._get("wine", [])
        if wines:
            lines.append("## Inventory")
            lines.append("")
            lines.append("| Producer | Wine | Type | Qty | Reorder at | Par | Price |")
            lines.append("|----------|------|------|-----|------------|-----|-------|")
            for w in wines:
                price = w.get("price", "")
                if price != "" and price is not None:
                    price = "${}".format(price)
                lines.append("| {} | {} | {} | {} | {} | {} | {} |".format(
                    w.get("producer", ""), w.get("name", ""),
                    w.get("type", ""), w.get("qty", ""),
                    w.get("reorder_at", ""), w.get("par", ""), price,
                ))
            lines.append("")
        else:
            lines.append("## Inventory")
            lines.append("")
            lines.append("| Producer | Wine | Type | Qty | Reorder at | Par | Price |")
            lines.append("|----------|------|------|-----|------------|-----|-------|")
            lines.append("| | | | | | | |")
            lines.append("")

        lines.append("## Notes")
        lines.append("")
        lines.append("- Count weekly.")
        lines.append("- Par is the target quantity to have on hand.")
        lines.append("")

        return self._write(path, "\n".join(lines))

    def _write_vendors(self, root):
        path = root / "docs" / "vendors" / "README.md"
        lines = ["# Vendors", "", "Who supplies what, when to order, and who to call.", "", "---", ""]

        vendors = self._get("vendors", [])
        if vendors:
            lines.append("## Vendor List")
            lines.append("")
            lines.append("| Vendor | Type | Rep | Phone | Email | Account # | Categories |")
            lines.append("|--------|------|-----|-------|-------|-----------|------------|")
            for v in vendors:
                cats = ", ".join(v.get("categories", []))
                lines.append("| {} | {} | {} | {} | {} | {} | {} |".format(
                    v.get("name", ""), v.get("type", ""),
                    v.get("rep", ""), v.get("phone", ""),
                    v.get("email", ""), v.get("account", ""), cats,
                ))
            lines.append("")
        else:
            lines.append("## Vendor List")
            lines.append("")
            lines.append("| Vendor | Type | Rep | Phone | Email | Account # | Categories |")
            lines.append("|--------|------|-----|-------|-------|-----------|------------|")
            lines.append("| | | | | | | |")
            lines.append("")

        lines.append("## Order Workflow")
        lines.append("")
        lines.append("1. **Sunday night**: Run `python -m skills.inventory_check` to see what's low.")
        lines.append("2. **Monday morning**: Review low stock list.")
        lines.append("3. **Monday by noon**: Place distributor orders.")
        lines.append("4. **Wednesday-Friday**: Receive deliveries. Count against order. Flag shorts immediately.")
        lines.append("")

        lines.append("## Notes")
        lines.append("")
        lines.append("- Rep relationships matter. If something's allocated, the rep decides who gets it.")
        lines.append("- When a rep changes, update this file same day.")
        lines.append("- Keep order confirmations until delivery is verified.")
        lines.append("- Dispute shorts within 24 hours or lose the claim.")
        lines.append("")

        return self._write(path, "\n".join(lines))

    def _write_menu(self, root):
        path = root / "docs" / "menu" / "current.md"
        lines = ["# Current Menu", "", "Last updated: ____-__-__", "", "---", ""]

        menu = self._get("menu", [])
        if menu:
            # Group by category
            categories = {}
            for item in menu:
                cat = item.get("category", "other")
                categories.setdefault(cat, []).append(item)

            cat_labels = {
                "cocktail": "Cocktails",
                "beer": "Beer",
                "wine": "Wine",
                "non-alc": "Non-Alcoholic",
            }

            for cat_key in ("cocktail", "beer", "wine", "non-alc"):
                items = categories.get(cat_key, [])
                if items:
                    lines.append("## {}".format(cat_labels.get(cat_key, cat_key)))
                    lines.append("")
                    lines.append("| Item | Price | Description |")
                    lines.append("|------|-------|-------------|")
                    for item in items:
                        price = item.get("price", "")
                        if price != "" and price is not None:
                            price = "${}".format(price)
                        lines.append("| {} | {} | {} |".format(
                            item.get("name", ""), price,
                            item.get("description", ""),
                        ))
                    lines.append("")
        else:
            lines.append("## Menu")
            lines.append("")
            lines.append("| Item | Category | Price | Description |")
            lines.append("|------|----------|-------|-------------|")
            lines.append("| | | | |")
            lines.append("")

        lines.append("---")
        lines.append("")
        lines.append("## How the Menu Changes")
        lines.append("")
        lines.append("- Buy-outs go on special until gone.")
        lines.append("- Seasonal changes when it makes sense.")
        lines.append("- If it doesn't sell, it comes off.")
        lines.append("")

        return self._write(path, "\n".join(lines))

    def _write_opening(self, root):
        path = root / "docs" / "operations" / "opening.md"
        hours = self._get("hours", {})
        open_time = hours.get("open", "____") if hours else "____"

        lines = [
            "# Opening Checklist",
            "",
            "Run through this before the doors open. Every shift, no exceptions.",
            "",
            "---",
            "",
            "## Behind the Bar",
            "",
            "- [ ] Ice bins filled",
            "- [ ] Garnish prep: lemons, limes, oranges",
            "- [ ] Glassware polished and staged",
            "- [ ] Speed rail stocked and in order",
            "- [ ] Draft lines -- pull a short pour from each tap, check for off flavors",
            "- [ ] Bottle count -- eyeball the well, pull backups for anything below 1/4",
            "",
            "## Front of House",
            "",
            "- [ ] Tables wiped, chairs set",
            "- [ ] Floor swept/mopped",
            "- [ ] Bathrooms checked (soap, paper, clean)",
            "- [ ] Music on, volume appropriate",
            "- [ ] Lighting set",
            "- [ ] Menu boards updated if anything changed or is 86'd",
            "",
            "## Cash & Systems",
            "",
            "- [ ] POS powered on, test transaction",
            "- [ ] Cash drawer counted, starting bank verified",
            "- [ ] Card reader tested",
            "- [ ] Tabs from last night -- any still open?",
            "",
            "## Compliance",
            "",
            "- [ ] Liquor license visible behind bar",
            "- [ ] Health permit visible near entrance",
            "- [ ] Fire exit clear, not blocked",
            "- [ ] ID check supplies ready",
            "",
        ]

        music = self._get("music_policy", "")
        if music:
            lines.append("## {} Specifics".format(self.display_name))
            lines.append("")
            if music == "live music":
                lines.append("- [ ] Sound system tested")
                lines.append("- [ ] Stage area clear and ready")
            elif music == "jukebox":
                lines.append("- [ ] Jukebox powered on and tested")
            lines.append("")

        lines.append("## 86 List")
        lines.append("")
        lines.append("Update and post visibly for all staff:")
        lines.append("")
        lines.append("| Item | Reason | ETA Back |")
        lines.append("|------|--------|----------|")
        lines.append("| | | |")
        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append("**Time target**: 30-45 minutes before doors open ({}).".format(open_time))
        lines.append("**Who**: Opening bartender.")
        lines.append("")

        return self._write(path, "\n".join(lines))

    def _write_closing(self, root):
        path = root / "docs" / "operations" / "closing.md"
        hours = self._get("hours", {})
        close_time = hours.get("close", "02:00") if hours else "02:00"

        # Calculate last call (30 min before close)
        try:
            ch, cm = int(close_time[:2]), int(close_time[3:])
            total_min = ch * 60 + cm - 30
            if total_min < 0:
                total_min += 24 * 60
            lc_h = total_min // 60
            lc_m = total_min % 60
            last_call = "{:02d}:{:02d}".format(lc_h, lc_m)
        except (ValueError, IndexError):
            last_call = "1:30 AM"

        lines = [
            "# Closing Checklist",
            "",
            "Last call is at {}. Doors locked at {}. This gets done before anyone leaves.".format(last_call, close_time),
            "",
            "---",
            "",
            "## Cash Out",
            "",
            "- [ ] Close all open tabs",
            "- [ ] Run POS end-of-day report",
            "- [ ] Count cash drawer",
            "- [ ] Record: starting bank, cash sales, credit sales, tips, variance",
            "- [ ] Drop cash in safe",
            "- [ ] Note any discrepancies",
            "",
            "## Bar Breakdown",
            "",
            "- [ ] Wash all glassware, run through sanitizer",
            "- [ ] Wipe down bar top, speed rail, back bar",
            "- [ ] Empty ice wells, wipe and leave to dry",
            "- [ ] Cap or cork all open bottles",
            "- [ ] Refrigerate vermouth, wine, and anything perishable",
            "- [ ] Restock beer cooler from back stock",
            "- [ ] Dump garnish trays, wash containers",
            "",
            "## Front of House",
            "",
            "- [ ] Chairs up on tables",
            "- [ ] Floor swept and mopped",
            "- [ ] Bathrooms: final check, lights off",
            "- [ ] Trash out -- all bins",
            "- [ ] Recycling sorted (glass separate)",
            "",
            "## Security",
            "",
            "- [ ] Back door locked",
            "- [ ] Windows secured",
            "- [ ] Alarm set (if applicable)",
            "- [ ] Front door locked, key accounted for",
            "",
            "## Shift Notes",
            "",
            "```",
            "Date: ____-__-__",
            "Bartender: ________________",
            "",
            "What happened tonight:",
            "",
            "",
            "What's 86'd:",
            "",
            "",
            "What needs attention tomorrow:",
            "",
            "",
            "```",
            "",
            "---",
            "",
            "**Time target**: 30-45 minutes after last guest leaves.",
            "**Who**: Closing bartender. Nobody leaves until this is done.",
            "",
        ]

        return self._write(path, "\n".join(lines))

    def _write_cooler_temps(self, root):
        path = root / "docs" / "compliance" / "cooler-temps.md"
        lines = [
            "# Cooler Temperature Log",
            "",
            "Record temperatures daily. AM before open, PM at close. Must stay below 41F (5C). SFDPH requires this log.",
            "",
            "---",
            "",
            "## Current Week",
            "",
            "| Date | Cooler | AM Temp (F) | PM Temp (F) | Initials | Notes |",
            "|------|--------|-------------|-------------|----------|-------|",
        ]
        for _ in range(7):
            lines.append("| | Beer cooler | | | | |")
        lines.append("")
        lines.append("## Rules")
        lines.append("")
        lines.append("- If any reading is above 41F: adjust thermostat, recheck in 1 hour, note corrective action.")
        lines.append("- If still above 41F after adjustment: call refrigeration service. Do not serve product from a warm cooler.")
        lines.append("- Keep completed weeks on file for 1 year minimum.")
        lines.append("")

        return self._write(path, "\n".join(lines))

    def _write_pest_log(self, root):
        path = root / "docs" / "compliance" / "pest-log.md"
        dates = self._get("compliance_dates", {})
        last_pest = dates.get("pest_inspection", "____-__-__") if dates else "____-__-__"

        content = """# Pest Control Log

Weekly visual inspection. SFDPH requires documentation of pest monitoring.

Last professional inspection: {}

---

## Current Month

| Date | Inspector | Rodent Signs | Insect Signs | Droppings | Entry Points | Action Taken | Notes |
|------|-----------|-------------|-------------|-----------|-------------|-------------|-------|
| | | None/Found | None/Found | None/Found | None/Found | | |
| | | None/Found | None/Found | None/Found | None/Found | | |
| | | None/Found | None/Found | None/Found | None/Found | | |
| | | None/Found | None/Found | None/Found | None/Found | | |

## Inspection Areas

Check these every week:
- [ ] Behind bar (under speed rail, behind bottles)
- [ ] Storage room / back stock
- [ ] Under sinks (bar and bathroom)
- [ ] Around trash/recycling area
- [ ] Around exterior doors and vents

## If You Find Something

1. Document it in this log with specifics (what, where, how many).
2. Call pest control service: __________________ (phone: ____________)
3. Note the service visit date and what they did.
4. Re-inspect in 48 hours. Document follow-up.

## Pest Control Service

| Company | Contact | Phone | Schedule | Notes |
|---------|---------|-------|----------|-------|
| | | | Monthly preventive | |

## Rules

- Keep completed months on file for 1 year minimum.
- If SFDPH asks for your pest log, hand them this. It should be current.
""".format(last_pest)
        return self._write(path, content)

    def _write_incidents(self, root):
        path = root / "docs" / "compliance" / "incidents.md"
        content = """# Incident Log

Document anything that goes beyond a normal night. This protects you, your staff, and your license.

---

## Incidents

| Date | Time | Type | Description | Staff Present | Action Taken | Police Called | Report # |
|------|------|------|-------------|---------------|-------------|-------------|----------|
| | | | | | | Yes/No | |

## Types

- **Refusal**: Refused service to intoxicated patron
- **ID**: Fake ID confiscated or minor attempted purchase
- **Altercation**: Physical or verbal confrontation
- **Injury**: Staff or patron injury on premises
- **Theft**: Cash, product, or personal property
- **Property**: Damage to bar or patron property
- **Other**: Anything else that needs documenting

## Rules

- Write it down the same night. Memory fades, details matter.
- Be factual, not emotional.
- If police respond, get the report number.
- Keep on file indefinitely. Do not delete incident records.
"""
        return self._write(path, content)

    def _write_staff_certs(self, root):
        path = root / "docs" / "compliance" / "staff-certs.md"
        lines = [
            "# Staff Certifications",
            "",
            "California requires RBS (Responsible Beverage Service) certification for all alcohol servers.",
            "",
            "---",
            "",
            "## Current Staff",
            "",
            "| Name | Role | RBS Cert | Expires | Status | Notes |",
            "|------|------|----------|---------|--------|-------|",
        ]

        staff = self._get("staff", [])
        if staff:
            for s in staff:
                cert = "Yes" if s.get("rbs_cert") else "No"
                expiry = s.get("rbs_expiry", "--") or "--"
                status = "Active" if s.get("rbs_cert") else "Pending"
                lines.append("| {} | {} | {} | {} | {} | |".format(
                    s.get("name", ""), s.get("role", "").title(),
                    cert, expiry, status,
                ))
        else:
            lines.append("| | | | | | |")

        lines.append("")
        lines.append("## Requirements")
        lines.append("")
        lines.append("- **RBS Certification**: Mandatory for all servers/bartenders in California since July 1, 2024 (AB 1221).")
        lines.append("- **Renewal**: Every 3 years. $3 per certification.")
        lines.append("- **New hires**: Must obtain RBS within 60 days of hire.")
        lines.append("")

        return self._write(path, "\n".join(lines))

    def _write_permits(self, root):
        path = root / "docs" / "permits" / "README.md"
        license_type = self._get("license_type", "Type 48")
        address = self._get("address", "")

        address_line = ""
        if address:
            address_line = "\nAddress: {}\n".format(address)

        content = """# Permits & Licenses

All permits, licenses, and compliance documents for {bar_name}.
{address_line}
---

## Active Permits

| Permit | Issuing Authority | Number | Issued | Expires | Status | Notes |
|--------|-------------------|--------|--------|---------|--------|-------|
| Liquor License ({license}) | CA ABC | | | | Active | |
| Business License | City of SF (Treasurer) | | | | Active | Annual renewal. |
| Health Permit | SF Dept of Public Health | | | | Active | Must be displayed near entrance. |
| Fire Occupancy Permit | SFFD | | | | Active | |
| Seller's Permit | CA CDTFA | | | | Active | Sales tax collection. |
| EIN | IRS | | | | Active | Federal employer ID. |

## License Types Reference (CA ABC)

| Type | Name | Food Required | Notes |
|------|------|---------------|-------|
| 42 | On-Sale Beer and Wine | No | Beer and wine only. |
| 47 | On-Sale General, Eating Place | Yes | Full liquor, must serve meals. |
| **48** | **On-Sale General, Public Premises** | **No** | **Full liquor, no food requirement. This is a bar license.** |

## Renewal Calendar

| Permit | Renewal Date | Lead Time | Cost | Notes |
|--------|-------------|-----------|------|-------|
| Liquor License | | 60 days | ~$900/yr | Do not let this lapse. |
| Business License | | 30 days | Varies | Online renewal available. |
| Health Permit | | 30 days | ~$600/yr | SFDPH. |

## Notes

- Flag renewals to the lawyer with at least the lead time listed above.
- ABC violations go to the lawyer immediately, no exceptions.
- Keep inspection results on file for 3 years minimum.
""".format(
            bar_name=self.display_name,
            address_line=address_line,
            license=license_type,
        )
        return self._write(path, content)

    def _write_calendar(self, root):
        path = root / "docs" / "calendar.md"
        dates = self._get("compliance_dates", {})

        lines = [
            "# Special Dates Calendar",
            "",
            "Dates that affect the menu, staffing, or how the room runs.",
            "",
            "---",
            "",
            "## Annual Events",
            "",
            "| Date | Event | Impact | Notes |",
            "|------|-------|--------|-------|",
            "| Jan 1 | New Year's Day | Low volume | Late open OK. |",
            "| Feb (Super Bowl Sunday) | Super Bowl | High volume | Open early. Beer moves fast. |",
            "| March 17 | St. Patrick's Day | High volume | Irish whiskey specials, extra staff. |",
            "| June (last week) | SF Pride Week | Highest volume week | Plan 2 weeks out. Extra everything. |",
            "| July 4 | Fourth of July | Moderate | Neighborhood crowd. |",
            "| Oct 31 | Halloween | High volume | Extra staff. Long night. |",
            "| Dec 31 | New Year's Eve | Highest revenue night | Staff confirmed 2 weeks out. |",
            "",
            "## Compliance Dates",
            "",
            "| Date | What | Lead Time | Notes |",
            "|------|------|-----------|-------|",
            "| ABC renewal date | Liquor license renewal | 60 days | Do not miss this. |",
            "| Jan 31 | CA CDTFA sales tax | 30 days | Annual or quarterly filing. |",
            "| Quarterly | SFDPH inspection window | Always ready | Unannounced. Keep logs current. |",
        ]

        if dates:
            pest = dates.get("pest_inspection", "")
            health = dates.get("health_inspection", "")
            fire = dates.get("fire_inspection", "")
            if pest:
                lines.append("| {} | Last pest inspection | -- | On file. |".format(pest))
            if health:
                lines.append("| {} | Last health inspection | -- | On file. |".format(health))
            if fire:
                lines.append("| {} | Last fire inspection | -- | On file. |".format(fire))

        lines.append("")

        return self._write(path, "\n".join(lines))

    def _write_schedule_readme(self, root):
        path = root / "docs" / "schedule" / "README.md"
        content = """# Schedule Data Format

Staff schedules are stored as markdown tables in this directory.

- `current.md` -- The active weekly schedule. One table with columns: Day, Shift, Start, End, Staff, Role.
- `staff.md` -- Staff roster with availability, max hours, and certification status.

Schedule skills read these files via `io.read_allowed_path()`. Do not move them outside `docs/schedule/` without updating skill configurations.
"""
        return self._write(path, content)

    def _write_schedule_current(self, root):
        path = root / "docs" / "schedule" / "current.md"
        lines = [
            "# Schedule -- Week of ____-__-__",
            "",
            "| Day | Shift | Start | End | Staff | Role |",
            "|-----|-------|-------|-----|-------|------|",
        ]

        hours = self._get("hours", {})
        staff = self._get("staff", [])

        if staff and hours:
            open_time = hours.get("open", "")
            close_time = hours.get("close", "")
            # Generate a basic schedule placeholder with staff
            for s in staff:
                lines.append("| Mon | Open | {} | {} | {} | {} |".format(
                    open_time, close_time, s.get("name", ""), s.get("role", "").title(),
                ))
        else:
            lines.append("| | | | | | |")

        lines.append("")

        return self._write(path, "\n".join(lines))

    def _write_schedule_staff(self, root):
        path = root / "docs" / "schedule" / "staff.md"
        lines = [
            "# Staff",
            "",
            "| Name | Role | Max Hours/Week | RBS Cert | RBS Expiry |",
            "|------|------|----------------|----------|-----------|",
        ]

        staff = self._get("staff", [])
        if staff:
            for s in staff:
                cert = "Yes" if s.get("rbs_cert") else "No"
                expiry = s.get("rbs_expiry", "--") or "--"
                lines.append("| {} | {} | {} | {} | {} |".format(
                    s.get("name", ""), s.get("role", "").title(),
                    s.get("max_hours", ""), cert, expiry,
                ))
        else:
            lines.append("| | | | | |")

        lines.append("")

        return self._write(path, "\n".join(lines))

    def _write_closeout_readme(self, root):
        path = root / "data" / "close-out" / "README.md"
        content = """# Close-Out Data

Nightly close-out reports go here. Generated by `python -m skills.close_out`.

This directory is mutable -- skills write here. Do not store reference data in this directory.
"""
        return self._write(path, content)

    def _write_86_readme(self, root):
        path = root / "data" / "86" / "README.md"
        content = """# 86 List

Current 86'd items. Managed by `python -m skills.eighty_six`.

This directory is mutable -- skills write here. Do not store reference data in this directory.
"""
        return self._write(path, content)
