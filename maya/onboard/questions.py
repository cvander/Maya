"""Question definitions, validators, and defaults for the onboarding wizard."""

import re
from datetime import datetime


# -- Validators --

def validate_bar_name(value):
    """Validate and sanitize bar name. Returns (display_name, slug) or raises ValueError."""
    value = value.strip()
    if not value:
        raise ValueError("Bar name is required.")
    if len(value) > 64:
        raise ValueError("Bar name must be 64 characters or fewer.")
    # Display name keeps original (after strip)
    display_name = value
    # Slug: only allow safe filesystem chars
    slug = re.sub(r'[^a-zA-Z0-9 _-]', '', value)
    slug = slug.strip()
    slug = re.sub(r'\s+', '-', slug)
    slug = slug.lower()
    if not slug:
        raise ValueError("Bar name must contain at least one alphanumeric character.")
    # Prevent path traversal
    if '..' in slug or '/' in slug or '\\' in slug:
        raise ValueError("Bar name contains invalid path characters.")
    return display_name, slug


def validate_bar_type(value):
    """Validate bar type choice."""
    valid = {"dive-bar", "cocktail-lounge", "sports-bar", "wine-bar", "other"}
    value = value.strip().lower()
    if value not in valid:
        raise ValueError("Bar type must be one of: {}".format(", ".join(sorted(valid))))
    return value


def validate_license_type(value):
    """Validate license type choice."""
    valid = {"Type 47", "Type 48", "other"}
    value = value.strip()
    # Normalize common inputs
    if value.lower() in ("type 47", "47"):
        return "Type 47"
    if value.lower() in ("type 48", "48"):
        return "Type 48"
    if value.lower() == "other":
        return "other"
    if value not in valid:
        raise ValueError("License type must be one of: Type 47, Type 48, other")
    return value


def validate_time(value):
    """Validate HH:MM time format."""
    value = value.strip()
    if not re.match(r'^\d{2}:\d{2}$', value):
        raise ValueError("Time must be in HH:MM format (e.g., 16:00).")
    hour, minute = int(value[:2]), int(value[3:])
    if hour > 23 or minute > 59:
        raise ValueError("Invalid time: {}".format(value))
    return value


