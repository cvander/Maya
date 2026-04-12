#!/bin/bash
# setup.sh — Verify Maya is ready to run on this machine
# Usage: ./setup.sh

set -euo pipefail

MAYA_ROOT="$(cd "$(dirname "$0")" && pwd)"
PASS=0
FAIL=0

check() {
  local label="$1"
  local result="$2"
  if [ "$result" -eq 0 ]; then
    printf "  ✓  %s\n" "$label"
    PASS=$((PASS + 1))
  else
    printf "  ✗  %s\n" "$label"
    FAIL=$((FAIL + 1))
  fi
}

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  MAYA SETUP CHECK"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Check OS
echo "System:"
[[ "$(uname)" == "Darwin" ]] && check "macOS detected" 0 || check "macOS detected (not macOS — $(uname))" 1

# Check bash version (need 4+ for associative arrays if ever needed)
check "bash available ($(bash --version | head -1 | grep -oE '[0-9]+\.[0-9]+' | head -1))" 0

# Check bc (used for cash math)
command -v bc &>/dev/null && check "bc available (cash math)" 0 || check "bc available (cash math) — install with: brew install bc" 1

# Check directory structure
echo ""
echo "Directory structure:"
[ -f "$MAYA_ROOT/maya" ] && check "maya CLI found" 0 || check "maya CLI found" 1
[ -d "$MAYA_ROOT/skills" ] && check "skills/ directory" 0 || check "skills/ directory" 1
[ -d "$MAYA_ROOT/docs" ] && check "docs/ directory" 0 || check "docs/ directory" 1
[ -d "$MAYA_ROOT/memory" ] && check "memory/ directory" 0 || check "memory/ directory" 1
[ -f "$MAYA_ROOT/SOUL.md" ] && check "SOUL.md" 0 || check "SOUL.md" 1
[ -f "$MAYA_ROOT/AGENTS.md" ] && check "AGENTS.md" 0 || check "AGENTS.md" 1

# Check maya is executable
echo ""
echo "Permissions:"
[ -x "$MAYA_ROOT/maya" ] && check "maya is executable" 0 || check "maya is executable — run: chmod +x maya" 1

# Check skills are executable
for f in "$MAYA_ROOT/skills"/*.sh; do
  [ -f "$f" ] || continue
  local_name="$(basename "$f")"
  [ -x "$f" ] && check "$local_name is executable" 0 || check "$local_name is executable — run: chmod +x skills/$local_name" 1
done

# Check .env
echo ""
echo "Configuration:"
[ -f "$MAYA_ROOT/.env" ] && check ".env file configured" 0 || check ".env file configured — copy from .env.example" 1

# Check PATH
echo ""
echo "Installation:"
if command -v maya &>/dev/null; then
  check "maya in PATH ($(which maya))" 0
else
  check "maya in PATH — run: ln -sf $MAYA_ROOT/maya /usr/local/bin/maya" 1
fi

# Summary
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
printf "  %d passed, %d failed\n" "$PASS" "$FAIL"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

if [ "$FAIL" -eq 0 ]; then
  echo "Maya is ready. Run: maya --list"
else
  echo "Fix the items above, then run this again."
fi
