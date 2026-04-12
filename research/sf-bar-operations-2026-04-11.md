# Research: SF Bar Operations vs Maya's Inventory Template

**Date**: 2026-04-11
**Sources**: Perplexity Sonar Pro, Grok X Search, Grok YouTube
**Question**: Is Maya's markdown-based inventory system a good template for San Francisco bars?

## Executive Summary

San Francisco neighborhood bars face a unique combination of expensive/scarce ABC licenses, strict health department oversight, and high labor costs ($18.67/hr minimum wage, 2026). The industry standard for inventory is dedicated mobile apps (Bar Patrol, BevSpot, Wisk, Backbar) at $49-69/month. Maya's markdown-based approach is unconventional but has real strengths for a specific niche: a single-location bar run by a tech-comfortable owner who values simplicity, zero vendor lock-in, and full data ownership.

## SF Bar Operations Landscape

### ABC Licensing (California)
- **License types**: Type 42 (beer/wine on-premise), Type 47 (full liquor on-premise), Type 48 (bar, no food requirement)
- **Cost**: Market price ~$110K for transferable licenses in SF; limited supply creates bidding wars
- **Timeline**: 150-180 days for new applications (ABC + MVIP/CCU inspections)
- **Renewal**: Annual, strict compliance required
- **Enforcement**: Unannounced ABC audits; mandatory physical ID checks; license revocation for violations
- **SF-specific**: Limited license count makes them scarce assets; transfers are slow even for previously-licensed locations

### Inventory Management (Industry Standard)
| Tool | Price | Key Features | Best For |
|------|-------|-------------|----------|
| Bar Patrol | $49-69/mo | Bluetooth scales, auto-reorders, POS export, recipe costing | Small independents |
| BevSpot | Varies | Multi-location, demand forecasting | Growing bars |
| Wisk | Varies | POS integration, scanning, alerts | Tech-forward bars |
| Backbar | Varies | Invoice import, real-time counts | Easy setup |
| Partender | Varies | Fast mobile counts, basic reports | Speed-focused |
| Square for Retail | POS-bundled | Barcode scanning, low-stock alerts, local tax | Already on Square |

### Reorder Workflows
- Par levels set per item (min stock before reorder)
- Apps calculate variance (expected vs actual usage)
- Automated vendor order drafts from low-stock triggers
- Demand forecasting tied to local events, tourist seasons, day-of-week patterns

### Compliance Deadlines (SF-Specific)
- **SFDPH (Health Dept)**: Weekly pest logs, monthly cooler temperature records, FIFO rotation, sanitation logs
- **ABC**: Annual renewal, unannounced compliance audits, hours enforcement (no sales after 2 AM)
- **Labor**: SF minimum wage $18.67/hr (2026), 21+ requirement for liquor service

### Staffing
- Minimum age 21 for serving liquor
- SF's high cost of living makes retention difficult
- Most small bars run lean (2-3 bartenders, owner-operator model)

## Maya Template Assessment

### What Maya Gets Right

1. **File-per-category structure** (beer.md, spirits.md, wine.md) -- matches how bars actually think about inventory (separate orders, separate vendors, separate count sheets)
2. **Reorder threshold as first-class field** -- this is THE critical number for bar inventory; every pro tool centers on it
3. **Notes column** -- bars rely heavily on institutional knowledge ("Don't waste it", "Sipping rum, not a mixer"); capturing this in-line is valuable
4. **Read-only skill model** -- correct for inventory checking; mutations (orders, counts) are separate workflows
5. **Advisory failure mode** -- the bar runs without the software; this matches small-bar reality where the bartender knows what's low
6. **Zero dependencies** -- runs on a Mac Mini with no internet, no subscription, no vendor lock-in
7. **Fictional fixture rule** -- privacy-correct for a bar that knows its regulars by name

### What Maya Is Missing (vs Industry Tools)