def validate_date(value):
    """Validate YYYY-MM-DD date format."""
    value = value.strip()
    if not value:
        return ""
    if not re.match(r'^\d{4}-\d{2}-\d{2}$', value):
        raise ValueError("Date must be in YYYY-MM-DD format.")
    try:
        datetime.strptime(value, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Invalid date: {}".format(value))
    return value


def validate_currency(value):
    """Validate currency as float with 2 decimal places."""
    if isinstance(value, (int, float)):
        if value < 0:
            raise ValueError("Price cannot be negative.")
        return round(float(value), 2)
    value = str(value).strip().lstrip('$')
    try:
        result = round(float(value), 2)
    except (ValueError, TypeError):
        raise ValueError("Price must be a number (e.g., 12.50).")
    if result < 0:
        raise ValueError("Price cannot be negative.")
    return result


def validate_level(value):
    """Validate spirit level (0, 0.25, 0.5, 0.75, 1.0)."""
    valid = {0, 0.25, 0.5, 0.75, 1.0}
    try:
        fval = float(value)
    except (ValueError, TypeError):
        raise ValueError("Level must be one of: 0, 0.25, 0.5, 0.75, 1.0")
    if fval not in valid:
        raise ValueError("Level must be one of: 0, 0.25, 0.5, 0.75, 1.0")
    return fval


def validate_role(value):
    """Validate staff role."""
    valid = {"bartender", "barback", "manager"}
    value = value.strip().lower()
    if value not in valid:
        raise ValueError("Role must be one of: bartender, barback, manager")
    return value


def validate_vendor_type(value):
    """Validate vendor type."""
    valid = {"distributor", "brewery", "direct"}
    value = value.strip().lower()
    if value not in valid:
        raise ValueError("Vendor type must be one of: distributor, brewery, direct")
    return value


def validate_menu_category(value):
    """Validate menu item category."""
    valid = {"cocktail", "beer", "wine", "non-alc"}
    value = value.strip().lower()
    if value not in valid:
        raise ValueError("Category must be one of: cocktail, beer, wine, non-alc")
    return value


def validate_music_policy(value):
    """Validate music policy choice."""
    valid = {"live music", "jukebox", "no music"}
    value = value.strip().lower()
    if value not in valid:
        raise ValueError("Music policy must be one of: live music, jukebox, no music")
    return value


def validate_positive_int(value):
    """Validate a positive integer."""
    try:
        ival = int(value)
    except (ValueError, TypeError):
        raise ValueError("Must be a positive integer.")
    if ival < 0:
        raise ValueError("Must be a positive integer.")
    return ival


# -- Question flow for interactive mode --

QUESTIONS = [
    {
        "key": "bar_name",
        "prompt": "Bar name",
        "required": True,
        "help": "The name of your bar (max 64 chars).",
    },
    {
        "key": "bar_type",
        "prompt": "Bar type",
        "required": True,
        "choices": ["dive-bar", "cocktail-lounge", "sports-bar", "wine-bar", "other"],
        "help": "What kind of bar is this?",
    },
    {
        "key": "address",
        "prompt": "Address",
        "required": False,
        "help": "Street address (used in compliance docs). Press Enter to skip.",
    },
    {
        "key": "license_type",
        "prompt": "License type",
        "required": True,
        "choices": ["Type 47", "Type 48", "other"],
        "help": "Type 47 (on-sale general, eating place) or Type 48 (on-sale general, public premises).",
        "default": "Type 48",
    },
    {
        "key": "music_policy",
        "prompt": "Music policy",
        "required": True,
        "choices": ["live music", "jukebox", "no music"],
        "help": "What's your music situation?",
        "default": "jukebox",
    },
]


def validate_staff_entry(entry):
    """Validate a single staff entry dict."""
    errors = []
    if not entry.get("name", "").strip():
        errors.append("Staff name is required.")
    try:
        role = validate_role(entry.get("role", ""))
    except ValueError as e:
        errors.append(str(e))
        role = None
    try:
        validate_positive_int(entry.get("max_hours", 0))
    except ValueError:
        errors.append("max_hours must be a positive integer.")
    # RBS cert required for bartenders
    if role == "bartender" and not entry.get("rbs_cert"):
        errors.append("RBS certification is required for bartenders.")
    if entry.get("rbs_cert") and entry.get("rbs_expiry"):
        try:
            validate_date(entry["rbs_expiry"])
        except ValueError as e:
            errors.append("RBS expiry: {}".format(str(e)))
    if errors:
        raise ValueError("; ".join(errors))
    return entry


def validate_vendor_entry(entry):
    """Validate a single vendor entry dict."""
    errors = []
    if not entry.get("name", "").strip():
        errors.append("Vendor name is required.")
    try:
        validate_vendor_type(entry.get("type", ""))
    except ValueError as e:
        errors.append(str(e))
    if errors:
        raise ValueError("; ".join(errors))
    return entry


def validate_beer_entry(entry):
    """Validate a single beer entry dict."""
    errors = []
    if not entry.get("brewery", "").strip():
        errors.append("Brewery is required.")
    if not entry.get("name", "").strip():
        errors.append("Beer name is required.")
    try:
        validate_positive_int(entry.get("qty", 0))
    except ValueError:
        errors.append("qty must be a positive integer.")
    try:
        validate_positive_int(entry.get("reorder_at", 0))
    except ValueError:
        errors.append("reorder_at must be a positive integer.")
    try:
        validate_positive_int(entry.get("par", 0))
    except ValueError:
        errors.append("par must be a positive integer.")
    if errors:
        raise ValueError("; ".join(errors))
    return entry


def validate_spirit_entry(entry):
    """Validate a single spirits entry dict."""
    errors = []
    if not entry.get("category", "").strip():
        errors.append("Category is required.")
    if not entry.get("brand", "").strip():
        errors.append("Brand is required.")
    try:
        validate_level(entry.get("level", 0))
    except ValueError as e:
        errors.append(str(e))
    try:
        validate_positive_int(entry.get("qty", 0))
    except ValueError:
        errors.append("qty must be a positive integer.")
    try:
        validate_positive_int(entry.get("reorder_at", 0))
    except ValueError:
        errors.append("reorder_at must be a positive integer.")
    try:
        validate_positive_int(entry.get("par", 0))
    except ValueError:
        errors.append("par must be a positive integer.")
    if errors:
        raise ValueError("; ".join(errors))
    return entry


def validate_wine_entry(entry):
    """Validate a single wine entry dict."""
    errors = []
    if not entry.get("producer", "").strip():
        errors.append("Producer is required.")
    if not entry.get("name", "").strip():
        errors.append("Wine name is required.")
    try:
        validate_positive_int(entry.get("qty", 0))
    except ValueError:
        errors.append("qty must be a positive integer.")
    try:
        validate_positive_int(entry.get("reorder_at", 0))
    except ValueError:
        errors.append("reorder_at must be a positive integer.")
    try:
        validate_positive_int(entry.get("par", 0))
    except ValueError:
        errors.append("par must be a positive integer.")
    if entry.get("price") is not None:
        try:
            validate_currency(entry["price"])
        except ValueError as e:
            errors.append("Price: {}".format(str(e)))
    if errors:
        raise ValueError("; ".join(errors))
    return entry


def validate_menu_entry(entry):
    """Validate a single menu entry dict."""
    errors = []
    if not entry.get("name", "").strip():
        errors.append("Menu item name is required.")
    try:
        validate_menu_category(entry.get("category", ""))
    except ValueError as e:
        errors.append(str(e))
    if entry.get("price") is not None:
        try:
            validate_currency(entry["price"])
        except ValueError as e:
            errors.append("Price: {}".format(str(e)))
    if errors:
        raise ValueError("; ".join(errors))
    return entry


def validate_hours(hours):
    """Validate the operating hours structure."""
    errors = []
    if not hours:
        raise ValueError("Operating hours are required.")
    try:
        validate_time(hours.get("open", ""))
    except ValueError as e:
        errors.append("Open time: {}".format(str(e)))
    try:
        validate_time(hours.get("close", ""))
    except ValueError as e:
        errors.append("Close time: {}".format(str(e)))
    if not hours.get("days", "").strip():
        errors.append("Days open is required (e.g., Mon-Sun).")
    if errors:
        raise ValueError("; ".join(errors))
    return hours


def validate_compliance_dates(dates):
    """Validate compliance dates structure."""
    errors = []
    if not dates:
        return {}
    for key in ("pest_inspection", "health_inspection", "fire_inspection"):
        val = dates.get(key, "")
        if val:
            try:
                validate_date(val)
            except ValueError as e:
                errors.append("{}: {}".format(key, str(e)))
    if errors:
        raise ValueError("; ".join(errors))
    return dates


def validate_answers(answers):
    """Validate a complete answers dict. Returns list of error strings (empty = valid)."""
    errors = []

    # Required: bar_name
    if not answers.get("bar_name"):
        errors.append("bar_name is required.")
    else:
        try:
            validate_bar_name(answers["bar_name"])
        except ValueError as e:
            errors.append("bar_name: {}".format(str(e)))

    # Required: bar_type
    if not answers.get("bar_type"):
        errors.append("bar_type is required.")
    else:
        try:
            validate_bar_type(answers["bar_type"])
        except ValueError as e:
            errors.append("bar_type: {}".format(str(e)))

    # Optional: address (no validation needed beyond string)

    # License type
    if answers.get("license_type"):
        try:
            validate_license_type(answers["license_type"])
        except ValueError as e:
            errors.append("license_type: {}".format(str(e)))

    # Hours
    if answers.get("hours"):
        try:
            validate_hours(answers["hours"])
        except ValueError as e:
            errors.append("hours: {}".format(str(e)))

    # Staff
    for i, s in enumerate(answers.get("staff", [])):
        try:
            validate_staff_entry(s)
        except ValueError as e:
            errors.append("staff[{}]: {}".format(i, str(e)))

    # Vendors
    for i, v in enumerate(answers.get("vendors", [])):
        try:
            validate_vendor_entry(v)
        except ValueError as e:
            errors.append("vendors[{}]: {}".format(i, str(e)))

    # Beer
    for i, b in enumerate(answers.get("beer", [])):
        try:
            validate_beer_entry(b)
        except ValueError as e:
            errors.append("beer[{}]: {}".format(i, str(e)))

    # Spirits
    for i, s in enumerate(answers.get("spirits", [])):
        try:
            validate_spirit_entry(s)
        except ValueError as e:
            errors.append("spirits[{}]: {}".format(i, str(e)))

    # Wine
    for i, w in enumerate(answers.get("wine", [])):
        try:
            validate_wine_entry(w)
        except ValueError as e:
            errors.append("wine[{}]: {}".format(i, str(e)))

    # Menu
    for i, m in enumerate(answers.get("menu", [])):
        try:
            validate_menu_entry(m)
        except ValueError as e:
            errors.append("menu[{}]: {}".format(i, str(e)))

    # Music policy
    if answers.get("music_policy"):
        try:
            validate_music_policy(answers["music_policy"])
        except ValueError as e:
            errors.append("music_policy: {}".format(str(e)))

    # Compliance dates
    if answers.get("compliance_dates"):
        try:
            validate_compliance_dates(answers["compliance_dates"])
        except ValueError as e:
            errors.append("compliance_dates: {}".format(str(e)))

    return errors
