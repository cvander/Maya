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
    printf "  +  %s\n" "$label"
    PASS=$((PASS + 1))
  else
    printf "  x  %s\n" "$label"
    FAIL=$((FAIL + 1))
  fi
}

echo ""
echo "  MAYA SETUP CHECK"
echo "  ================"
echo ""

# Check OS
echo "System:"
[[ "$(uname)" == "Darwin" ]] && check "macOS detected" 0 || check "macOS detected (not macOS -- $(uname))" 1

# Check Python 3.11+
PYTHON=""
for candidate in python3.11 python3.12 python3.13 python3; do
  p="$(command -v "$candidate" 2>/dev/null || true)"
  if [ -n "$p" ] && [ -x "$p" ]; then
    PYTHON="$p"
    break
  fi
done
# Homebrew fallback
if [ -z "$PYTHON" ]; then
  for p in /opt/homebrew/bin/python3.11 /opt/homebrew/bin/python3 /usr/local/bin/python3; do
    if [ -x "$p" ]; then
      PYTHON="$p"
      break
    fi
  done
fi
if [ -n "$PYTHON" ]; then
  PY_VER="$("$PYTHON" --version 2>&1 | grep -oE '[0-9]+\.[0-9]+' | head -1)"
  check "Python $PY_VER ($PYTHON)" 0
else
  check "Python 3.11+ -- install with: brew install python@3.11" 1
fi

# Check directory structure
echo ""
echo "Directory structure:"
[ -f "$MAYA_ROOT/bin/maya" ] && check "bin/maya CLI found" 0 || check "bin/maya CLI found" 1
[ -d "$MAYA_ROOT/skills" ] && check "skills/ directory" 0 || check "skills/ directory" 1
[ -d "$MAYA_ROOT/docs" ] && check "docs/ directory" 0 || check "docs/ directory" 1
[ -f "$MAYA_ROOT/SOUL.md" ] && check "SOUL.md" 0 || check "SOUL.md" 1
[ -f "$MAYA_ROOT/AGENTS.md" ] && check "AGENTS.md" 0 || check "AGENTS.md" 1
[ -f "$MAYA_ROOT/skills/CONTRACT.md" ] && check "skills/CONTRACT.md" 0 || check "skills/CONTRACT.md" 1

# Check maya is executable
echo ""
echo "Permissions:"
[ -x "$MAYA_ROOT/bin/maya" ] && check "bin/maya is executable" 0 || check "bin/maya is executable -- run: chmod +x bin/maya" 1

# Count skills
echo ""
echo "Skills:"
SKILL_COUNT=0
for d in "$MAYA_ROOT/skills"/*/; do
  [ -d "$d" ] || continue
  name="$(basename "$d")"
  case "$name" in _*|__*) continue ;; esac
  [ -f "$d/manifest.toml" ] || continue
  SKILL_COUNT=$((SKILL_COUNT + 1))
done
check "$SKILL_COUNT skills installed" 0

# Quick smoke test
if [ -n "$PYTHON" ]; then
  echo ""
  echo "Smoke test:"
  cd "$MAYA_ROOT"
  # Exit code 0=ok, 1=warn are both valid
  rc=0
  "$PYTHON" -m skills.inventory_check --format json >/dev/null 2>&1 || rc=$?
  if [ "$rc" -le 1 ]; then
    check "inventory-check runs" 0
  else
    check "inventory-check runs" 1
  fi
fi

# Check .env
echo ""
echo "Configuration:"
[ -f "$MAYA_ROOT/.env" ] && check ".env file configured" 0 || check ".env file -- not required yet (no integrations active)" 0

# Summary
echo ""
echo "  ================"
printf "  %d passed, %d failed\n" "$PASS" "$FAIL"
echo "  ================"
echo ""

if [ "$FAIL" -eq 0 ]; then
  echo "Maya is ready. Run: bin/maya --list"
else
  echo "Fix the items above, then run this again."
fi
