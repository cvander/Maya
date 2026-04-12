"""Base template - defines the structure all bar types share."""

from pathlib import Path


class BaseTemplate:
    """Base class for bar type templates.

    Subclasses override data properties to provide bar-type-specific content.
    The generate() method writes all files using shared formatting logic.
    """

    # -- Subclasses must set these --
    name = ""
    description = ""

    # -- Data properties subclasses override --

    def beer_on_tap(self):
        """List of dicts: Brewery, Beer, Style, Size, Qty, Reorder_at, Par, Notes."""
        return []

    def beer_packaged(self):
        """List of dicts: Brewery, Beer, Style, Format, Qty, Reorder_at, Par, Notes."""
        return []

    def beer_notes(self):
        """List of strings for the beer notes section."""
        return []

    def spirits_well(self):
        """List of dicts: Category, Brand, Size, Qty, Level, Reorder_at, Par, Notes."""
        return []

    def spirits_call(self):
        """List of dicts: Category, Brand, Size, Qty, Level, Reorder_at, Par, Price, Notes."""
        return []

    def spirits_modifiers(self):
        """List of dicts: Item, Brand, Size, Qty, Level, Reorder_at, Par, Opened, Notes."""
        return []

    def spirits_mixers(self):
        """List of dicts: Item, Brand, Size, Qty, Reorder_at, Notes."""
        return []

    def spirits_notes(self):
        """List of strings for spirits notes section."""
        return [
            "Count weekly, order Monday.",
            "Track what's moving fast and what's collecting dust.",
            "When a bottle empties, note the date.",
            "Level is 0 to 1.0 in quarter increments (0, 0.25, 0.5, 0.75, 1.0).",
        ]

    def wine_by_glass(self):
        """List of dicts: Producer, Wine, Type, Region, Vintage, Qty, Reorder_at, Par, Opened, Price, Notes."""
        return []

    def wine_by_bottle(self):
        """List of dicts: Producer, Wine, Type, Region, Vintage, Qty, Reorder_at, Par, Price, Notes."""
        return []

    def wine_notes(self):
        """List of strings for wine notes section."""
        return []

    def vendors_distributors(self):
        """List of dicts: Vendor, Rep, Phone, Email, Order_Day, Delivery_Day, Minimum, Account, Notes."""
        return []

    def vendors_direct(self):
        """List of dicts: Vendor, Contact, Phone, Location, Notes."""
        return []

    def vendors_payment(self):
        """List of dicts: Vendor, Terms, Notes."""
        return []

    def vendors_notes(self):
        """List of strings."""
        return [
            "Rep relationships matter. If something's allocated, the rep decides who gets it.",
            "When a rep changes, update this file same day.",
            "Keep order confirmations until delivery is verified.",
            "Dispute shorts within 24 hours or lose the claim.",
        ]

    def menu_cocktails(self):
        """List of dicts: name, ingredients (list of str), instruction, price."""
        return []

    def menu_beer_prices(self):
        """List of dicts: What, Price."""
        return []

    def menu_wine_prices(self):
        """List of dicts: What, Price."""
        return []

    def menu_spirits_prices(self):
        """List of dicts: Tier, Price, Notes."""
        return []

    def menu_food(self):
        """List of dicts: Item, Price, Notes. Optional - not all bars have food."""
        return []

    def menu_notes(self):
        """List of strings for how the menu changes."""
        return [
            "Buy-outs go on special until gone.",
            "Seasonal changes when it makes sense.",
            "If it doesn't sell, it comes off.",
        ]

    def staff_roster(self):
        """List of dicts: Name, Role, Max_Hours, Availability, RBS_Cert, RBS_Expiry."""
        return []

    def schedule_current(self):
        """List of dicts: Day, Shift, Start, End, Staff, Role."""
        return []

    def calendar_events(self):
        """List of dicts: Date, Event, Impact, Notes."""
        return [
            {"Date": "Jan 1", "Event": "New Year's Day", "Impact": "Low volume", "Notes": "Late open OK."},
            {"Date": "Feb (Super Bowl Sunday)", "Event": "Super Bowl", "Impact": "High volume", "Notes": "Open early. Beer moves fast."},
            {"Date": "March 17", "Event": "St. Patrick's Day", "Impact": "High volume", "Notes": "Irish whiskey specials, extra staff."},
            {"Date": "June (last week)", "Event": "SF Pride Week", "Impact": "Highest volume week", "Notes": "Plan 2 weeks out. Extra everything."},
            {"Date": "July 4", "Event": "Fourth of July", "Impact": "Moderate", "Notes": "Neighborhood crowd. Good night for regulars."},
            {"Date": "Aug (2nd weekend)", "Event": "Outside Lands", "Impact": "Weekend overflow", "Notes": "Post-show crowds Friday-Sunday."},
            {"Date": "Oct 31", "Event": "Halloween", "Impact": "High volume", "Notes": "Extra staff. Long night."},
            {"Date": "Dec 31", "Event": "New Year's Eve", "Impact": "Highest revenue night", "Notes": "Staff confirmed 2 weeks out."},
        ]

    def calendar_compliance(self):
        """List of dicts: Date, What, Lead_Time, Notes."""
        return [
            {"Date": "ABC renewal date", "What": "Liquor license renewal", "Lead_Time": "60 days", "Notes": "Do not miss this."},
            {"Date": "Jan 31", "What": "CA CDTFA sales tax", "Lead_Time": "30 days", "Notes": "Annual or quarterly filing."},
            {"Date": "Quarterly", "What": "SFDPH inspection window", "Lead_Time": "Always ready", "Notes": "Unannounced. Keep logs current."},
        ]

    def opening_extras(self):
        """Extra checklist items specific to this bar type."""
        return []

    def closing_extras(self):
        """Extra checklist items specific to this bar type."""
        return []

    def cooler_names(self):
        """List of cooler names for temperature log."""
        return ["Beer cooler", "Wine fridge"]

    def staff_cert_rows(self):
        """Pre-filled rows for staff certs. Uses staff_roster() data."""
        rows = []
        for s in self.staff_roster():
            cert = s.get("RBS_Cert", "")
            expiry = s.get("RBS_Expiry", "--")
            status = "Active" if cert else "Pending"
            rows.append({
                "Name": s["Name"],
                "Role": s["Role"],
                "Cert": cert,
                "Issued": "",
                "Expires": expiry,
                "Status": status,
                "Notes": "",
            })
        return rows

    # -- Generation logic --

    def generate(self, output_dir):
        """Generate all files into output_dir. Returns list of files created."""
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

    # -- File writers --

    def _write_beer(self, root):
        path = root / "docs" / "inventory" / "beer.md"
        lines = ["# Beer Inventory", "", "Last counted: ____-__-__", ""]

        tap = self.beer_on_tap()
        if tap:
            lines.append("## On Tap")
            lines.append("")
            lines.append("| # | Brewery | Beer | Style | Size | Qty (kegs) | Reorder at | Par | Notes |")
            lines.append("|---|---------|------|-------|------|------------|------------|-----|-------|")
            for i, b in enumerate(tap, 1):
                lines.append("| {} | {} | {} | {} | {} | {} | {} | {} | {} |".format(
                    i, b["Brewery"], b["Beer"], b["Style"], b["Size"],
                    b["Qty"], b["Reorder_at"], b["Par"], b.get("Notes", ""),
                ))
            lines.append("")

        pkg = self.beer_packaged()
        if pkg:
            lines.append("## Bottles & Cans")
            lines.append("")
            lines.append("| Brewery | Beer | Style | Format | Qty | Reorder at | Par | Notes |")
            lines.append("|---------|------|-------|--------|-----|------------|-----|-------|")
            for b in pkg:
                lines.append("| {} | {} | {} | {} | {} | {} | {} | {} |".format(
                    b["Brewery"], b["Beer"], b["Style"], b["Format"],
                    b["Qty"], b["Reorder_at"], b["Par"], b.get("Notes", ""),
                ))
            lines.append("")

        notes = self.beer_notes()
        if notes:
            lines.append("## Notes")
            lines.append("")
            for n in notes:
                lines.append("- {}".format(n))
            lines.append("")

        return self._write(path, "\n".join(lines))

    def _write_spirits(self, root):
        path = root / "docs" / "inventory" / "spirits.md"
        lines = ["# Spirits & Bottles Inventory", "", "Last counted: ____-__-__", ""]

        well = self.spirits_well()
        if well:
            lines.append("## Well (House Pour)")
            lines.append("")
            lines.append("| Category | Brand | Size | Qty | Level | Reorder at | Par | Notes |")
            lines.append("|----------|-------|------|-----|-------|------------|-----|-------|")
            for s in well:
                lines.append("| {} | {} | {} | {} | {} | {} | {} | {} |".format(
                    s["Category"], s["Brand"], s["Size"], s["Qty"],
                    s["Level"], s["Reorder_at"], s["Par"], s.get("Notes", ""),
                ))
            lines.append("")

        call = self.spirits_call()
        if call:
            lines.append("## Call & Top Shelf")
            lines.append("")
            lines.append("| Category | Brand | Size | Qty | Level | Reorder at | Par | Price | Notes |")
            lines.append("|----------|-------|------|-----|-------|------------|-----|-------|-------|")
            for s in call:
                lines.append("| {} | {} | {} | {} | {} | {} | {} | {} | {} |".format(
                    s["Category"], s["Brand"], s["Size"], s["Qty"],
                    s["Level"], s["Reorder_at"], s["Par"], s["Price"], s.get("Notes", ""),
                ))
            lines.append("")

        mods = self.spirits_modifiers()
        if mods:
            lines.append("## Bitters, Vermouths & Modifiers")
            lines.append("")
            lines.append("| Item | Brand | Size | Qty | Level | Reorder at | Par | Opened | Notes |")
            lines.append("|------|-------|------|-----|-------|------------|-----|--------|-------|")
            for m in mods:
                lines.append("| {} | {} | {} | {} | {} | {} | {} | {} | {} |".format(
                    m["Item"], m["Brand"], m["Size"], m["Qty"],
                    m["Level"], m["Reorder_at"], m["Par"], m.get("Opened", ""), m.get("Notes", ""),
                ))
            lines.append("")

        mixers = self.spirits_mixers()
        if mixers:
            lines.append("## Mixers & Non-Alcoholic")
            lines.append("")
            lines.append("| Item | Brand | Size | Qty | Reorder at | Notes |")
            lines.append("|------|-------|------|-----|------------|-------|")
            for m in mixers:
                lines.append("| {} | {} | {} | {} | {} | {} |".format(
                    m["Item"], m["Brand"], m["Size"], m["Qty"],
                    m["Reorder_at"], m.get("Notes", ""),
                ))
            lines.append("")

        notes = self.spirits_notes()
        if notes:
            lines.append("## Notes")
            lines.append("")
            for n in notes:
                lines.append("- {}".format(n))
            lines.append("")

        return self._write(path, "\n".join(lines))

    def _write_wine(self, root):
        path = root / "docs" / "inventory" / "wine.md"
        lines = ["# Wine Inventory", "", "Last counted: ____-__-__", ""]

        glass = self.wine_by_glass()
        if glass:
            lines.append("## By the Glass")
            lines.append("")
            lines.append("| Producer | Wine | Type | Region | Vintage | Qty | Reorder at | Par | Opened | Price | Notes |")
            lines.append("|----------|------|------|--------|---------|-----|------------|-----|--------|-------|-------|")
            for w in glass:
                lines.append("| {} | {} | {} | {} | {} | {} | {} | {} | {} | {} | {} |".format(
                    w["Producer"], w["Wine"], w["Type"], w["Region"], w["Vintage"],
                    w["Qty"], w["Reorder_at"], w["Par"], w.get("Opened", ""), w["Price"], w.get("Notes", ""),
                ))
            lines.append("")

        bottle = self.wine_by_bottle()
        if bottle:
            lines.append("## By the Bottle")
            lines.append("")
            lines.append("| Producer | Wine | Type | Region | Vintage | Qty | Reorder at | Par | Price | Notes |")
            lines.append("|----------|------|------|--------|---------|-----|------------|-----|-------|-------|")
            for w in bottle:
                lines.append("| {} | {} | {} | {} | {} | {} | {} | {} | {} | {} |".format(
                    w["Producer"], w["Wine"], w["Type"], w["Region"], w["Vintage"],
                    w["Qty"], w["Reorder_at"], w["Par"], w["Price"], w.get("Notes", ""),
                ))
            lines.append("")

        notes = self.wine_notes()
        if notes:
            lines.append("## Notes")
            lines.append("")
            for n in notes:
                lines.append("- {}".format(n))
            lines.append("")

        return self._write(path, "\n".join(lines))

    def _write_vendors(self, root):
        path = root / "docs" / "vendors" / "README.md"
        lines = ["# Vendors", "", "Who supplies what, when to order, and who to call.", "", "---", ""]

        dist = self.vendors_distributors()
        if dist:
            lines.append("## Distributors")
            lines.append("")
            lines.append("| Vendor | Rep | Phone | Email | Order Day | Delivery Day | Minimum | Account # | Notes |")
            lines.append("|--------|-----|-------|-------|-----------|-------------|---------|-----------|-------|")
            for v in dist:
                lines.append("| {} | {} | {} | {} | {} | {} | {} | {} | {} |".format(
                    v["Vendor"], v.get("Rep", ""), v.get("Phone", ""), v.get("Email", ""),
                    v["Order_Day"], v["Delivery_Day"], v["Minimum"], v.get("Account", ""), v.get("Notes", ""),
                ))
            lines.append("")

        direct = self.vendors_direct()
        if direct:
            lines.append("## Direct / Walk-In")
            lines.append("")
            lines.append("| Vendor | Contact | Phone | Location | Notes |")
            lines.append("|--------|---------|-------|----------|-------|")
            for v in direct:
                lines.append("| {} | {} | {} | {} | {} |".format(
                    v["Vendor"], v.get("Contact", ""), v.get("Phone", ""),
                    v.get("Location", ""), v.get("Notes", ""),
                ))
            lines.append("")

        lines.append("## Order Workflow")
        lines.append("")
        lines.append("1. **Sunday night**: Run `python -m skills.inventory_check` to see what's low.")
        lines.append("2. **Monday morning**: Review low stock list.")
        lines.append("3. **Monday by noon**: Place distributor orders.")
        lines.append("4. **Wednesday-Friday**: Receive deliveries. Count against order. Flag shorts immediately.")
        lines.append("")

        pay = self.vendors_payment()
        if pay:
            lines.append("## Payment Terms")
            lines.append("")
            lines.append("| Vendor | Terms | Notes |")
            lines.append("|--------|-------|-------|")
            for p in pay:
                lines.append("| {} | {} | {} |".format(
                    p["Vendor"], p["Terms"], p.get("Notes", ""),
                ))
            lines.append("")

        notes = self.vendors_notes()
        if notes:
            lines.append("## Notes")
            lines.append("")
            for n in notes:
                lines.append("- {}".format(n))
            lines.append("")

        return self._write(path, "\n".join(lines))

    def _write_menu(self, root):
        path = root / "docs" / "menu" / "current.md"
        lines = ["# Current Menu", "", "Last updated: ____-__-__", ""]
        lines.append("---")
        lines.append("")

        cocktails = self.menu_cocktails()
        if cocktails:
            lines.append("## Cocktails")
            lines.append("")
            for c in cocktails:
                lines.append("### {}".format(c["name"]))
                for ing in c["ingredients"]:
                    lines.append("- {}".format(ing))
                lines.append("")
                if c.get("instruction"):
                    lines.append(c["instruction"])
                    lines.append("")
                lines.append("**Price:** ${}".format(c["price"]))
                lines.append("")

            lines.append("---")
            lines.append("")

        beer_prices = self.menu_beer_prices()
        if beer_prices:
            lines.append("## Beer")
            lines.append("")
            lines.append("See [inventory/beer.md](../inventory/beer.md) for current taps and bottles.")
            lines.append("")
            lines.append("| What | Price |")
            lines.append("|------|-------|")
            for b in beer_prices:
                lines.append("| {} | {} |".format(b["What"], b["Price"]))
            lines.append("")

        wine_prices = self.menu_wine_prices()
        if wine_prices:
            lines.append("## Wine")
            lines.append("")
            lines.append("See [inventory/wine.md](../inventory/wine.md) for current list.")
            lines.append("")
            lines.append("| What | Price |")
            lines.append("|------|-------|")
            for w in wine_prices:
                lines.append("| {} | {} |".format(w["What"], w["Price"]))
            lines.append("")

        spirit_prices = self.menu_spirits_prices()
        if spirit_prices:
            lines.append("## Spirits (Neat/Rocks)")
            lines.append("")
            lines.append("| Tier | Price | Notes |")
            lines.append("|------|-------|-------|")
            for s in spirit_prices:
                lines.append("| {} | {} | {} |".format(s["Tier"], s["Price"], s.get("Notes", "")))
            lines.append("")

        food = self.menu_food()
        if food:
            lines.append("## Food")
            lines.append("")
            lines.append("| Item | Price | Notes |")
            lines.append("|------|-------|-------|")
            for f in food:
                lines.append("| {} | {} | {} |".format(f["Item"], f["Price"], f.get("Notes", "")))
            lines.append("")

        lines.append("---")
        lines.append("")
        lines.append("## How the Menu Changes")
        lines.append("")
        for n in self.menu_notes():
            lines.append("- {}".format(n))
        lines.append("")

        return self._write(path, "\n".join(lines))

    def _write_opening(self, root):
        path = root / "docs" / "operations" / "opening.md"
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

        extras = self.opening_extras()
        if extras:
            lines.append("## {} Specifics".format(self.name))
            lines.append("")
            for e in extras:
                lines.append("- [ ] {}".format(e))
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
        lines.append("**Time target**: 30-45 minutes before doors open.")
        lines.append("**Who**: Opening bartender.")
        lines.append("")

        return self._write(path, "\n".join(lines))

    def _write_closing(self, root):
        path = root / "docs" / "operations" / "closing.md"
        lines = [
            "# Closing Checklist",
            "",
            "Last call is at 1:30 AM. Doors locked at 2:00 AM. This gets done before anyone leaves.",
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
        ]

        extras = self.closing_extras()
        if extras:
            lines.append("## {} Specifics".format(self.name))
            lines.append("")
            for e in extras:
                lines.append("- [ ] {}".format(e))
            lines.append("")

        lines.append("## Shift Notes")
        lines.append("")
        lines.append("```")
        lines.append("Date: ____-__-__")
        lines.append("Bartender: ________________")
        lines.append("")
        lines.append("What happened tonight:")
        lines.append("")
        lines.append("")
        lines.append("What's 86'd:")
        lines.append("")
        lines.append("")
        lines.append("What needs attention tomorrow:")
        lines.append("")
        lines.append("")
        lines.append("```")
        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append("**Time target**: 30-45 minutes after last guest leaves.")
        lines.append("**Who**: Closing bartender. Nobody leaves until this is done.")
        lines.append("")

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
        for cooler in self.cooler_names():
            for _ in range(7):
                lines.append("| | {} | | | | |".format(cooler))
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
        content = """# Pest Control Log

Weekly visual inspection. SFDPH requires documentation of pest monitoring.

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
"""
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
            "| Name | Role | RBS Cert # | Issued | Expires | Status | Notes |",
            "|------|------|-----------|--------|---------|--------|-------|",
        ]
        for row in self.staff_cert_rows():
            lines.append("| {} | {} | {} | {} | {} | {} | {} |".format(
                row["Name"], row["Role"], row["Cert"], row["Issued"],
                row["Expires"], row["Status"], row.get("Notes", ""),
            ))
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
        content = """# Permits & Licenses

All permits, licenses, and compliance documents for the bar.

---

## Active Permits

| Permit | Issuing Authority | Number | Issued | Expires | Status | Notes |
|--------|-------------------|--------|--------|---------|--------|-------|
| Liquor License (Type 48) | CA ABC | | | | Active | On-sale general, public premises. |
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
"""
        return self._write(path, content)

    def _write_calendar(self, root):
        path = root / "docs" / "calendar.md"
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
        ]
        for e in self.calendar_events():
            lines.append("| {} | {} | {} | {} |".format(
                e["Date"], e["Event"], e["Impact"], e["Notes"],
            ))
        lines.append("")

        lines.append("## Compliance Dates")
        lines.append("")
        lines.append("| Date | What | Lead Time | Notes |")
        lines.append("|------|------|-----------|-------|")
        for c in self.calendar_compliance():
            lines.append("| {} | {} | {} | {} |".format(
                c["Date"], c["What"], c["Lead_Time"], c["Notes"],
            ))
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
        for row in self.schedule_current():
            lines.append("| {} | {} | {} | {} | {} | {} |".format(
                row["Day"], row["Shift"], row["Start"], row["End"],
                row["Staff"], row["Role"],
            ))
        lines.append("")

        return self._write(path, "\n".join(lines))

    def _write_schedule_staff(self, root):
        path = root / "docs" / "schedule" / "staff.md"
        lines = [
            "# Staff",
            "",
            "| Name | Role | Max Hours/Week | Availability | RBS Cert | RBS Expiry |",
            "|------|------|----------------|-------------|----------|-----------|",
        ]
        for s in self.staff_roster():
            lines.append("| {} | {} | {} | {} | {} | {} |".format(
                s["Name"], s["Role"], s["Max_Hours"],
                s["Availability"], "Yes" if s["RBS_Cert"] else "No",
                s["RBS_Expiry"],
            ))
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

    # -- Helpers --

    def _write(self, path, content):
        """Write content to path, creating parent dirs as needed. Returns the path."""
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
        return path
