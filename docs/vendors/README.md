# Vendors

Who supplies what, when to order, and who to call.

---

## Distributors

| Vendor | Rep | Phone | Email | Order Day | Delivery Day | Minimum | Account # | Notes |
|--------|-----|-------|-------|-----------|-------------|---------|-----------|-------|
| Southern Glazer's | | | | Monday | Wednesday | $500 | | Main spirits distributor. Covers well + most call. |
| Young's Market | | | | Monday | Thursday | $300 | | Wine, some craft spirits. |
| Anchor Distributing | | | | Tuesday | Thursday | $200 | | Local beer focus. Anchor, Fort Point, Almanac. |
| City Beer | | | | Wednesday | Friday | 2 cases | | Craft cans/bottles only. Walk-in option too. |

## Direct / Walk-In

| Vendor | Contact | Phone | Location | Notes |
|--------|---------|-------|----------|-------|
| Cellarmaker Brewing | Taproom | | Hayes Valley | No distributor. Walk-in purchase only. Call ahead for kegs. |
| Barebottle Brewing | Taproom | | Bernal Heights | Same. Walk-in for kegs, call 1 week ahead. |
| Produce (lemons, limes, oranges) | | | Farmers market / Restaurant Depot | Tuesday farmers market or Restaurant Depot on Bayshore. |

## Order Workflow

1. **Sunday night**: Run `python -m skills.inventory_check` to see what's low.
2. **Monday morning**: Review low stock list. Cross-reference with what's moving and what's sitting.
3. **Monday by noon**: Place distributor orders (Southern Glazer's, Young's Market).
4. **Tuesday**: Place Anchor Distributing order. Walk Cellarmaker/Barebottle if needed.
5. **Wednesday**: Place City Beer order if needed.
6. **Wednesday-Friday**: Receive deliveries. Count against order. Flag shorts immediately.

## Payment Terms

| Vendor | Terms | Notes |
|--------|-------|-------|
| Southern Glazer's | Net 30 | |
| Young's Market | Net 30 | |
| Anchor Distributing | COD | Pay on delivery. |
| City Beer | COD | |
| Walk-in breweries | COD | Cash or card at taproom. |

## Notes

- Rep relationships matter. If something's allocated (Pliny, etc.), the rep decides who gets it.
- When a rep changes, update this file same day. Losing the contact costs weeks.
- Keep order confirmations (email/text) until delivery is verified.
- Dispute shorts within 24 hours or lose the claim.
