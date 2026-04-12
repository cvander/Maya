"""Sports bar template - domestic drafts, wings, TVs everywhere, game night volume."""

from maya.seed.templates.base import BaseTemplate


class SportsBarTemplate(BaseTemplate):
    name = "Sports Bar"
    description = "Domestic drafts, wings, nachos. TVs everywhere. Happy hour specials. High volume on game nights."

    def beer_on_tap(self):
        return [
            {"Brewery": "Budweiser", "Beer": "Bud Light", "Style": "Light Lager", "Size": "1/2 bbl", "Qty": 3, "Reorder_at": 2, "Par": 4, "Notes": "The volume mover. Always on."},
            {"Brewery": "Coors", "Beer": "Coors Light", "Style": "Light Lager", "Size": "1/2 bbl", "Qty": 2, "Reorder_at": 1, "Par": 3, "Notes": "Second most popular."},
            {"Brewery": "Modelo", "Beer": "Especial", "Style": "Lager", "Size": "1/2 bbl", "Qty": 2, "Reorder_at": 1, "Par": 3, "Notes": "Steady mover."},
            {"Brewery": "Sierra Nevada", "Beer": "Pale Ale", "Style": "Pale Ale", "Size": "1/6 bbl", "Qty": 1, "Reorder_at": 1, "Par": 2, "Notes": "The craft option."},
            {"Brewery": "Lagunitas", "Beer": "IPA", "Style": "IPA", "Size": "1/6 bbl", "Qty": 1, "Reorder_at": 1, "Par": 2, "Notes": "IPA drinkers need a spot."},
            {"Brewery": "Guinness", "Beer": "Draught", "Style": "Stout", "Size": "1/6 bbl", "Qty": 1, "Reorder_at": 1, "Par": 2, "Notes": "Poured right. Patience."},
            {"Brewery": "Anchor Brewing", "Beer": "Anchor Steam", "Style": "California Common", "Size": "1/6 bbl", "Qty": 1, "Reorder_at": 1, "Par": 2, "Notes": "Local loyalty."},
            {"Brewery": "Fort Point Beer Co", "Beer": "KSA", "Style": "Kolsch", "Size": "1/6 bbl", "Qty": 1, "Reorder_at": 1, "Par": 2, "Notes": "Session beer. Moves well."},
        ]

    def beer_packaged(self):
        return [
            {"Brewery": "Budweiser", "Beer": "Budweiser", "Style": "Lager", "Format": "12oz bottle", "Qty": 36, "Reorder_at": 24, "Par": 48, "Notes": "Always stocked."},
            {"Brewery": "Corona", "Beer": "Extra", "Style": "Lager", "Format": "12oz bottle", "Qty": 24, "Reorder_at": 12, "Par": 36, "Notes": "With a lime."},
            {"Brewery": "Michelob", "Beer": "Ultra", "Style": "Light Lager", "Format": "12oz bottle", "Qty": 24, "Reorder_at": 12, "Par": 36, "Notes": "Low-cal crowd."},
            {"Brewery": "White Claw", "Beer": "Variety Pack", "Style": "Hard Seltzer", "Format": "12oz can", "Qty": 24, "Reorder_at": 12, "Par": 36, "Notes": "It sells. Stock it."},
            {"Brewery": "Athletic Brewing", "Beer": "Run Wild", "Style": "NA IPA", "Format": "12oz can", "Qty": 12, "Reorder_at": 6, "Par": 18, "Notes": "Designated drivers."},
        ]

    def beer_notes(self):
        return [
            "8 taps, domestic heavy. That's the sweet spot.",
            "Game nights burn through Bud Light and Coors Light. Double-check par before weekends.",
            "Keep a local option (Anchor, Fort Point) for the SF crowd.",
            "Bottled domestics are backup volume when kegs kick on big nights.",
        ]

    def spirits_well(self):
        return [
            {"Category": "Bourbon", "Brand": "Jim Beam", "Size": "1L", "Qty": 4, "Level": 0.5, "Reorder_at": 3, "Par": 6, "Notes": "Whiskey-coke. Jack-and-coke people get this."},
            {"Category": "Vodka", "Brand": "Smirnoff", "Size": "1L", "Qty": 4, "Level": 0.5, "Reorder_at": 3, "Par": 6, "Notes": "Vodka sodas all day."},
            {"Category": "Gin", "Brand": "New Amsterdam", "Size": "1L", "Qty": 2, "Level": 0.75, "Reorder_at": 1, "Par": 3, "Notes": "G&T."},
            {"Category": "Tequila", "Brand": "Sauza Silver", "Size": "1L", "Qty": 3, "Level": 0.5, "Reorder_at": 2, "Par": 4, "Notes": "Margs. Game night staple."},
            {"Category": "Rum", "Brand": "Bacardi Superior", "Size": "1L", "Qty": 2, "Level": 0.75, "Reorder_at": 1, "Par": 3, "Notes": "Rum and coke."},
        ]

    def spirits_call(self):
        return [
            {"Category": "Bourbon", "Brand": "Maker's Mark", "Size": "750ml", "Qty": 2, "Level": 0.5, "Reorder_at": 1, "Par": 3, "Price": "$9", "Notes": "Step-up bourbon."},
            {"Category": "Tequila", "Brand": "Patron Silver", "Size": "750ml", "Qty": 2, "Level": 0.5, "Reorder_at": 1, "Par": 3, "Price": "$10", "Notes": "Premium marg or shots."},
            {"Category": "Vodka", "Brand": "Tito's", "Size": "750ml", "Qty": 2, "Level": 0.75, "Reorder_at": 1, "Par": 3, "Price": "$9", "Notes": "Everyone asks for it."},
            {"Category": "Irish", "Brand": "Jameson", "Size": "750ml", "Qty": 2, "Level": 0.5, "Reorder_at": 1, "Par": 3, "Price": "$9", "Notes": "Shots. Always."},
        ]

    def spirits_modifiers(self):
        return [
            {"Item": "Angostura bitters", "Brand": "Angostura", "Size": "4oz", "Qty": 1, "Level": 0.5, "Reorder_at": 1, "Par": 2, "Notes": "Old Fashioned requests."},
            {"Item": "Simple syrup", "Brand": "Store-bought", "Size": "750ml", "Qty": 2, "Level": 0.75, "Reorder_at": 1, "Par": 3, "Notes": "Margaritas, whiskey sours."},
            {"Item": "Sweet & sour mix", "Brand": "Store-bought", "Size": "1L", "Qty": 2, "Level": 0.5, "Reorder_at": 2, "Par": 3, "Notes": "Volume margaritas. It works."},
        ]

    def spirits_mixers(self):
        return [
            {"Item": "Cola", "Brand": "Coca-Cola", "Size": "BIB", "Qty": 2, "Reorder_at": 1, "Notes": "Soda gun. High volume."},
            {"Item": "Diet Cola", "Brand": "Diet Coke", "Size": "BIB", "Qty": 1, "Reorder_at": 1, "Notes": "Soda gun."},
            {"Item": "Soda water", "Brand": "Soda gun", "Size": "BIB", "Qty": 1, "Reorder_at": 1, "Notes": ""},
            {"Item": "Tonic", "Brand": "Schweppes", "Size": "BIB", "Qty": 1, "Reorder_at": 1, "Notes": "Soda gun."},
            {"Item": "Ginger ale", "Brand": "Canada Dry", "Size": "BIB", "Qty": 1, "Reorder_at": 1, "Notes": "Soda gun."},
            {"Item": "Orange juice", "Brand": "Tropicana", "Size": "qt", "Qty": 3, "Reorder_at": 2, "Notes": "Screwdrivers, mimosas for Sunday brunch."},
            {"Item": "Cranberry juice", "Brand": "Ocean Spray", "Size": "32oz", "Qty": 3, "Reorder_at": 2, "Notes": ""},
            {"Item": "Limes", "Brand": "", "Size": "each", "Qty": 30, "Reorder_at": 15, "Notes": "Corona, margs. Goes fast on game nights."},
            {"Item": "Lemons", "Brand": "", "Size": "each", "Qty": 12, "Reorder_at": 6, "Notes": "Garnish."},
        ]

    def spirits_notes(self):
        return [
            "Count weekly, order Monday.",
            "Game nights triple normal volume. Pre-check pars on Friday.",
            "Level is 0 to 1.0 in quarter increments (0, 0.25, 0.5, 0.75, 1.0).",
            "Soda gun syrup runs out mid-rush if you don't check. Always have backup BIBs.",
            "Speed matters more than finesse here. Keep the rail tight.",
        ]

    def wine_by_glass(self):
        return [
            {"Producer": "Woodbridge", "Wine": "Cabernet Sauvignon", "Type": "Red", "Region": "California", "Vintage": "NV", "Qty": 2, "Reorder_at": 1, "Par": 3, "Price": "$9", "Notes": "House red."},
            {"Producer": "Woodbridge", "Wine": "Chardonnay", "Type": "White", "Region": "California", "Vintage": "NV", "Qty": 2, "Reorder_at": 1, "Par": 3, "Price": "$9", "Notes": "House white."},
            {"Producer": "La Marca", "Wine": "Prosecco", "Type": "Sparkling", "Region": "Italy", "Vintage": "NV", "Qty": 3, "Reorder_at": 2, "Par": 4, "Price": "$10", "Notes": "Mimosas on Sunday."},
        ]

    def wine_by_bottle(self):
        return []

    def wine_notes(self):
        return [
            "Three options. Red, white, bubbly. Keep it moving.",
            "Wine drinkers aren't the core crowd, but they show up with groups.",
            "Prosecco moves on Sundays. Stock up for football brunch.",
        ]

    def vendors_distributors(self):
        return [
            {"Vendor": "Pacific Beverage Co", "Order_Day": "Monday", "Delivery_Day": "Wednesday", "Minimum": "$500", "Notes": "Main beer distributor. Domestic kegs, bottles, spirits."},
            {"Vendor": "Golden Gate Distributing", "Order_Day": "Tuesday", "Delivery_Day": "Thursday", "Minimum": "$300", "Notes": "Wine, backup spirits, import beer."},
        ]

    def vendors_direct(self):
        return [
            {"Vendor": "Sysco", "Contact": "Account rep", "Location": "Delivery", "Notes": "Wings, nachos, fries, bar food supplies."},
            {"Vendor": "Restaurant Depot", "Contact": "", "Location": "Bayshore Blvd, SF", "Notes": "Backup food supplies, bulk mixers."},
        ]

    def vendors_payment(self):
        return [
            {"Vendor": "Pacific Beverage Co", "Terms": "Net 30"},
            {"Vendor": "Golden Gate Distributing", "Terms": "Net 30"},
            {"Vendor": "Sysco", "Terms": "Net 30"},
            {"Vendor": "Restaurant Depot", "Terms": "Cash/Card", "Notes": "Membership required."},
        ]

    def vendors_notes(self):
        return [
            "Two drink distributors, one food supplier. Simple.",
            "Order extra before big game weekends. Running out of Bud Light during the Super Bowl is a firing offense.",
            "Sysco delivers. Restaurant Depot for emergency runs.",
        ]

    def menu_cocktails(self):
        return [
            {
                "name": "Margarita",
                "ingredients": ["1.5 oz tequila (Sauza Silver)", "3 oz sweet & sour mix", "Salt rim (optional)"],
                "instruction": "Blended or on the rocks. Volume drink.",
                "price": 10,
            },
            {
                "name": "Long Island Iced Tea",
                "ingredients": ["0.5 oz vodka", "0.5 oz gin", "0.5 oz rum", "0.5 oz tequila", "Splash of cola", "Sour mix"],
                "instruction": "Shaken, tall glass. The game night classic.",
                "price": 12,
            },
        ]

    def menu_beer_prices(self):
        return [
            {"What": "Domestic draft pint", "Price": "$6"},
            {"What": "Craft draft pint", "Price": "$8"},
            {"What": "Domestic bottles", "Price": "$5"},
            {"What": "Import bottles", "Price": "$6"},
            {"What": "Hard seltzer", "Price": "$6"},
            {"What": "Happy hour draft (4-6pm)", "Price": "$4"},
        ]

    def menu_wine_prices(self):
        return [
            {"What": "House glass", "Price": "$9"},
            {"What": "Prosecco", "Price": "$10"},
        ]

    def menu_spirits_prices(self):
        return [
            {"Tier": "Well", "Price": "$7", "Notes": "Jim Beam, Smirnoff, New Amsterdam, Sauza, Bacardi"},
            {"Tier": "Call", "Price": "$9-10", "Notes": "Maker's, Patron, Tito's, Jameson"},
            {"Tier": "Happy hour well (4-6pm)", "Price": "$5", "Notes": ""},
        ]

    def menu_food(self):
        return [
            {"Item": "Wings (10 pc)", "Price": "$14", "Notes": "Buffalo, BBQ, garlic parm, or dry rub."},
            {"Item": "Wings (20 pc)", "Price": "$24", "Notes": "For the table."},
            {"Item": "Nachos", "Price": "$12", "Notes": "Loaded. Cheese, jalapenos, sour cream, guac."},
            {"Item": "Basket of fries", "Price": "$8", "Notes": "Seasoned."},
            {"Item": "Mozzarella sticks", "Price": "$10", "Notes": "With marinara."},
            {"Item": "Soft pretzel", "Price": "$9", "Notes": "With beer cheese."},
            {"Item": "Sliders (3 pc)", "Price": "$13", "Notes": "Beef, American cheese, pickles."},
        ]

    def menu_notes(self):
        return [
            "Happy hour: 4-6pm weekdays. $4 domestic drafts, $5 wells.",
            "Game night specials: wing + pitcher combos.",
            "Sunday brunch: mimosa pitchers $20.",
            "Food menu doesn't change much. People want consistency.",
        ]

    def staff_roster(self):
        return [
            {"Name": "Tony", "Role": "Bartender", "Max_Hours": 40, "Availability": "Mon-Sat", "RBS_Cert": "RBS-334521", "RBS_Expiry": "2027-04-10"},
            {"Name": "Maria", "Role": "Bartender", "Max_Hours": 35, "Availability": "Wed-Sun", "RBS_Cert": "RBS-667788", "RBS_Expiry": "2026-10-20"},
            {"Name": "Jake", "Role": "Bartender", "Max_Hours": 30, "Availability": "Thu-Sun", "RBS_Cert": "RBS-112233", "RBS_Expiry": "2027-01-05"},
            {"Name": "Priya", "Role": "Barback", "Max_Hours": 30, "Availability": "Wed-Sat", "RBS_Cert": "", "RBS_Expiry": "--"},
            {"Name": "Carlos", "Role": "Barback", "Max_Hours": 25, "Availability": "Fri-Sun", "RBS_Cert": "", "RBS_Expiry": "--"},
            {"Name": "Sophie", "Role": "Kitchen", "Max_Hours": 35, "Availability": "Mon-Fri", "RBS_Cert": "", "RBS_Expiry": "--"},
        ]

    def schedule_current(self):
        return [
            {"Day": "Mon", "Shift": "Open", "Start": "15:00", "End": "23:00", "Staff": "Tony", "Role": "Bartender"},
            {"Day": "Mon", "Shift": "Open", "Start": "15:00", "End": "23:00", "Staff": "Sophie", "Role": "Kitchen"},
            {"Day": "Tue", "Shift": "Open", "Start": "15:00", "End": "23:00", "Staff": "Tony", "Role": "Bartender"},
            {"Day": "Tue", "Shift": "Open", "Start": "15:00", "End": "23:00", "Staff": "Sophie", "Role": "Kitchen"},
            {"Day": "Wed", "Shift": "Open", "Start": "15:00", "End": "00:00", "Staff": "Maria", "Role": "Bartender"},
            {"Day": "Wed", "Shift": "Open", "Start": "15:00", "End": "00:00", "Staff": "Priya", "Role": "Barback"},
            {"Day": "Wed", "Shift": "Open", "Start": "15:00", "End": "23:00", "Staff": "Sophie", "Role": "Kitchen"},
            {"Day": "Thu", "Shift": "Open", "Start": "15:00", "End": "02:00", "Staff": "Tony", "Role": "Bartender"},
            {"Day": "Thu", "Shift": "Open", "Start": "15:00", "End": "02:00", "Staff": "Jake", "Role": "Bartender"},
            {"Day": "Thu", "Shift": "Open", "Start": "17:00", "End": "02:00", "Staff": "Priya", "Role": "Barback"},
            {"Day": "Thu", "Shift": "Open", "Start": "15:00", "End": "23:00", "Staff": "Sophie", "Role": "Kitchen"},
            {"Day": "Fri", "Shift": "Open", "Start": "15:00", "End": "02:00", "Staff": "Tony", "Role": "Bartender"},
            {"Day": "Fri", "Shift": "Open", "Start": "15:00", "End": "02:00", "Staff": "Maria", "Role": "Bartender"},
            {"Day": "Fri", "Shift": "Open", "Start": "17:00", "End": "02:00", "Staff": "Priya", "Role": "Barback"},
            {"Day": "Fri", "Shift": "Open", "Start": "17:00", "End": "02:00", "Staff": "Carlos", "Role": "Barback"},
            {"Day": "Fri", "Shift": "Open", "Start": "15:00", "End": "23:00", "Staff": "Sophie", "Role": "Kitchen"},
            {"Day": "Sat", "Shift": "Open", "Start": "11:00", "End": "02:00", "Staff": "Tony", "Role": "Bartender"},
            {"Day": "Sat", "Shift": "Open", "Start": "15:00", "End": "02:00", "Staff": "Jake", "Role": "Bartender"},
            {"Day": "Sat", "Shift": "Open", "Start": "17:00", "End": "02:00", "Staff": "Priya", "Role": "Barback"},
            {"Day": "Sat", "Shift": "Open", "Start": "17:00", "End": "02:00", "Staff": "Carlos", "Role": "Barback"},
            {"Day": "Sun", "Shift": "Open", "Start": "10:00", "End": "22:00", "Staff": "Maria", "Role": "Bartender"},
            {"Day": "Sun", "Shift": "Open", "Start": "10:00", "End": "22:00", "Staff": "Jake", "Role": "Bartender"},
            {"Day": "Sun", "Shift": "Open", "Start": "12:00", "End": "22:00", "Staff": "Carlos", "Role": "Barback"},
        ]

    def opening_extras(self):
        return [
            "TVs on -- check all screens, correct channels for today's games",
            "Sound system -- game audio to main speakers, music to bar speakers",
            "Check game schedule -- post today's matchups on the board",
            "Wings prepped, fryer on, kitchen mise en place",
            "Happy hour signage up",
        ]

    def closing_extras(self):
        return [
            "TVs off, remotes stored",
            "Kitchen closed out -- fryer off, hood off, surfaces sanitized",
            "Food inventory quick count -- wings, fries, buns",
            "Update tomorrow's game schedule on the board",
        ]

    def cooler_names(self):
        return ["Beer cooler", "Walk-in cooler", "Kitchen reach-in"]

    def calendar_events(self):
        events = super().calendar_events()
        # Add sports-specific events
        sports_events = [
            {"Date": "Feb (Super Bowl Sunday)", "Event": "Super Bowl", "Impact": "Highest volume day", "Notes": "Open early. Wings prepped double. Extra kegs. All hands."},
            {"Date": "Mar-Apr", "Event": "March Madness", "Impact": "High volume weekdays", "Notes": "Bracket specials. Lunch crowd on game days."},
            {"Date": "Apr (Opening Day)", "Event": "MLB Opening Day", "Impact": "High volume", "Notes": "Giants opener. SF goes orange."},
            {"Date": "Sep-Jan (Sundays)", "Event": "NFL Sundays", "Impact": "High volume weekly", "Notes": "Open early. Brunch + football. Pitcher specials."},
            {"Date": "Oct", "Event": "World Series / NBA Tipoff", "Impact": "Varies", "Notes": "If Warriors or Giants are in it, all bets are off."},
        ]
        # Replace the generic Super Bowl entry
        events = [e for e in events if e["Event"] != "Super Bowl"]
        return sports_events + events
