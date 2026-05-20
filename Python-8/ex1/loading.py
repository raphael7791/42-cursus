"""loading.py — Data analysis with dependency management."""
import sys
import importlib


def check_dependency(name: str, description: str) -> bool:
    """Check if a package is installed and print its status."""
    try:
        mod = importlib.import_module(name)
        version: str = getattr(mod, "__version__", "unknown")
        print(f"  [OK] {name} ({version}) - {description}")
        return True
    except ImportError:
        print(f"  [MISSING] {name} - {description}")
        return False


def show_install_instructions() -> None:
    """Show installation instructions for pip and Poetry."""
    print("\nTo install missing dependencies:")
    print("\n  With pip:")
    print("    pip install -r requirements.txt")
    print("\n  With Poetry:")
    print("    poetry install")
    print("    poetry run python loading.py")


def compare_pip_poetry() -> None:
    """Show differences between pip and Poetry dependency management."""
    print("\n--- pip vs Poetry comparison ---")
    print("pip (requirements.txt):")
    print("  - Simple flat text file listing packages")
    print("  - No lock file by default (non-deterministic)")
    print("  - Install: pip install -r requirements.txt")
    print("  - Global or manual venv management")
    print()
    print("Poetry (pyproject.toml):")
    print("  - Structured TOML file with metadata")
    print("  - Automatic lock file (poetry.lock) for reproducibility")
    print("  - Install: poetry install")
    print("  - Built-in virtual environment management")


def run_analysis() -> None:
    """Run the Matrix data analysis using numpy, pandas, matplotlib."""
    import numpy as np
    import pandas as pd
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt  # noqa: E402

    print("\nAnalyzing Matrix data...")

    data = np.random.default_rng(42).integers(0, 100, size=1000)
    print("Processing 1000 data points...")

    df: pd.DataFrame = pd.DataFrame({"value": data})

    mean_val: float = float(df["value"].mean())
    std_val: float = float(df["value"].std())
    min_val: int = int(df["value"].min())
    max_val: int = int(df["value"].max())

    print("\nMatrix Data Summary:")
    print(f"  Total data points: {len(df)}")
    print(f"  Mean: {mean_val:.2f}")
    print(f"  Std deviation: {std_val:.2f}")
    print(f"  Min: {min_val}, Max: {max_val}")

    print("\nGenerating visualization...")
    plt.figure()
    df["value"].plot(kind="hist", bins=20, title="Matrix Data Distribution")
    plt.xlabel("Value")
    plt.ylabel("Frequency")
    output_file: str = "matrix_analysis.png"
    plt.savefig(output_file)
    plt.close()

    print("\nAnalysis complete!")
    print(f"Results saved to: {output_file}")


def main() -> None:
    """Entry point: check deps and run analysis."""
    print("LOADING STATUS: Loading programs...")
    print("\nChecking dependencies:")

    has_pandas: bool = check_dependency(
        "pandas", "Data manipulation ready")
    has_numpy: bool = check_dependency(
        "numpy", "Numerical computation ready")
    has_matplotlib: bool = check_dependency(
        "matplotlib", "Visualization ready")

    if not (has_pandas and has_numpy and has_matplotlib):
        print("\nERROR: Missing required dependencies!")
        show_install_instructions()
        compare_pip_poetry()
        sys.exit(1)

    run_analysis()
    compare_pip_poetry()


if __name__ == "__main__":
    main()
