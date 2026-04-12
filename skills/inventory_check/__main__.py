"""Entrypoint for python -m skills.inventory_check."""

from skills._lib.runner import run_skill
from skills.inventory_check import main as skill_module

run_skill(skill_module)