1. **No mobile counting interface** -- bartenders count from behind the bar, not from a terminal. Industry tools use phone cameras/Bluetooth scales. Maya reads static markdown, which means someone updates the files manually.
2. **No POS integration** -- bars track pour cost (cost vs revenue per drink). Without POS data, you can't calculate variance or shrinkage. Maya has no concept of sales.
3. **No partial bottle tracking** -- spirits inventory is counted in tenths ("tenthing"). beer.md tracks kegs, but spirits.md needs a "level" field (e.g., 0.7 = 70% full), not just integer qty.
4. **No vendor order generation** -- Maya detects low stock but can't draft an order email/fax. Phase 1 explicitly defers this (vendor-order skill is planned).
5. **No cost/price tracking** -- spirits.md has a Price column but it's empty template. Pour cost analysis requires cost-per-unit.
6. **No expiration tracking** -- vermouth, juice, garnishes expire. wine.md's "By the Glass" section needs open-date tracking.
7. **No count workflow** -- no "start count" / "end count" / "submit count" flow. Inventory-count skill is planned but not built.

### Honest Verdict

**Maya is a good template for Phase 1 of a bar management system, not a replacement for dedicated bar inventory apps.**

For a bar owner who is also a developer (or has one as a friend), Maya's approach has genuine advantages:
- **$0/month** vs $49-69/month for Bar Patrol
- **Full data ownership** -- your inventory data is in readable files, not locked in a SaaS
- **Customizable** -- you can add columns, change thresholds, script whatever you want
- **Offline-first** -- works on a Mac Mini behind the bar with no internet dependency
- **Git history** -- every inventory change is tracked, diffable, revertible

But for a typical SF bar owner who just wants inventory done:
- Bar Patrol or Backbar is the pragmatic choice
- Mobile interface matters more than data ownership
- $49/month is trivial vs the cost of one wasted keg

**The sweet spot for Maya**: a bar that starts with Maya's markdown for structure + low-stock alerts, and adds the count workflow (Phase 2) and vendor-order (Phase 3) skills. If the owner finds they need POS integration or mobile counting, they graduate to Bar Patrol. Maya's contract system (manifest.toml, Result schema) is designed to make that graduation possible without losing the structured data.

## Recommendations for Maya's Roadmap

Based on how SF bars actually operate:

1. **Add a "level" field for spirits** -- integer qty works for kegs/bottles, but spirits need fractional tracking (tenthing). Consider `level` as a float column alternative.
2. **Add open-date for perishables** -- vermouth, juice, garnishes need "opened: YYYY-MM-DD" to track freshness.
3. **Vendor-order skill should generate actual orders** -- even a plain-text email draft ("Order 2x Pliny the Elder 1/2 bbl from Russian River") would be high-value.
4. **Consider a simple count mode** -- `python -m skills.inventory_count` that walks through each item and asks for current qty, then updates the markdown. Even a CLI is better than manual file editing.
5. **Track the ABC renewal deadline** -- compliance-check skill should know the bar's license type and renewal date.
6. **SFDPH logs** -- weekly pest log and monthly cooler temps are mandatory. A `compliance-log` skill that appends dated entries would prevent violations.

## Sources

### Web (Perplexity)
- Bar Patrol, BevSpot, Wisk, Backbar, Partender, Square for Retail feature comparisons
- CA ABC licensing requirements and process documentation
- SFDPH health code requirements for food/beverage establishments

### X/Twitter
- @clintolsen on SF liquor license scarcity (Jan 2025, 551 likes)
- @DDaarriius on ABC audit enforcement (Apr 2026)
- General bar inventory management discussions

### YouTube
- [How To Get A California Liquor License](https://www.youtube.com/watch?v=OlHg7BIsSl0) - Permit Place
- [ABC License Types Explained](https://www.youtube.com/watch?v=LzOB71rjbfw) - AAA Liquor License Consulting
- [Top 4 Bar Inventory Apps 2026](https://www.youtube.com/watch?v=z1DeX1wTqy4) - Dave Allred/Bar Patrol
- [Best Bar Inventory App 2025](https://www.youtube.com/watch?v=-t4edaakZIo) - Dave Allred/Bar Patrol
- [Bar Inventory App for Independents](https://www.youtube.com/watch?v=vkoiJKQIZME) - Dave Allred/Bar Patrol
- [WISK Inventory Software](https://www.youtube.com/watch?v=gpZcmeDNqpg) - WISK
- [Bar Inventory Spreadsheet Setup](https://www.youtube.com/watch?v=-pk0KC2WnmI) - Backbar
