# Cost Analysis Fixtures

All data is fictional.

## happy_path

A test menu with 2 cocktails, 2 beer tiers, 1 wine tier, 2 spirit tiers.
Some items trigger LOW_MARGIN (beer) and HIGH_POUR_COST (cocktail with extra ingredients).

## warn_case

A menu with underpriced items: expensive cocktail at $10, $5 draft beer, $6 well spirits.
Multiple HIGH_POUR_COST and LOW_MARGIN findings expected.
