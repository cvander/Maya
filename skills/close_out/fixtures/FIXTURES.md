# Close-Out Fixtures

All data is fictional.

## happy_path

Balanced register: cash $850 + card $1200 = $2050, expected $2045 (variance +$5, within threshold).
Tips $320, waste: 5 limes, 2 beers.

## warn_case

Cash short: cash $825 + card $1200 = $2025, expected $2045 (variance -$20, triggers CASH_SHORT).
Tips $300, no waste.
