"""Alembic 2: import ... to access alchemy/elements.py directly."""
import alchemy.elements

print("=== Alembic 2 ===")
print("Accessing alchemy/elements.py using 'import ...' structure")
print(f"Testing create_earth: {alchemy.elements.create_earth()}")
