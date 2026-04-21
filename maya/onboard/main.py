"""Orchestrates the onboarding questionnaire flow."""

import json
import sys

from maya.onboard.questions import (
    QUESTIONS,
    validate_bar_name,
    validate_bar_type,
    validate_license_type,
    validate_time,
    validate_date,
    validate_role,
    validate_vendor_type,
    validate_menu_category,
    validate_music_policy,
    validate_currency,
    validate_level,
    validate_positive_int,
    validate_answers,
)
from maya.onboard.generator import Generator


def load_answers(path):
    """Load answers from a JSON file."""
    with open(path, "r") as f:
        return json.load(f)


def run_non_interactive(answers_path, output_dir):
    """Run the wizard in non-interactive mode with a pre-filled answers file.

    Args:
        answers_path: Path to JSON file with answers.
        output_dir: Directory where docs/ and data/ will be created.

    Returns:
        List of Path objects for all files created.

    Raises:
        ValueError: If answers fail validation.
        FileNotFoundError: If answers file doesn't exist.
    """
    answers = load_answers(answers_path)
    errors = validate_answers(answers)
    if errors:
        raise ValueError("Validation errors:\n  " + "\n  ".join(errors))

    gen = Generator(answers)
    return gen.generate(output_dir)


def _ask(prompt, required=False, choices=None, default=None, validator=None):
    """Ask a single question interactively. Returns the answer string."""
    suffix = ""
    if choices:
        suffix = " [{}]".format("/".join(choices))
    if default:
        suffix += " (default: {})".format(default)
    if not required:
        suffix += " (optional)"

    while True:
        try:
            answer = input("{}{}: ".format(prompt, suffix)).strip()
        except (EOFError, KeyboardInterrupt):
            print("")
            sys.exit(1)

        if not answer and default:
            answer = default
        if not answer and not required:
            return ""
        if not answer and required:
            print("  This field is required.")
            continue
        if choices and answer.lower() not in [c.lower() for c in choices]:
            print("  Must be one of: {}".format(", ".join(choices)))
            continue
        if validator:
            try:
                validator(answer)
            except ValueError as e:
                print("  {}".format(e))
                continue
        return answer


def _ask_repeated(item_name, fields, validators=None):
    """Ask for repeated entries (staff, vendors, etc). Returns list of dicts."""
    items = []
    validators = validators or {}
    print("\nEnter {} (press Enter with no name to finish):".format(item_name))

    while True:
        entry = {}
        first_field = fields[0]
        try:
            val = input("\n  {} name: ".format(item_name.rstrip('s').title())).strip()
        except (EOFError, KeyboardInterrupt):
            print("")
            break
        if not val:
            break
        entry[first_field] = val

        for field in fields[1:]:
            try:
                fval = input("  {}: ".format(field)).strip()
            except (EOFError, KeyboardInterrupt):
                print("")
                return items
            if field in validators and fval:
                try:
                    validators[field](fval)
                except ValueError as e:
                    print("    {}".format(e))
                    fval = input("  {} (retry): ".format(field)).strip()
            entry[field] = fval

        items.append(entry)

    return items


