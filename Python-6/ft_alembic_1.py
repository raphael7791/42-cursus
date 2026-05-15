"""Alembic 1: from ... import ... to access elements.py directly."""
from elements import create_water

print("=== Alembic 1 ===")
print("Using: 'from ... import ...' structure to access elements.py")
print(f"Testing create_water: {create_water()}")
