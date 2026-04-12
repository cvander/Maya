#!/bin/bash
# skill: close-out
# description: End-of-night cash count and reconciliation
# usage: maya close-out [--date YYYY-MM-DD]

set -euo pipefail

MAYA_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
MEMORY_DIR="$MAYA_ROOT/memory"
DATE="${1:-}"

# Parse --date flag
if [ "$DATE" = "--date" ] && [ -n "${2:-}" ]; then
  DATE="$2"
elif [ -z "$DATE" ] || [[ "$DATE" == --* ]]; then
  DATE="$(date +%Y-%m-%d)"
fi

CLOSE_OUT_FILE="$MEMORY_DIR/${DATE}-close-out.md"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  CLOSE-OUT — $DATE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Check if already closed out today
if [ -f "$CLOSE_OUT_FILE" ]; then
  echo "A close-out already exists for $DATE."
  read -rp "Overwrite? (y/N): " overwrite
  if [[ ! "$overwrite" =~ ^[Yy]$ ]]; then
    echo "Keeping existing close-out."
    exit 0
  fi
fi

# Register starting cash
read -rp "Starting cash in register: \$" starting_cash

# Register ending cash
read -rp "Ending cash in register:   \$" ending_cash

# Expected sales (from POS or manual count)
read -rp "Total sales today:         \$" total_sales

# Tips
read -rp "Total tips:                \$" total_tips

# Payouts (vendor cash, petty cash, etc.)
read -rp "Cash payouts (if any):     \$" payouts
payouts="${payouts:-0}"

# Calculate expected ending cash (bc preferred, awk fallback)
calc() { echo "$1" | bc 2>/dev/null || awk "BEGIN {printf \"%.2f\", $1}"; }
expected=$(calc "$starting_cash + $total_sales - $payouts")
variance=$(calc "$ending_cash - $expected")

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  RECONCILIATION"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
printf "  Starting cash:       \$%s\n" "$starting_cash"
printf "  Sales:              +\$%s\n" "$total_sales"
printf "  Payouts:            -\$%s\n" "$payouts"
printf "  ─────────────────────────\n"
printf "  Expected in register: \$%s\n" "$expected"
printf "  Actual in register:   \$%s\n" "$ending_cash"
printf "  ─────────────────────────\n"

if [ "$variance" = "0" ] || [ "$variance" = "0.00" ]; then
  printf "  Variance:             \$0.00 ✓\n"
elif [[ "$variance" == -* ]]; then
  printf "  Variance:             \$%s (short)\n" "$variance"
else
  printf "  Variance:            +\$%s (over)\n" "$variance"
fi

echo ""

# Notes
read -rp "Notes (optional): " notes

# Write to memory
mkdir -p "$MEMORY_DIR"
cat > "$CLOSE_OUT_FILE" <<EOF
# Close-Out — $DATE

## Cash Reconciliation

| Item | Amount |
|------|--------|
| Starting cash | \$$starting_cash |
| Total sales | \$$total_sales |
| Tips | \$$total_tips |
| Payouts | \$$payouts |
| Expected register | \$$expected |
| Actual register | \$$ending_cash |
| **Variance** | **\$$variance** |

## Notes

${notes:-No notes.}

---

*Recorded $(date '+%Y-%m-%d %H:%M:%S')*
EOF

echo "Close-out saved to: $CLOSE_OUT_FILE"
echo ""
echo "Done. Lock up."