def run_interactive(output_dir):
    """Run the wizard interactively, prompting the user for each question.

    Args:
        output_dir: Directory where docs/ and data/ will be created.

    Returns:
        List of Path objects for all files created.
    """
    print("\n=== Maya Onboarding Wizard ===\n")
    print("Set up your bar for Maya. Answer the questions below.\n")

    answers = {}

    # 1. Bar name
    bar_name = _ask("Bar name", required=True, validator=validate_bar_name)
    answers["bar_name"] = bar_name

    # 2. Bar type
    answers["bar_type"] = _ask(
        "Bar type", required=True,
        choices=["dive-bar", "cocktail-lounge", "sports-bar", "wine-bar", "other"],
        validator=validate_bar_type,
    )

    # 3. Address
    answers["address"] = _ask("Address", required=False)

    # 4. License type
    answers["license_type"] = _ask(
        "License type", required=True,
        choices=["Type 47", "Type 48", "other"],
        default="Type 48",
        validator=validate_license_type,
    )

    # 5. Operating hours
    print("\n--- Operating Hours ---")
    open_time = _ask("Open time (HH:MM)", required=True, validator=validate_time)
    close_time = _ask("Close time (HH:MM)", required=True, validator=validate_time)
    days = _ask("Days open (e.g., Mon-Sun)", required=True)
    answers["hours"] = {"open": open_time, "close": close_time, "days": days}

    # 6. Staff
    print("\n--- Staff ---")
    staff_list = []
    print("Enter staff members (press Enter with no name to finish):")
    while True:
        try:
            name = input("\n  Staff name: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("")
            break
        if not name:
            break
        role = _ask("  Role", required=True, choices=["bartender", "barback", "manager"], validator=validate_role)
        max_hours = _ask("  Max hours/week", required=True, validator=validate_positive_int)
        rbs = _ask("  RBS certified?", required=True, choices=["yes", "no"])
        rbs_cert = rbs.lower() == "yes"
        rbs_expiry = ""
        if rbs_cert:
            rbs_expiry = _ask("  RBS expiry date (YYYY-MM-DD)", required=True, validator=validate_date)
        staff_list.append({
            "name": name,
            "role": role,
            "max_hours": int(max_hours),
            "rbs_cert": rbs_cert,
            "rbs_expiry": rbs_expiry,
        })
    answers["staff"] = staff_list

    # 7. Vendors
    print("\n--- Vendors ---")
    vendor_list = []
    print("Enter vendors (press Enter with no name to finish):")
    while True:
        try:
            name = input("\n  Vendor name: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("")
            break
        if not name:
            break
        vtype = _ask("  Type", required=True, choices=["distributor", "brewery", "direct"], validator=validate_vendor_type)
        rep = _ask("  Rep name", required=False)
        phone = _ask("  Phone", required=False)
        email = _ask("  Email", required=False)
        account = _ask("  Account number", required=False)
        cats = _ask("  Categories (comma-separated, e.g., beer,spirits)", required=False)
        categories = [c.strip() for c in cats.split(",") if c.strip()] if cats else []
        vendor_list.append({
            "name": name, "type": vtype, "rep": rep,
            "phone": phone, "email": email, "account": account,
            "categories": categories,
        })
    answers["vendors"] = vendor_list

    # 8. Beer inventory
    print("\n--- Beer Inventory ---")
    beer_list = []
    print("Enter beers (press Enter with no brewery to finish):")
    while True:
        try:
            brewery = input("\n  Brewery: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("")
            break
        if not brewery:
            break
        bname = _ask("  Beer name", required=True)
        style = _ask("  Style", required=False)
        fmt = _ask("  Format (tap/bottle/can/1/2 bbl/1/6 bbl)", required=False)
        qty = _ask("  Qty", required=True, validator=validate_positive_int)
        reorder = _ask("  Reorder at", required=True, validator=validate_positive_int)
        par = _ask("  Par", required=True, validator=validate_positive_int)
        beer_list.append({
            "brewery": brewery, "name": bname, "style": style,
            "format": fmt, "qty": int(qty), "reorder_at": int(reorder), "par": int(par),
        })
    answers["beer"] = beer_list

    # 9. Spirits inventory
    print("\n--- Spirits Inventory ---")
    spirits_list = []
    print("Enter spirits (press Enter with no category to finish):")
    while True:
        try:
            cat = input("\n  Category (e.g., Bourbon, Vodka): ").strip()
        except (EOFError, KeyboardInterrupt):
            print("")
            break
        if not cat:
            break
        brand = _ask("  Brand", required=True)
        size = _ask("  Size (e.g., 750ml, 1L)", required=False)
        qty = _ask("  Qty", required=True, validator=validate_positive_int)
        level = _ask("  Level (0/0.25/0.5/0.75/1.0)", required=True, validator=validate_level)
        reorder = _ask("  Reorder at", required=True, validator=validate_positive_int)
        par = _ask("  Par", required=True, validator=validate_positive_int)
        spirits_list.append({
            "category": cat, "brand": brand, "size": size,
            "qty": int(qty), "level": float(level),
            "reorder_at": int(reorder), "par": int(par),
        })
    answers["spirits"] = spirits_list

    # 10. Wine inventory
    print("\n--- Wine Inventory ---")
    wine_list = []
    print("Enter wines (press Enter with no producer to finish):")
    while True:
        try:
            producer = input("\n  Producer: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("")
            break
        if not producer:
            break
        wname = _ask("  Wine name", required=True)
        wtype = _ask("  Type (Red/White/Rose/Sparkling)", required=False)
        qty = _ask("  Qty", required=True, validator=validate_positive_int)
        reorder = _ask("  Reorder at", required=True, validator=validate_positive_int)
        par = _ask("  Par", required=True, validator=validate_positive_int)
        price = _ask("  Price per glass/bottle", required=False, validator=validate_currency)
        wine_list.append({
            "producer": producer, "name": wname, "type": wtype,
            "qty": int(qty), "reorder_at": int(reorder), "par": int(par),
            "price": float(price) if price else None,
        })
    answers["wine"] = wine_list

    # 11. Menu items
    print("\n--- Menu ---")
    menu_list = []
    print("Enter menu items (press Enter with no name to finish):")
    while True:
        try:
            mname = input("\n  Item name: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("")
            break
        if not mname:
            break
        mcat = _ask("  Category", required=True, choices=["cocktail", "beer", "wine", "non-alc"], validator=validate_menu_category)
        mprice = _ask("  Price", required=True, validator=validate_currency)
        mdesc = _ask("  Description", required=False)
        menu_list.append({
            "name": mname, "category": mcat,
            "price": float(mprice), "description": mdesc,
        })
    answers["menu"] = menu_list

    # 12. Music policy
    answers["music_policy"] = _ask(
        "Music policy", required=True,
        choices=["live music", "jukebox", "no music"],
        default="jukebox",
        validator=validate_music_policy,
    )

    # 13. Compliance dates
    print("\n--- Compliance Dates ---")
    pest = _ask("Last pest inspection (YYYY-MM-DD)", required=False, validator=validate_date)
    health = _ask("Last health inspection (YYYY-MM-DD)", required=False, validator=validate_date)
    fire = _ask("Last fire inspection (YYYY-MM-DD)", required=False, validator=validate_date)
    answers["compliance_dates"] = {
        "pest_inspection": pest,
        "health_inspection": health,
        "fire_inspection": fire,
    }

    # Validate and generate
    errors = validate_answers(answers)
    if errors:
        print("\nValidation errors:")
        for e in errors:
            print("  - {}".format(e))
        sys.exit(1)

    gen = Generator(answers)
    return gen.generate(output_dir)
