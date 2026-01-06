import os
import sys
from pathlib import Path

# --- Configuration ---
PROJECT_NAME = "New_Petro_Project"  # Change this or input via prompt
PYTHON_VERSION = "3.12"  # 3.12 is currently the stable choice for O&G stacks

def create_structure():
    """Creates the standard directory tree."""
    base_dir = Path.cwd() / PROJECT_NAME
    
    # Define folder structure
    folders = [
        base_dir / "data" / "raw",       # Immutable inputs (LAS, SEGY)
        base_dir / "data" / "processed", # Cleaned parquets/CSVs
        base_dir / "src",                # .py modules
        base_dir / "notebooks",          # Jupyter sandboxes
        base_dir / "tests",              # pytest folder
        base_dir / "reports" / "figures" # Exported plots
    ]

    for folder in folders:
        folder.mkdir(parents=True, exist_ok=True)
        # Add a .gitkeep file so git tracks empty folders
        (folder / ".gitkeep").touch()

    return base_dir

def create_environment_file(base_dir):
    """Creates the Conda environment.yml with O&G + ML stack."""
    
    # We prioritize conda-forge for geospatial/science binaries.
    # We include a pip section for flexibility, though most valid libs are on conda-forge.
    env_content = f"""name: {PROJECT_NAME}
channels:
  - conda-forge
  - defaults
dependencies:
  # --- Core Python ---
  - python={PYTHON_VERSION}
  - pip

  # --- Data Manipulation (The Two Engines) ---
  - pandas
  - polars
  - numpy
  - pyarrow  # Critical for Parquet support

  # --- Geospatial & CRS ---
  - geopandas
  - shapely
  - fiona
  - pyproj
  - rasterio

  # --- O&G Domain Specific ---
  - lasio      # Well logs
  - segyio     # Seismic
  - welly      # Well log quality/handling
  - striplog   # Stratigraphic columns
  # dlisio is sometimes better installed via pip if conda fetch fails, 
  # but we try conda first for cleanliness.
  - dlisio     

  # --- Machine Learning & Math ---
  - scikit-learn
  - scipy
  - statsmodels

  # --- Database ---
  - sqlalchemy
  - psycopg2   # Postgres driver
  - geoalchemy2 # PostGIS support

  # --- Visualization ---
  - matplotlib
  - seaborn
  
  # --- Dev Tools & Quality ---
  - pytest
  - ruff       # The modern linter/formatter
  - jupyterlab
  - ipykernel

  # --- Pip Fallback ---
  - pip:
    # Add any libraries here that are NOT on conda-forge
    # - some-niche-library
"""
    with open(base_dir / "environment.yml", "w") as f:
        f.write(env_content)

def create_readme(base_dir):
    """Generates the README.md with the Style Guide summary."""
    readme_content = f"""# {PROJECT_NAME}

## PetroLuminary Geo Code Style Guide (Quick Reference)

### 1. Environment
* **Update:** `conda env update --file environment.yml --prune`
* **Activate:** `conda activate {PROJECT_NAME}`

### 2. File Paths
* **Never** use string concatenation for paths.
* **Always** use `pathlib`:
    ```python
    from pathlib import Path
    las_path = Path("data/raw") / "well_A.las"
    ```

### 3. Data Strategy
* **Small Data:** Pandas.
* **Big Data (>1GB):** Polars (Lazy execution).
* **Format:** Prefer `.parquet` over `.csv` for internal storage.

### 4. Code Standards
* **Naming:** Semantic variables (e.g., `porosity_fraction` not `phi`).
* **Notebooks:** Logic used >1 times goes into `src/`.
* **Testing:** Run `pytest` before pushing critical calculation code.
* **Linting:** Use `ruff` to format code.

### 5. CRS (Coordinate Reference Systems)
* Always be explicit when loading geospatial data:
    ```python
    gdf = gpd.read_postgis(sql, engine, crs="EPSG:4326")
    ```
"""
    with open(base_dir / "README.md", "w") as f:
        f.write(readme_content)

def create_gitignore(base_dir):
    """Creates a standard Python/Data .gitignore."""
    gitignore_content = """
# Python
__pycache__/
*.py[cod]
.ipynb_checkpoints/
.env

# Environments
.venv/
env/

# Data (NEVER COMMIT RAW DATA)
data/raw/*
data/processed/*
!data/raw/.gitkeep
!data/processed/.gitkeep

# IDEs
.vscode/
.idea/
"""
    with open(base_dir / ".gitignore", "w") as f:
        f.write(gitignore_content)

def create_test_scaffold(base_dir):
    """Creates a dummy test to encourage usage."""
    test_content = """import pytest
import numpy as np

def test_environment_sanity():
    \"\"\"Quick check to ensure libraries load.\"\"\"
    import pandas as pd
    import polars as pl
    import lasio
    assert True

def test_example_calculation():
    \"\"\"Example: Calculate Water Saturation (Archie).\"\"\"
    # This is a placeholder to show how to write a test
    a, m, n = 1, 2, 2
    phi = 0.2
    rw = 0.1
    rt = 10.0
    sw = ((a / (phi ** m)) * (rw / rt)) ** (1 / n)
    assert sw == pytest.approx(0.5, abs=0.01)
"""
    with open(base_dir / "tests" / "test_initial.py", "w") as f:
        f.write(test_content)

def main():
    print(f"🛢️  Initializing PetroLuminary Project: {PROJECT_NAME}...")
    
    base_dir = create_structure()
    print(f"✅ Created directory structure in {base_dir}")
    
    create_environment_file(base_dir)
    print("✅ Created environment.yml (Python 3.12 + O&G Stack)")
    
    create_readme(base_dir)
    print("✅ Created README.md with Style Guide")
    
    create_gitignore(base_dir)
    print("✅ Created .gitignore (Data excluded)")
    
    create_test_scaffold(base_dir)
    print("✅ Created initial pytest scaffold")

    print("\n" + "="*50)
    print("🚀 SETUP COMPLETE!")
    print("="*50)
    print("Next Steps:")
    print(f"1. cd {PROJECT_NAME}")
    print("2. conda env create -f environment.yml")
    print(f"3. conda activate {PROJECT_NAME}")
    print("4. git init")
    print("="*50)

if __name__ == "__main__":
    # Optional: Allow command line argument for project name
    if len(sys.argv) > 1:
        PROJECT_NAME = sys.argv[1]
    main()