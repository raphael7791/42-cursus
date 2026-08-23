from __future__ import annotations

import sys
import os
import site

def main() -> None:
    venv_path: str | None = os.environ.get("VIRTUAL_ENV")

if venv_path is None:                                                                                                                                                                               
    print("MATRIX STATUS: You're still plugged in")                                                                                                                                                 
    print(f"Current Python: {sys.executable}")                                                                                                                                                    
    print("Virtual Environment: None detected")
    print()                                                                                                                                                                                         
    print("WARNING: You're in the global environment!")                                                                                                                                             
    print("The machines can see everything you install.")                                                                                                                                           
    global_packages: list[str] = site.getsitepackages()                                                                                                                                             

if global_packages:                                                                                                                                                                             
    print("\nGlobal package location:")                                                                                                                                                         
    print(f"  {global_packages[0]}")                                                                                                                                                          
    print()
    print("To enter the construct, run:")
    print("  python -m venv matrix_env")
    print("  source matrix_env/bin/activate  # On Unix")
    print("  matrix_env\\Scripts\\activate      # On Windows")
    print()
    print("Then run this program again.")