"""Cocktail lounge template - craft cocktails, small-batch spirits, house syrups."""

from maya.seed.templates.base import BaseTemplate


class CocktailLoungeTemplate(BaseTemplate):
    name = "Cocktail Lounge"
    description = "Craft cocktails, small-batch spirits, house syrups. Low lighting, vinyl."

    def beer_on_tap(self):
        return [
            {"Brewery": "Fort Point Beer Co", "Beer": "KSA", "Style": "Kolsch", "Size": "1/6 bbl", "Qty": 1, "Reorder_at": 1, "Par": 2, "Notes": "Session beer for guests who want a break from cocktails."},
            {"Brewery": "Cellarmaker Brewing", "Beer": "Tiny Pils", "Style": "Pilsner", "Size": "1/6 bbl", "Qty": 1, "Reorder_at": 1, "Par": 2, "Notes": "Hayes Valley. Clean, crisp."},
        ]

    def beer_packaged(self):
        return [
            {"Brewery": "Almanac Beer Co", "Beer": "Love Hazy IPA", "Style": "Hazy IPA", "Format": "16oz can", "Qty": 12, "Reorder_at": 6, "Par": 18, "Notes": "For the IPA crowd."},
            {"Brewery": "Athletic Brewing", "Beer": "Run Wild", "Style": "NA IPA", "Format": "12oz can", "Qty": 12, "Reorder_at": 6, "Par": 18, "Notes": "Non-alcoholic option. Moves well."},
        ]

    def beer_notes(self):
        return [
            "Beer is the supporting cast here, not the lead.",
            "Two taps, a few cans. Enough variety without competing with the cocktail program.",
            "Always have a non-alcoholic option. The designated driver deserves something good.",
        ]

    def spirits_well(self):
        return [
            {"Category": "Bourbon", "Brand": "Evan Williams BiB", "Size": "750ml", "Qty": 3, "Level": 0.5, "Reorder_at": 2, "Par": 4, "Notes": "Old Fashioned house pour. Bonded."},
            {"Category": "Rye", "Brand": "Rittenhouse BiB", "Size": "750ml", "Qty": 2, "Level": 0.5, "Reorder_at": 2, "Par": 3, "Notes": "Manhattans, Sazeracs."},
            {"Category": "Gin", "Brand": "Ford's Gin", "Size": "750ml", "Qty": 3, "Level": 0.75, "Reorder_at": 2, "Par": 4, "Notes": "Martini house pour. Built for cocktails."},
            {"Category": "Vodka", "Brand": "St. George All Purpose", "Size": "750ml", "Qty": 2, "Level": 0.5, "Reorder_at": 2, "Par": 3, "Notes": "Alameda distillery. Local."},
            {"Category": "Tequila", "Brand": "Cimarron Blanco", "Size": "1L", "Qty": 2, "Level": 0.75, "Reorder_at": 2, "Par": 3, "Notes": "Margarita base. Good value."},
            {"Category": "Rum (white)", "Brand": "Probitas", "Size": "750ml", "Qty": 2, "Level": 0.5, "Reorder_at": 2, "Par": 3, "Notes": "Daiquiri house pour."},
            {"Category": "Rum (aged)", "Brand": "Smith & Cross", "Size": "750ml", "Qty": 1, "Level": 0.75, "Reorder_at": 1, "Par": 2, "Notes": "Funky Jamaican. Tiki specs."},
            {"Category": "Mezcal", "Brand": "Banhez Espadin", "Size": "750ml", "Qty": 2, "Level": 0.5, "Reorder_at": 1, "Par": 3, "Notes": "House mezcal. Smoke without fire."},
            {"Category": "Scotch", "Brand": "Monkey Shoulder", "Size": "750ml", "Qty": 1, "Level": 1.0, "Reorder_at": 1, "Par": 2, "Notes": "Blended malt. Penicillin base."},
        ]

    def spirits_call(self):
        return [
            {"Category": "Bourbon", "Brand": "Buffalo Trace", "Size": "750ml", "Qty": 2, "Level": 0.5, "Reorder_at": 1, "Par": 3, "Price": "$14", "Notes": "Step-up Old Fashioned."},
            {"Category": "Bourbon", "Brand": "Elijah Craig Small Batch", "Size": "750ml", "Qty": 1, "Level": 0.75, "Reorder_at": 1, "Par": 2, "Price": "$16", "Notes": ""},
            {"Category": "Rye", "Brand": "Sazerac 6yr", "Size": "750ml", "Qty": 1, "Level": 0.5, "Reorder_at": 1, "Par": 2, "Price": "$15", "Notes": "Sazerac cocktail upgrade."},
            {"Category": "Gin", "Brand": "Hendrick's", "Size": "750ml", "Qty": 1, "Level": 0.5, "Reorder_at": 1, "Par": 2, "Price": "$15", "Notes": "Cucumber martini crowd."},
            {"Category": "Gin", "Brand": "St. George Terroir", "Size": "750ml", "Qty": 1, "Level": 0.75, "Reorder_at": 1, "Par": 2, "Price": "$16", "Notes": "Local. Tastes like NorCal forest."},
            {"Category": "Scotch", "Brand": "Laphroaig 10", "Size": "750ml", "Qty": 1, "Level": 0.75, "Reorder_at": 1, "Par": 2, "Price": "$18", "Notes": "Islay. Peat lovers know."},
            {"Category": "Tequila", "Brand": "Fortaleza Blanco", "Size": "750ml", "Qty": 1, "Level": 0.5, "Reorder_at": 1, "Par": 2, "Price": "$17", "Notes": "Sipping or premium margarita."},
            {"Category": "Mezcal", "Brand": "Del Maguey Vida", "Size": "750ml", "Qty": 1, "Level": 0.5, "Reorder_at": 1, "Par": 2, "Price": "$16", "Notes": "Step-up mezcal."},
            {"Category": "Rum", "Brand": "Ron Zacapa 23", "Size": "750ml", "Qty": 1, "Level": 0.5, "Reorder_at": 1, "Par": 2, "Price": "$18", "Notes": "Sipping rum. Old Fashioned riff."},
            {"Category": "Amaro", "Brand": "Montenegro", "Size": "750ml", "Qty": 1, "Level": 0.75, "Reorder_at": 1, "Par": 2, "Price": "$14", "Notes": "Paper Plane, Black Manhattan."},
        ]

    def spirits_modifiers(self):
        return [
            {"Item": "Angostura bitters", "Brand": "Angostura", "Size": "4oz", "Qty": 3, "Level": 0.5, "Reorder_at": 2, "Par": 4, "Notes": "Essential."},
            {"Item": "Orange bitters", "Brand": "Regan's No. 6", "Size": "5oz", "Qty": 2, "Level": 0.75, "Reorder_at": 1, "Par": 3, "Notes": ""},
            {"Item": "Peychaud's bitters", "Brand": "Peychaud's", "Size": "5oz", "Qty": 1, "Level": 0.5, "Reorder_at": 1, "Par": 2, "Notes": "Sazerac essential."},
            {"Item": "Dry vermouth", "Brand": "Dolin Dry", "Size": "750ml", "Qty": 2, "Level": 0.5, "Reorder_at": 1, "Par": 3, "Notes": "Refrigerate. 5 days max once open."},
            {"Item": "Sweet vermouth", "Brand": "Carpano Antica", "Size": "750ml", "Qty": 2, "Level": 0.5, "Reorder_at": 1, "Par": 3, "Notes": "Refrigerate. 5 days max once open."},
            {"Item": "Blanc vermouth", "Brand": "Dolin Blanc", "Size": "750ml", "Qty": 1, "Level": 0.75, "Reorder_at": 1, "Par": 2, "Notes": "Vesper, 50/50 Martini."},
            {"Item": "Maraschino", "Brand": "Luxardo", "Size": "750ml", "Qty": 1, "Level": 0.75, "Reorder_at": 1, "Par": 2, "Notes": "Last Word, Aviation."},
            {"Item": "Green Chartreuse", "Brand": "Chartreuse", "Size": "750ml", "Qty": 1, "Level": 0.5, "Reorder_at": 1, "Par": 1, "Notes": "Hard to find. Hoard it."},
            {"Item": "Campari", "Brand": "Campari", "Size": "750ml", "Qty": 1, "Level": 0.5, "Reorder_at": 1, "Par": 2, "Notes": "Negroni, Boulevardier."},
            {"Item": "Simple syrup", "Brand": "House-made", "Size": "750ml", "Qty": 2, "Level": 0.75, "Reorder_at": 1, "Par": 3, "Notes": "1:1 ratio. Make fresh weekly."},
            {"Item": "Rich demerara syrup", "Brand": "House-made", "Size": "750ml", "Qty": 1, "Level": 0.5, "Reorder_at": 1, "Par": 2, "Notes": "2:1 ratio. Old Fashioned, Jungle Bird."},
            {"Item": "Honey syrup", "Brand": "House-made", "Size": "750ml", "Qty": 1, "Level": 0.75, "Reorder_at": 1, "Par": 2, "Notes": "3:1 honey:water. Gold Rush, Bee's Knees."},
        ]

    def spirits_mixers(self):
        return [
            {"Item": "Soda water", "Brand": "Topo Chico", "Size": "12oz", "Qty": 48, "Reorder_at": 24, "Notes": "Glass bottles only."},
            {"Item": "Tonic", "Brand": "Fever-Tree", "Size": "200ml", "Qty": 24, "Reorder_at": 12, "Notes": "Premium tonic."},
            {"Item": "Ginger beer", "Brand": "Fever-Tree", "Size": "200ml", "Qty": 18, "Reorder_at": 12, "Notes": "Mules, Dark & Stormy."},
            {"Item": "Cola", "Brand": "Mexican Coke", "Size": "12oz", "Qty": 12, "Reorder_at": 6, "Notes": "Glass bottle, real sugar."},
            {"Item": "Lemons", "Brand": "", "Size": "each", "Qty": 40, "Reorder_at": 20, "Notes": "Juice + garnish. Goes fast."},
            {"Item": "Limes", "Brand": "", "Size": "each", "Qty": 50, "Reorder_at": 25, "Notes": "Juice + garnish. Goes faster."},
            {"Item": "Oranges", "Brand": "", "Size": "each", "Qty": 12, "Reorder_at": 6, "Notes": "Old Fashioned, garnish."},
            {"Item": "Grapefruit", "Brand": "", "Size": "each", "Qty": 8, "Reorder_at": 4, "Notes": "Paloma, Brown Derby."},
            {"Item": "Egg whites", "Brand": "Pasteurized", "Size": "qt", "Qty": 1, "Reorder_at": 1, "Notes": "Whiskey sour, clover club."},
            {"Item": "Olives", "Brand": "Castelvetrano", "Size": "jar", "Qty": 2, "Reorder_at": 1, "Notes": "Good olives matter."},
            {"Item": "Luxardo cherries", "Brand": "Luxardo", "Size": "jar", "Qty": 1, "Reorder_at": 1, "Notes": "Not the neon ones. Ever."},
        ]

    def spirits_notes(self):
        return [
            "Count weekly, order Monday.",
            "House-made syrups: make a batch every Monday. Label with date.",
            "Level is 0 to 1.0 in quarter increments (0, 0.25, 0.5, 0.75, 1.0).",
            "Vermouth and modifiers: check the Opened date. Past 5 days, pour it out.",
            "Chartreuse allocation is unpredictable. Buy it when you see it.",
            "Egg whites: pasteurized only. No cracking eggs during service.",
        ]

    def wine_by_glass(self):
        return [
            {"Producer": "Scribe Winery", "Wine": "Pinot Noir", "Type": "Red", "Region": "Sonoma", "Vintage": "2023", "Qty": 2, "Reorder_at": 1, "Par": 3, "Price": "$16", "Notes": "Carneros. Elegant."},
            {"Producer": "Pax Wines", "Wine": "Chenin Blanc", "Type": "White", "Region": "Sonoma", "Vintage": "2023", "Qty": 2, "Reorder_at": 1, "Par": 3, "Price": "$15", "Notes": "Interesting white. Conversation starter."},
            {"Producer": "Matthiasson", "Wine": "Rose", "Type": "Rose", "Region": "Napa", "Vintage": "2024", "Qty": 2, "Reorder_at": 1, "Par": 3, "Price": "$14", "Notes": "Dry. Not sweet."},
            {"Producer": "Cruse Wine Co", "Wine": "Sparkling", "Type": "Sparkling", "Region": "North Coast", "Vintage": "NV", "Qty": 3, "Reorder_at": 2, "Par": 4, "Price": "$16", "Notes": "Pet-nat. Good start to the night."},
        ]

    def wine_by_bottle(self):
        return [
            {"Producer": "Turley Wine Cellars", "Wine": "Zinfandel", "Type": "Red", "Region": "Paso Robles", "Vintage": "2022", "Qty": 2, "Reorder_at": 1, "Par": 3, "Price": "$60", "Notes": "Big wine for a big night."},
            {"Producer": "Lioco", "Wine": "Chardonnay", "Type": "White", "Region": "Sonoma", "Vintage": "2023", "Qty": 2, "Reorder_at": 1, "Par": 3, "Price": "$50", "Notes": "Unoaked. For people who say they don't like Chardonnay."},
        ]

    def wine_notes(self):
        return [
            "Small list, intentional. The cocktails are the draw, but the wine should be worth drinking.",
            "California producers preferred.",
            "Always have a sparkling option. Opens conversations and tabs.",
            "Open bottles: 3 days max for whites/rose, 5 days for reds.",
        ]

    def vendors_distributors(self):
        return [
            {"Vendor": "Southern Glazer's", "Order_Day": "Monday", "Delivery_Day": "Wednesday", "Minimum": "$500", "Notes": "Main spirits. Well + most call."},
            {"Vendor": "Young's Market", "Order_Day": "Monday", "Delivery_Day": "Thursday", "Minimum": "$300", "Notes": "Wine, craft spirits, amari."},
            {"Vendor": "Anchor Distributing", "Order_Day": "Tuesday", "Delivery_Day": "Thursday", "Minimum": "$200", "Notes": "Local beer. Fort Point, Almanac."},
            {"Vendor": "The Spirit Guild", "Order_Day": "Wednesday", "Delivery_Day": "Friday", "Minimum": "$200", "Notes": "Small-batch spirits, specialty modifiers."},
        ]

    def vendors_direct(self):
        return [
            {"Vendor": "Cellarmaker Brewing", "Contact": "Taproom", "Location": "Hayes Valley", "Notes": "Walk-in for kegs. Call ahead."},
            {"Vendor": "Farmers market", "Contact": "", "Location": "Ferry Building, Tuesdays", "Notes": "Citrus, herbs, seasonal garnish."},
        ]

    def vendors_payment(self):
        return [
            {"Vendor": "Southern Glazer's", "Terms": "Net 30"},
            {"Vendor": "Young's Market", "Terms": "Net 30"},
            {"Vendor": "Anchor Distributing", "Terms": "COD"},
            {"Vendor": "The Spirit Guild", "Terms": "Net 15", "Notes": "Smaller outfit, shorter terms."},
        ]

    def menu_cocktails(self):
        return [
            {
                "name": "Old Fashioned",
                "ingredients": ["2 oz bourbon (Evan Williams BiB)", "1 demerara sugar cube", "2-3 dashes Angostura bitters", "Orange peel", "Large ice cube"],
                "instruction": "No cherry. No soda. Keep it honest.",
                "price": 16,
            },
            {
                "name": "Dry Martini",
                "ingredients": ["2.5 oz gin (Ford's)", "0.5 oz dry vermouth (Dolin)", "Lemon twist or olive"],
                "instruction": "Stirred, not shaken. Cold glass.",
                "price": 17,
            },
            {
                "name": "Daiquiri",
                "ingredients": ["2 oz white rum (Probitas)", "1 oz fresh lime juice", "0.75 oz simple syrup"],
                "instruction": "Shaken hard. Served up. The real daiquiri.",
                "price": 16,
            },
            {
                "name": "Last Word",
                "ingredients": ["0.75 oz gin (Ford's)", "0.75 oz Green Chartreuse", "0.75 oz Luxardo maraschino", "0.75 oz fresh lime juice"],
                "instruction": "Equal parts. Shaken. A classic for a reason.",
                "price": 18,
            },
            {
                "name": "Paper Plane",
                "ingredients": ["0.75 oz bourbon (Evan Williams BiB)", "0.75 oz Aperol", "0.75 oz Amaro Montenegro", "0.75 oz fresh lemon juice"],
                "instruction": "Equal parts. Shaken. Bittersweet and bright.",
                "price": 17,
            },
            {
                "name": "Penicillin",
                "ingredients": ["2 oz scotch (Monkey Shoulder)", "0.75 oz fresh lemon juice", "0.75 oz honey-ginger syrup", "0.25 oz Laphroaig 10 float"],
                "instruction": "Shaken, large ice, Islay float. Smoky and medicinal in the best way.",
                "price": 18,
            },
            {
                "name": "Negroni",
                "ingredients": ["1 oz gin (Ford's)", "1 oz Campari", "1 oz sweet vermouth (Carpano Antica)", "Orange peel"],
                "instruction": "Stirred, served on a big rock.",
                "price": 16,
            },
            {
                "name": "Gold Rush",
                "ingredients": ["2 oz bourbon (Evan Williams BiB)", "0.75 oz fresh lemon juice", "0.75 oz honey syrup"],
                "instruction": "Shaken. A whiskey sour that grew up.",
                "price": 16,
            },
        ]

    def menu_beer_prices(self):
        return [
            {"What": "Draft pint", "Price": "$8"},
            {"What": "Cans", "Price": "$8-9"},
        ]

    def menu_wine_prices(self):
        return [
            {"What": "Glass", "Price": "$14-16"},
            {"What": "Bottle", "Price": "$50-60"},
            {"What": "Sparkling", "Price": "$16"},
        ]

    def menu_spirits_prices(self):
        return [
            {"Tier": "Well", "Price": "$12", "Notes": "Evan Williams, Rittenhouse, Ford's, St. George, Cimarron, Probitas"},
            {"Tier": "Call", "Price": "$14-18", "Notes": "See spirits list."},
        ]

    def menu_notes(self):
        return [
            "The menu rotates seasonally. House cocktails change every 6-8 weeks.",
            "Classics are always available, even if not on the printed menu.",
            "If a guest has a preference but no order, the bartender builds something. That's the point.",
            "Buy-outs and seasonal specs get a spot until they're gone.",
        ]

    def staff_roster(self):
        return [
            {"Name": "Ellis", "Role": "Head Bartender", "Max_Hours": 40, "Availability": "Tue-Sat", "RBS_Cert": "RBS-441277", "RBS_Expiry": "2027-06-01"},
            {"Name": "Noor", "Role": "Bartender", "Max_Hours": 35, "Availability": "Wed-Sun", "RBS_Cert": "RBS-558903", "RBS_Expiry": "2026-12-15"},
            {"Name": "Jamie", "Role": "Bartender", "Max_Hours": 30, "Availability": "Mon-Fri", "RBS_Cert": "RBS-672341", "RBS_Expiry": "2027-02-28"},
            {"Name": "Leo", "Role": "Barback", "Max_Hours": 30, "Availability": "Wed-Sat", "RBS_Cert": "", "RBS_Expiry": "--"},
            {"Name": "Ava", "Role": "Barback", "Max_Hours": 25, "Availability": "Fri-Sun", "RBS_Cert": "", "RBS_Expiry": "--"},
        ]

    def schedule_current(self):
        return [
            {"Day": "Mon", "Shift": "Open", "Start": "17:00", "End": "01:00", "Staff": "Jamie", "Role": "Bartender"},
            {"Day": "Tue", "Shift": "Open", "Start": "17:00", "End": "01:00", "Staff": "Ellis", "Role": "Bartender"},
            {"Day": "Wed", "Shift": "Open", "Start": "17:00", "End": "02:00", "Staff": "Ellis", "Role": "Bartender"},
            {"Day": "Wed", "Shift": "Open", "Start": "17:00", "End": "02:00", "Staff": "Leo", "Role": "Barback"},
            {"Day": "Thu", "Shift": "Open", "Start": "17:00", "End": "02:00", "Staff": "Noor", "Role": "Bartender"},
            {"Day": "Thu", "Shift": "Open", "Start": "17:00", "End": "02:00", "Staff": "Leo", "Role": "Barback"},
            {"Day": "Fri", "Shift": "Open", "Start": "17:00", "End": "02:00", "Staff": "Ellis", "Role": "Bartender"},
            {"Day": "Fri", "Shift": "Open", "Start": "17:00", "End": "02:00", "Staff": "Jamie", "Role": "Bartender"},
            {"Day": "Fri", "Shift": "Open", "Start": "19:00", "End": "02:00", "Staff": "Leo", "Role": "Barback"},
            {"Day": "Fri", "Shift": "Open", "Start": "19:00", "End": "02:00", "Staff": "Ava", "Role": "Barback"},
            {"Day": "Sat", "Shift": "Open", "Start": "17:00", "End": "02:00", "Staff": "Ellis", "Role": "Bartender"},
            {"Day": "Sat", "Shift": "Open", "Start": "17:00", "End": "02:00", "Staff": "Noor", "Role": "Bartender"},
            {"Day": "Sat", "Shift": "Open", "Start": "19:00", "End": "02:00", "Staff": "Leo", "Role": "Barback"},
            {"Day": "Sat", "Shift": "Open", "Start": "19:00", "End": "02:00", "Staff": "Ava", "Role": "Barback"},
            {"Day": "Sun", "Shift": "Open", "Start": "17:00", "End": "00:00", "Staff": "Noor", "Role": "Bartender"},
            {"Day": "Sun", "Shift": "Open", "Start": "17:00", "End": "00:00", "Staff": "Ava", "Role": "Barback"},
        ]

    def opening_extras(self):
        return [
            "Prep house syrups if running low (simple, demerara, honey)",
            "Check vermouth -- Opened date, 5 days max",
            "Juice citrus: lemons, limes, grapefruit",
            "Egg whites portioned and chilled",
            "Vinyl on, volume low",
            "Candles lit, lighting set to evening level",
        ]

    def closing_extras(self):
        return [
            "Strain and store fresh juice (label with date)",
            "Cap all house syrups, refrigerate",
            "Wipe down cocktail tools (jiggers, shakers, strainers)",
            "Blow out candles",
        ]

    def cooler_names(self):
        return ["Beer cooler", "Wine fridge"]
