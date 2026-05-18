"""loading.py — Data analysis with dependency management."""
from __future__ import annotations
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
    import matplotlib.pyplot as plt

    print("\nAnalyzing Matrix data...")

    rng: np.random.Generator = np.random.default_rng(42)
    n: int = 1000
    print(f"Processing {n} data points...")

    timestamps: np.ndarray = np.arange(n)  # type: ignore[type-arg]
    signal: np.ndarray = (  # type: ignore[type-arg]
        np.sin(timestamps * 0.05) * 50
        + rng.normal(0, 10, n)
    )
    anomaly_flags: np.ndarray = (  # type: ignore[type-arg]
        rng.choice([0, 1], size=n, p=[0.95, 0.05])
    )

    df: pd.DataFrame = pd.DataFrame({
        "timestamp": timestamps,
        "signal_strength": signal,
        "anomaly": anomaly_flags,
    })

    total: int = len(df)
    anomalies: int = int(df["anomaly"].sum())
    mean_signal: float = float(df["signal_strength"].mean())
    std_signal: float = float(df["signal_strength"].std())

    print("\nMatrix Data Summary:")
    print(f"  Total data points: {total}")
    print(f"  Anomalies detected: {anomalies}")
    print(f"  Mean signal strength: {mean_signal:.2f}")
    print(f"  Signal std deviation: {std_signal:.2f}")

    print("\nGenerating visualization...")

    fig, axes = plt.subplots(2, 1, figsize=(12, 8))

    axes[0].plot(df["timestamp"], df["signal_strength"],
                 color="green", alpha=0.7, linewidth=0.5)
    anomaly_data = df[df["anomaly"] == 1]
    axes[0].scatter(anomaly_data["timestamp"],
                    anomaly_data["signal_strength"],
                    color="red", s=20, label="Anomaly")
    axes[0].set_title("Matrix Signal Monitoring")
    axes[0].set_xlabel("Timestamp")
    axes[0].set_ylabel("Signal Strength")
    axes[0].legend()

    axes[1].hist(df["signal_strength"], bins=40,
                 color="green", alpha=0.7, edgecolor="black")
    axes[1].set_title("Signal Distribution")
    axes[1].set_xlabel("Signal Strength")
    axes[1].set_ylabel("Frequency")

    plt.tight_layout()
    output_file: str = "matrix_analysis.png"
    plt.savefig(output_file, dpi=100)
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
