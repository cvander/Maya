"""Wine bar template - California wines, charcuterie, cheese, wine flights."""

from maya.seed.templates.base import BaseTemplate


class WineBarTemplate(BaseTemplate):
    name = "Wine Bar"
    description = "California wines by the glass and bottle, charcuterie, cheese. Intimate. Wine flights."

    def beer_on_tap(self):
        return [
            {"Brewery": "Fort Point Beer Co", "Beer": "KSA", "Style": "Kolsch", "Size": "1/6 bbl", "Qty": 1, "Reorder_at": 1, "Par": 2, "Notes": "For the non-wine drinker in the group."},
        ]

    def beer_packaged(self):
        return [
            {"Brewery": "Almanac Beer Co", "Beer": "Love Hazy IPA", "Style": "Hazy IPA", "Format": "16oz can", "Qty": 6, "Reorder_at": 3, "Par": 12, "Notes": "Craft option."},
            {"Brewery": "Athletic Brewing", "Beer": "Run Wild", "Style": "NA IPA", "Format": "12oz can", "Qty": 12, "Reorder_at": 6, "Par": 18, "Notes": "Non-alcoholic. Important to have."},
        ]

    def beer_notes(self):
        return [
            "Beer is an afterthought here, and that's OK.",
            "One tap, two cans. Enough to not lose the group when one person doesn't drink wine.",
            "Non-alcoholic option is essential. Wine bars attract mixed groups.",
        ]

    def spirits_well(self):
        return [
            {"Category": "Brandy", "Brand": "Germain-Robin", "Size": "750ml", "Qty": 1, "Level": 0.75, "Reorder_at": 1, "Par": 2, "Notes": "California brandy. Pairs with the wine program."},
            {"Category": "Gin", "Brand": "St. George Botanivore", "Size": "750ml", "Qty": 1, "Level": 0.5, "Reorder_at": 1, "Par": 2, "Notes": "For G&T requests. Local."},
            {"Category": "Bourbon", "Brand": "Evan Williams BiB", "Size": "750ml", "Qty": 1, "Level": 0.75, "Reorder_at": 1, "Par": 2, "Notes": "For the occasional Old Fashioned."},
        ]

    def spirits_call(self):
        return [
            {"Category": "Grappa", "Brand": "Nardini Bianca", "Size": "750ml", "Qty": 1, "Level": 0.75, "Reorder_at": 1, "Par": 1, "Price": "$14", "Notes": "Digestif. Pairs with cheese."},
            {"Category": "Port", "Brand": "Graham's 10yr Tawny", "Size": "750ml", "Qty": 1, "Level": 0.5, "Reorder_at": 1, "Par": 2, "Price": "$14", "Notes": "Dessert pour."},
            {"Category": "Sherry", "Brand": "Lustau Amontillado", "Size": "750ml", "Qty": 1, "Level": 0.75, "Reorder_at": 1, "Par": 2, "Price": "$12", "Notes": "Nutty, dry. Underrated."},
            {"Category": "Amaro", "Brand": "Averna", "Size": "750ml", "Qty": 1, "Level": 0.5, "Reorder_at": 1, "Par": 2, "Price": "$12", "Notes": "After-dinner bitter."},
        ]

    def spirits_modifiers(self):
        return []

    def spirits_mixers(self):
        return [
            {"Item": "Sparkling water", "Brand": "Topo Chico", "Size": "12oz", "Qty": 36, "Reorder_at": 18, "Notes": "Glass bottles. Palate cleanser."},
            {"Item": "Still water", "Brand": "Tap, filtered", "Size": "carafe", "Qty": 0, "Reorder_at": 0, "Notes": "Always on the table. No charge."},
            {"Item": "Olives", "Brand": "Castelvetrano", "Size": "jar", "Qty": 3, "Reorder_at": 2, "Notes": "Warm with citrus zest. Bar snack."},
            {"Item": "Marcona almonds", "Brand": "", "Size": "lb", "Qty": 2, "Reorder_at": 1, "Notes": "Roasted, salted. Free bar snack."},
        ]

    def spirits_notes(self):
        return [
            "Spirits are a side note here. Wine is the program.",
            "Fortified wines (sherry, port) bridge wine and spirits. Worth stocking.",
            "Grappa and amaro for after dinner. Natural extensions of the wine program.",
            "Level is 0 to 1.0 in quarter increments (0, 0.25, 0.5, 0.75, 1.0).",
        ]

    def wine_by_glass(self):
        return [
            {"Producer": "Scribe Winery", "Wine": "Pinot Noir", "Type": "Red", "Region": "Sonoma, Carneros", "Vintage": "2023", "Qty": 3, "Reorder_at": 2, "Par": 4, "Price": "$18", "Notes": "Elegant, light body. Gateway Pinot."},
            {"Producer": "Ridge Vineyards", "Wine": "Three Valleys", "Type": "Red", "Region": "Sonoma", "Vintage": "2022", "Qty": 2, "Reorder_at": 1, "Par": 3, "Price": "$17", "Notes": "Zin blend. Regulars love it."},
            {"Producer": "Bedrock Wine Co", "Wine": "Old Vine Zinfandel", "Type": "Red", "Region": "Sonoma", "Vintage": "2022", "Qty": 2, "Reorder_at": 1, "Par": 3, "Price": "$18", "Notes": "Heritage vines. Rich, layered."},
            {"Producer": "Arnot-Roberts", "Wine": "Trousseau", "Type": "Red", "Region": "North Coast", "Vintage": "2023", "Qty": 2, "Reorder_at": 1, "Par": 3, "Price": "$19", "Notes": "Light red. Serve slightly chilled."},
            {"Producer": "Pax Wines", "Wine": "Chenin Blanc", "Type": "White", "Region": "Sonoma", "Vintage": "2023", "Qty": 3, "Reorder_at": 2, "Par": 4, "Price": "$17", "Notes": "Conversation starter. Textured."},
            {"Producer": "Lioco", "Wine": "Chardonnay", "Type": "White", "Region": "Sonoma", "Vintage": "2023", "Qty": 2, "Reorder_at": 1, "Par": 3, "Price": "$16", "Notes": "Unoaked. Changes minds about Chardonnay."},
            {"Producer": "Broc Cellars", "Wine": "Love White", "Type": "White Blend", "Region": "Mendocino", "Vintage": "2023", "Qty": 2, "Reorder_at": 1, "Par": 3, "Price": "$16", "Notes": "Natural wine. Fun, easy."},
            {"Producer": "Matthiasson", "Wine": "Rose", "Type": "Rose", "Region": "Napa", "Vintage": "2024", "Qty": 3, "Reorder_at": 2, "Par": 4, "Price": "$15", "Notes": "Dry. Not sweet. That matters."},
            {"Producer": "Cruse Wine Co", "Wine": "Pet-Nat", "Type": "Sparkling", "Region": "North Coast", "Vintage": "NV", "Qty": 4, "Reorder_at": 2, "Par": 5, "Price": "$17", "Notes": "Natural sparkling. Opens conversations."},
            {"Producer": "Schramsberg", "Wine": "Blanc de Blancs", "Type": "Sparkling", "Region": "Napa", "Vintage": "2020", "Qty": 3, "Reorder_at": 2, "Par": 4, "Price": "$20", "Notes": "California's answer to Champagne."},
        ]

    def wine_by_bottle(self):
        return [
            {"Producer": "Turley Wine Cellars", "Wine": "Zinfandel", "Type": "Red", "Region": "Paso Robles", "Vintage": "2022", "Qty": 3, "Reorder_at": 2, "Par": 4, "Price": "$55", "Notes": "Big wine for a big night."},
            {"Producer": "Sandhi Wines", "Wine": "Pinot Noir", "Type": "Red", "Region": "Sta. Rita Hills", "Vintage": "2022", "Qty": 2, "Reorder_at": 1, "Par": 3, "Price": "$65", "Notes": "Central Coast. Burgundian style."},
            {"Producer": "Hirsch Vineyards", "Wine": "Pinot Noir", "Type": "Red", "Region": "Sonoma Coast", "Vintage": "2021", "Qty": 2, "Reorder_at": 1, "Par": 2, "Price": "$85", "Notes": "Special occasion. Remarkable."},
            {"Producer": "Stony Hill", "Wine": "Chardonnay", "Type": "White", "Region": "Napa", "Vintage": "2022", "Qty": 2, "Reorder_at": 1, "Par": 3, "Price": "$60", "Notes": "Old-school Napa Chard. Restrained."},
            {"Producer": "Domaine Chandon", "Wine": "Brut", "Type": "Sparkling", "Region": "Napa", "Vintage": "NV", "Qty": 4, "Reorder_at": 2, "Par": 5, "Price": "$50", "Notes": "Celebrations."},
            {"Producer": "Tablas Creek", "Wine": "Patelin de Tablas Blanc", "Type": "White Blend", "Region": "Paso Robles", "Vintage": "2023", "Qty": 2, "Reorder_at": 1, "Par": 3, "Price": "$42", "Notes": "Rhone style. Pairs with everything."},
        ]

    def wine_notes(self):
        return [
            "California producers, almost exclusively. This is the program.",
            "By-the-glass list rotates every 2-3 weeks. Keep it fresh.",
            "Wine flights are a big draw. Change themes monthly (region, varietal, producer).",
            "Open bottles: 3 days max for whites/rose, 5 days for reds. Coravin on bottles over $60.",
            "Regulars are trusted advisors. They know the local producers.",
            "When something's gone, it's gone. Don't hold a spot for it unless it's coming back.",
            "Natural wine gets its own section when we have 3+ options open.",
        ]

    def vendors_distributors(self):
        return [
            {"Vendor": "Young's Market", "Order_Day": "Monday", "Delivery_Day": "Wednesday", "Minimum": "$400", "Notes": "Main wine distributor. Broad California portfolio."},
            {"Vendor": "Henry Wine Group", "Order_Day": "Monday", "Delivery_Day": "Thursday", "Minimum": "$300", "Notes": "Small producers. Arnot-Roberts, Broc, Cruse."},
            {"Vendor": "Wine Warehouse", "Order_Day": "Tuesday", "Delivery_Day": "Friday", "Minimum": "$250", "Notes": "Backup, import wines, fortified."},
        ]

    def vendors_direct(self):
        return [
            {"Vendor": "Scribe Winery", "Contact": "Wine club", "Phone": "", "Location": "Sonoma", "Notes": "Allocation. Order when available."},
            {"Vendor": "Ridge Vineyards", "Contact": "Trade account", "Phone": "", "Location": "Cupertino", "Notes": "Direct account. Better pricing on case lots."},
            {"Vendor": "Cheese Plus", "Contact": "Counter", "Phone": "", "Location": "Russian Hill, SF", "Notes": "Specialty cheese, charcuterie. Walk-in or call."},
            {"Vendor": "Boccalone", "Contact": "Orders", "Phone": "", "Location": "Ferry Building, SF", "Notes": "Local salumi. Pairs with everything."},
        ]

    def vendors_payment(self):
        return [
            {"Vendor": "Young's Market", "Terms": "Net 30"},
            {"Vendor": "Henry Wine Group", "Terms": "Net 30"},
            {"Vendor": "Wine Warehouse", "Terms": "Net 30"},
            {"Vendor": "Cheese Plus", "Terms": "COD"},
            {"Vendor": "Boccalone", "Terms": "COD"},
        ]

    def vendors_notes(self):
        return [
            "Three wine distributors covers the program. Each has different strengths.",
            "Direct relationships with wineries get you allocations. Worth the effort.",
            "Cheese and charcuterie quality defines the food program. Don't cheap out.",
            "Taste before buying. Every bottle. No exceptions.",
        ]

    def menu_cocktails(self):
        return [
            {
                "name": "Aperol Spritz",
                "ingredients": ["3 oz Prosecco", "2 oz Aperol", "1 oz soda water", "Orange slice"],
                "instruction": "Build in a wine glass over ice.",
                "price": 14,
            },
            {
                "name": "Kir Royale",
                "ingredients": ["5 oz sparkling wine (Domaine Chandon)", "0.5 oz creme de cassis"],
                "instruction": "Pour cassis first, top with bubbly.",
                "price": 16,
            },
        ]

    def menu_beer_prices(self):
        return [
            {"What": "Draft pint", "Price": "$8"},
            {"What": "Cans", "Price": "$7-8"},
        ]

    def menu_wine_prices(self):
        return [
            {"What": "Glass (red)", "Price": "$16-19"},
            {"What": "Glass (white/rose)", "Price": "$15-17"},
            {"What": "Glass (sparkling)", "Price": "$17-20"},
            {"What": "Flight (3 wines)", "Price": "$22-28"},
            {"What": "Bottle", "Price": "$42-85"},
        ]

    def menu_spirits_prices(self):
        return [
            {"Tier": "Brandy / Grappa", "Price": "$14", "Notes": "Digestif."},
            {"Tier": "Port / Sherry", "Price": "$12-14", "Notes": "Fortified wines."},
            {"Tier": "Amaro", "Price": "$12", "Notes": "After dinner."},
        ]

    def menu_food(self):
        return [
            {"Item": "Cheese board (3 selections)", "Price": "$22", "Notes": "Rotating. Ask what's on today."},
            {"Item": "Charcuterie board", "Price": "$24", "Notes": "Local salumi, mustard, cornichons."},
            {"Item": "Mixed board (cheese + meat)", "Price": "$32", "Notes": "The full spread."},
            {"Item": "Warm olives", "Price": "$8", "Notes": "Castelvetrano, citrus, herbs."},
            {"Item": "Marcona almonds", "Price": "$7", "Notes": "Roasted, sea salt."},
            {"Item": "Flatbread", "Price": "$14", "Notes": "Seasonal toppings. Changes weekly."},
        ]

    def menu_notes(self):
        return [
            "Wine list rotates every 2-3 weeks. Flights change monthly.",
            "Cheese and charcuterie boards are the anchor food. Quality over quantity.",
            "Seasonal pairings: suggest a wine with each board.",
            "If a regular brings a bottle (corkage $25), welcome it. It starts a conversation.",
        ]

    def staff_roster(self):
        return [
            {"Name": "Margaux", "Role": "Sommelier/Bartender", "Max_Hours": 40, "Availability": "Tue-Sat", "RBS_Cert": "RBS-991122", "RBS_Expiry": "2027-08-15"},
            {"Name": "Reed", "Role": "Bartender", "Max_Hours": 35, "Availability": "Wed-Sun", "RBS_Cert": "RBS-443355", "RBS_Expiry": "2027-01-20"},
            {"Name": "Ivy", "Role": "Bartender", "Max_Hours": 30, "Availability": "Mon-Thu", "RBS_Cert": "RBS-778899", "RBS_Expiry": "2026-09-10"},
            {"Name": "Theo", "Role": "Barback/Food Prep", "Max_Hours": 25, "Availability": "Thu-Sat", "RBS_Cert": "", "RBS_Expiry": "--"},
        ]

    def schedule_current(self):
        return [
            {"Day": "Mon", "Shift": "Open", "Start": "16:00", "End": "22:00", "Staff": "Ivy", "Role": "Bartender"},
            {"Day": "Tue", "Shift": "Open", "Start": "16:00", "End": "23:00", "Staff": "Margaux", "Role": "Bartender"},
            {"Day": "Wed", "Shift": "Open", "Start": "16:00", "End": "23:00", "Staff": "Reed", "Role": "Bartender"},
            {"Day": "Thu", "Shift": "Open", "Start": "16:00", "End": "00:00", "Staff": "Margaux", "Role": "Bartender"},
            {"Day": "Thu", "Shift": "Open", "Start": "17:00", "End": "00:00", "Staff": "Theo", "Role": "Barback"},
            {"Day": "Fri", "Shift": "Open", "Start": "16:00", "End": "00:00", "Staff": "Margaux", "Role": "Bartender"},
            {"Day": "Fri", "Shift": "Open", "Start": "16:00", "End": "00:00", "Staff": "Reed", "Role": "Bartender"},
            {"Day": "Fri", "Shift": "Open", "Start": "17:00", "End": "00:00", "Staff": "Theo", "Role": "Barback"},
            {"Day": "Sat", "Shift": "Open", "Start": "15:00", "End": "00:00", "Staff": "Margaux", "Role": "Bartender"},
            {"Day": "Sat", "Shift": "Open", "Start": "15:00", "End": "00:00", "Staff": "Reed", "Role": "Bartender"},
            {"Day": "Sat", "Shift": "Open", "Start": "16:00", "End": "00:00", "Staff": "Theo", "Role": "Barback"},
            {"Day": "Sun", "Shift": "Open", "Start": "15:00", "End": "22:00", "Staff": "Reed", "Role": "Bartender"},
        ]

    def opening_extras(self):
        return [
            "Pull wines for by-the-glass -- check Opened dates, discard if past 3 days (white) or 5 days (red)",
            "Cheese and charcuterie: pull from walk-in, temper to room temp (30 min before service)",
            "Wine flight of the week -- set up tasting mats and pour cards",
            "Coravin check -- gas capsule level, needle clean",
            "Polish wine glasses (stems, no spots)",
        ]

    def closing_extras(self):
        return [
            "Re-cork all open wines, refrigerate whites and rose",
            "Wrap and refrigerate cheese and charcuterie",
            "Update wine inventory -- mark any bottles that finished tonight",
            "Clean Coravin needle",
        ]

    def cooler_names(self):
        return ["Wine fridge (white/rose)", "Wine fridge (sparkling)", "Walk-in cooler"]

    def calendar_events(self):
        events = super().calendar_events()
        wine_events = [
            {"Date": "Mar (variable)", "Event": "Zinfandel Experience", "Impact": "Theme week", "Notes": "Zin flight, invite local producers."},
            {"Date": "May", "Event": "California Wine Month", "Impact": "Feature month", "Notes": "All-California focus. Discounted flights."},
            {"Date": "Aug (variable)", "Event": "Sonoma Harvest", "Impact": "Theme week", "Notes": "New vintage releases. Winemaker dinner if possible."},
            {"Date": "Nov (3rd Thursday)", "Event": "Beaujolais Nouveau Day", "Impact": "Special event", "Notes": "Exception to the California-only rule. One night."},
        ]
        return events + wine_events
