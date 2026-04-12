"""Dive bar template - well drinks, PBR tallboys, cheap shots, jukebox, pool table."""

from maya.seed.templates.base import BaseTemplate


class DiveBarTemplate(BaseTemplate):
    name = "Dive Bar"
    description = "Well drinks, PBR tallboys, cheap shots. Jukebox. Pool table. Cash-heavy."

    def beer_on_tap(self):
        return [
            {"Brewery": "Pabst", "Beer": "PBR", "Style": "American Lager", "Size": "1/2 bbl", "Qty": 2, "Reorder_at": 1, "Par": 3, "Notes": "The anchor. Always on."},
            {"Brewery": "Anchor Brewing", "Beer": "Anchor Steam", "Style": "California Common", "Size": "1/6 bbl", "Qty": 1, "Reorder_at": 1, "Par": 2, "Notes": "SF loyalty."},
            {"Brewery": "Lagunitas", "Beer": "IPA", "Style": "IPA", "Size": "1/6 bbl", "Qty": 1, "Reorder_at": 1, "Par": 2, "Notes": "For the IPA people."},
        ]

    def beer_packaged(self):
        return [
            {"Brewery": "Pabst", "Beer": "PBR", "Style": "Lager", "Format": "16oz tallboy", "Qty": 48, "Reorder_at": 24, "Par": 72, "Notes": "The workhorse."},
            {"Brewery": "Coors", "Beer": "Banquet", "Style": "Lager", "Format": "12oz bottle", "Qty": 24, "Reorder_at": 12, "Par": 36, "Notes": "Stubby bottles. Regulars like it."},
            {"Brewery": "Modelo", "Beer": "Especial", "Style": "Lager", "Format": "12oz bottle", "Qty": 24, "Reorder_at": 12, "Par": 36, "Notes": "With a lime."},
            {"Brewery": "Tecate", "Beer": "Original", "Style": "Lager", "Format": "16oz tallboy", "Qty": 24, "Reorder_at": 12, "Par": 36, "Notes": "Salt and lime if they ask."},
            {"Brewery": "Sierra Nevada", "Beer": "Pale Ale", "Style": "Pale Ale", "Format": "12oz bottle", "Qty": 12, "Reorder_at": 6, "Par": 18, "Notes": "The fancy option."},
        ]

    def beer_notes(self):
        return [
            "Cheap, cold, fast. That's the beer program.",
            "PBR is the backbone. Never run out.",
            "Tallboys outsell drafts 3:1. Stock accordingly.",
            "Don't overthink it. People come here for the price and the vibe, not the beer list.",
        ]

    def spirits_well(self):
        return [
            {"Category": "Bourbon", "Brand": "Jim Beam", "Size": "1L", "Qty": 4, "Level": 0.5, "Reorder_at": 3, "Par": 6, "Notes": "House pour. Shots and whiskey-cokes."},
            {"Category": "Vodka", "Brand": "Smirnoff", "Size": "1L", "Qty": 3, "Level": 0.75, "Reorder_at": 2, "Par": 5, "Notes": "Vodka sodas, shots."},
            {"Category": "Gin", "Brand": "New Amsterdam", "Size": "1L", "Qty": 2, "Level": 0.5, "Reorder_at": 1, "Par": 3, "Notes": "Gin and tonic. Simple."},
            {"Category": "Tequila", "Brand": "Sauza Silver", "Size": "1L", "Qty": 2, "Level": 0.5, "Reorder_at": 1, "Par": 3, "Notes": "Shots. Margaritas if someone insists."},
            {"Category": "Rum", "Brand": "Bacardi Superior", "Size": "1L", "Qty": 2, "Level": 0.75, "Reorder_at": 1, "Par": 3, "Notes": "Rum and coke territory."},
            {"Category": "Whiskey", "Brand": "Jameson", "Size": "750ml", "Qty": 3, "Level": 0.5, "Reorder_at": 2, "Par": 4, "Notes": "Jameson shots are currency here."},
        ]

    def spirits_call(self):
        return [
            {"Category": "Bourbon", "Brand": "Maker's Mark", "Size": "750ml", "Qty": 1, "Level": 0.75, "Reorder_at": 1, "Par": 2, "Price": "$8", "Notes": "Step-up from well."},
            {"Category": "Tequila", "Brand": "Espolon Blanco", "Size": "750ml", "Qty": 1, "Level": 0.5, "Reorder_at": 1, "Par": 2, "Price": "$8", "Notes": "For the tequila snobs."},
            {"Category": "Irish", "Brand": "Tullamore D.E.W.", "Size": "750ml", "Qty": 1, "Level": 0.5, "Reorder_at": 1, "Par": 2, "Price": "$8", "Notes": "Alternative to Jameson."},
        ]

    def spirits_modifiers(self):
        return [
            {"Item": "Angostura bitters", "Brand": "Angostura", "Size": "4oz", "Qty": 1, "Level": 0.5, "Reorder_at": 1, "Par": 2, "Notes": "Rarely needed."},
        ]

    def spirits_mixers(self):
        return [
            {"Item": "Cola", "Brand": "Pepsi", "Size": "2L", "Qty": 6, "Reorder_at": 4, "Notes": "Whiskey-coke is half the bar."},
            {"Item": "Soda water", "Brand": "Store brand", "Size": "1L", "Qty": 6, "Reorder_at": 4, "Notes": "Vodka sodas."},
            {"Item": "Tonic", "Brand": "Schweppes", "Size": "1L", "Qty": 3, "Reorder_at": 2, "Notes": "G&T."},
            {"Item": "Ginger ale", "Brand": "Canada Dry", "Size": "1L", "Qty": 2, "Reorder_at": 1, "Notes": ""},
            {"Item": "Orange juice", "Brand": "Tropicana", "Size": "qt", "Qty": 2, "Reorder_at": 1, "Notes": "Screwdrivers."},
            {"Item": "Cranberry juice", "Brand": "Ocean Spray", "Size": "32oz", "Qty": 2, "Reorder_at": 1, "Notes": "Cape Cods."},
            {"Item": "Limes", "Brand": "", "Size": "each", "Qty": 15, "Reorder_at": 8, "Notes": "Wedges. Not wheels. Not twists."},
            {"Item": "Lemons", "Brand": "", "Size": "each", "Qty": 8, "Reorder_at": 4, "Notes": "Minimal."},
        ]

    def spirits_notes(self):
        return [
            "Count weekly, order Monday.",
            "Track what's moving fast. Jameson and Jim Beam go fastest.",
            "Level is 0 to 1.0 in quarter increments (0, 0.25, 0.5, 0.75, 1.0).",
            "This is not a cocktail bar. Don't stock like one.",
            "Shots are the profit center. Keep the shot bottles full.",
        ]

    def wine_by_glass(self):
        return [
            {"Producer": "Bota Box", "Wine": "Cabernet Sauvignon", "Type": "Red", "Region": "California", "Vintage": "NV", "Qty": 1, "Reorder_at": 1, "Par": 2, "Price": "$7", "Notes": "Box wine. No shame."},
            {"Producer": "Bota Box", "Wine": "Pinot Grigio", "Type": "White", "Region": "California", "Vintage": "NV", "Qty": 1, "Reorder_at": 1, "Par": 2, "Price": "$7", "Notes": "The white option."},
        ]

    def wine_by_bottle(self):
        return []

    def wine_notes(self):
        return [
            "Two options. Red or white. Don't overthink it.",
            "Box wine keeps longer and costs less. Perfect for a dive bar.",
            "If someone wants a wine list, they're in the wrong bar.",
        ]

    def vendors_distributors(self):
        return [
            {"Vendor": "Pacific Beverage Co", "Order_Day": "Monday", "Delivery_Day": "Wednesday", "Minimum": "$300", "Notes": "Main distributor. Beer, well spirits, mixers."},
            {"Vendor": "Golden Gate Distributing", "Order_Day": "Monday", "Delivery_Day": "Thursday", "Minimum": "$200", "Notes": "Backup spirits, wine boxes."},
        ]

    def vendors_direct(self):
        return [
            {"Vendor": "Restaurant Depot", "Contact": "", "Location": "Bayshore Blvd, SF", "Notes": "Bulk mixers, bar supplies, garnish."},
        ]

    def vendors_payment(self):
        return [
            {"Vendor": "Pacific Beverage Co", "Terms": "Net 30"},
            {"Vendor": "Golden Gate Distributing", "Terms": "COD"},
            {"Vendor": "Restaurant Depot", "Terms": "Cash/Card", "Notes": "Membership required."},
        ]

    def vendors_notes(self):
        return [
            "Two distributors is enough. Keep it simple.",
            "Restaurant Depot for bulk runs. Stock up on mixers and garnish monthly.",
            "If a rep tries to upsell craft spirits, politely decline. Know your bar.",
        ]

    def menu_cocktails(self):
        return []  # No cocktail menu at a dive bar

    def menu_beer_prices(self):
        return [
            {"What": "Draft pint", "Price": "$5-6"},
            {"What": "Tallboy (16oz can)", "Price": "$4"},
            {"What": "Bottles", "Price": "$5"},
            {"What": "PBR + shot combo", "Price": "$7"},
        ]

    def menu_wine_prices(self):
        return [
            {"What": "Glass (red or white)", "Price": "$7"},
        ]

    def menu_spirits_prices(self):
        return [
            {"Tier": "Well", "Price": "$6", "Notes": "Jim Beam, Smirnoff, New Amsterdam, Sauza, Bacardi"},
            {"Tier": "Jameson", "Price": "$7", "Notes": "Its own tier. Earned it."},
            {"Tier": "Call", "Price": "$8", "Notes": "Maker's, Espolon, Tullamore"},
            {"Tier": "Shot special", "Price": "$4", "Notes": "Changes nightly. Ask."},
        ]

    def menu_notes(self):
        return [
            "No cocktail menu. You get what's on the rail.",
            "Shot specials change when we feel like it.",
            "If you want a complicated drink, there's a cocktail bar two blocks over.",
        ]

    def staff_roster(self):
        return [
            {"Name": "Mick", "Role": "Bartender", "Max_Hours": 40, "Availability": "Mon-Sat", "RBS_Cert": "RBS-887412", "RBS_Expiry": "2027-03-15"},
            {"Name": "Dana", "Role": "Bartender", "Max_Hours": 35, "Availability": "Wed-Sun", "RBS_Cert": "RBS-223198", "RBS_Expiry": "2026-11-01"},
            {"Name": "Ricky", "Role": "Door/Barback", "Max_Hours": 25, "Availability": "Thu-Sat", "RBS_Cert": "", "RBS_Expiry": "--"},
        ]

    def schedule_current(self):
        return [
            {"Day": "Mon", "Shift": "Open", "Start": "14:00", "End": "02:00", "Staff": "Mick", "Role": "Bartender"},
            {"Day": "Tue", "Shift": "Open", "Start": "14:00", "End": "02:00", "Staff": "Mick", "Role": "Bartender"},
            {"Day": "Wed", "Shift": "Open", "Start": "14:00", "End": "02:00", "Staff": "Dana", "Role": "Bartender"},
            {"Day": "Thu", "Shift": "Open", "Start": "14:00", "End": "02:00", "Staff": "Dana", "Role": "Bartender"},
            {"Day": "Thu", "Shift": "Open", "Start": "20:00", "End": "02:00", "Staff": "Ricky", "Role": "Door"},
            {"Day": "Fri", "Shift": "Open", "Start": "14:00", "End": "02:00", "Staff": "Mick", "Role": "Bartender"},
            {"Day": "Fri", "Shift": "Open", "Start": "20:00", "End": "02:00", "Staff": "Ricky", "Role": "Door"},
            {"Day": "Sat", "Shift": "Open", "Start": "12:00", "End": "02:00", "Staff": "Mick", "Role": "Bartender"},
            {"Day": "Sat", "Shift": "Open", "Start": "20:00", "End": "02:00", "Staff": "Ricky", "Role": "Door"},
            {"Day": "Sun", "Shift": "Open", "Start": "12:00", "End": "22:00", "Staff": "Dana", "Role": "Bartender"},
        ]

    def opening_extras(self):
        return [
            "Jukebox powered on and tested",
            "Pool table -- check felt, rack balls, chalk stocked",
            "Check cash reserve -- this bar runs cash-heavy",
        ]

    def closing_extras(self):
        return [
            "Jukebox powered off",
            "Pool table -- rack balls, clean felt if needed",
            "Count cash carefully -- high cash volume means higher variance risk",
        ]

    def cooler_names(self):
        return ["Beer cooler"]
