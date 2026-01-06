# PetroLuminary Geo Code Style Guide

**Version:** 1.1
**Effective Date:** 2026
**Target Python Version:** 3.12+

This guide unifies our approach to subsurface data science. It bridges the gap between geological intuition and software engineering rigor. Our code must be as reproducible as a well-log run and as reliable as a casing design.

---

## 1. The Golden Rules (Non-Negotiables)

-   **Reproducibility:** If it doesn't run on a fresh clone with `conda env create`, it is broken.
-   **Readability:** We write code for humans first, computers second. Implicit variable names (e.g., `df`, `temp`, `x`) are forbidden.
-   **Path Safety:** String manipulation for file paths is forbidden. Always use `pathlib`.
-   **Notebook Hygiene:** Notebooks are for exploration, not production. Any logic used more than once must be refactored into `src/` modules.

---

## 2. Environment & Project Structure

All projects must strictly adhere to the standard directory layout and dependency management.

### 2.1 Standard Directory Tree

```
project_name/
├── data/
│   ├── raw/             # IMMUTABLE. Never edit these files manually. (LAS, SEGY, CSV)
│   └── processed/       # Cleaned Parquet files, ready for analysis.
├── notebooks/           # Jupyter Labs for experimentation. Prefix with numbers (01_explore.ipynb).
├── src/                 # Reusable Python modules (.py).
├── tests/               # Pytest scripts.
├── environment.yml      # The source of truth for dependencies.
└── .gitignore           # Must exclude data/ folders.
```

### 2.2 Dependency Management (Conda/Mamba)

-   **Source of Truth:** The `environment.yml` file.
-   **Installation:** Never use `pip install` in the terminal without immediately adding the package to `environment.yml`.
-   **Channels:** We prioritize `conda-forge` th ensure geospatial binaries (GDAL, PROJ) play nicely with Python.
-   **Pip Rule: The pip section is used for geology specific libraries with no conda-forge support.**

**Example `environment.yml` snippet:**

```yaml
name: reservoir_viz
channels:
  - conda-forge
dependencies:
  - python=3.12
  - pandas
  - polars
  - geopandas
  - lasio
  - welly
  - scikit-learn
  - pytest
  - ruff
  #...etc
# --- Pip Fallback ---
# Only for libs not stable/available on conda-forge
  - pip:
    - lasio
    - welly
    - dlisio
    - striplog
    - segyio
    - pyproj

```

---

## 3. Data Strategy: The "Two-Engine" Rule

We choose our tools based on data volume to balance ease-of-use with performance.

### 3.1 Engine Selection

| Scenario    | Engine | Condition                                                              |
| :---------- | :----- | :--------------------------------------------------------------------- |
| Small Data  | Pandas | < 1M rows or < 500MB csv. Good for quick ad-hoc analysis.              |
| Large Data  | Polars | > 1M rows or > 500MB. Mandatory for full-field seismic attributes or multi-well production history. |

### 3.2 Polars Best Practices

Leverage "Lazy Execution" to optimize query plans before running them.

```python
import polars as pl

# GOOD: Lazy evaluation chain
q = (
    pl.scan_parquet("data/processed/production_history.parquet")
    .filter(pl.col("water_cut") < 0.8)
    .group_by("formation")
    .agg(pl.col("oil_production").sum())
)
df = q.collect() # Execution happens here
```

### 3.3 Storage Formats

-   **Input:** LAS, SEGY, DLIS (Keep raw).
-   **Intermediate/Output:** Parquet.
-   **Why?** It preserves data types (unlike CSV), compresses better, and is optimized for Polars/Arrow.

---

## 4. Coding Standards

### 4.1 Naming Conventions

Variable names must be semantic. In our domain, units matter.

-   **General Variables:** `lower_snake_case`
-   **Constants:** `UPPER_SNAKE_CASE`
-   **Classes:** `PascalCase`

**Geology Specific Suffixes:**

When a variable implies a physical quantity, suffix it with the unit if ambiguous.

| Bad               | Good                  | Why                                                      |
| :---------------- | :-------------------- | :------------------------------------------------------- |
| `depth`           | `depth_md` or `depth_tvd_ss` | Avoids confusion between Measured Depth vs TVD Subsea.   |
| `phi`             | `porosity_frac`       | Is it percentage (15.0) or fraction (0.15)?              |
| `gr`              | `gamma_ray_api`       | Be explicit about API units.                             |
| `data`            | `well_logs_df`        | `data` describes nothing.                                |

### 4.2 Path Handling (Pathlib)

**Rule:** Use `pathlib.Path` for all file interactions.

```python
from pathlib import Path

# BAD
path = "data/raw/" + well_name + ".las"

# GOOD
RAW_DIR = Path("../data/raw")
FILE_PATH = raw_dir / f"{well_name}.las"

if not file_path.exists():
    raise FileNotFoundError(f"Well file not found: {file_path}")
```

### 4.3 Type Hinting

All shared functions in `src/` must be type-hinted. This serves as documentation and error checking.

```python
def calculate_vshale(gamma: float, gr_min: float, gr_max: float) -> float:
    return (gamma - gr_min) / (gr_max - gr_min)
```

---

## 5. Database & Spatial (PostgreSQL / PostGIS)

### 5.1 Credential Safety

Never hardcode passwords or connection strings in scripts. Use environment variables.

```python
import os
from sqlalchemy import create_engine

# GOOD
db_pass = os.getenv("DB_PASSWORD")
engine = create_engine(f"postgresql://user:{db_pass}@localhost:5432/petrodb")
```

### 5.2 CRS (Coordinate Reference Systems) Hygiene

When loading spatial data, you must be explicit about the CRS. Implicit assumptions cause drilling targets to move 50 meters.

```python
import geopandas as gpd

# GOOD: Explicitly defining the Source CRS (EPSG:4326) and converting to Project CRS
gdf = gpd.read_postgis(sql, engine, geom_col="geom", crs="EPSG:4326")
gdf_projected = gdf.to_crs("EPSG:32040") # NAD27 Texas South Central
```

---

## 6. Documentation & Testing

### 6.1 Docstrings

Use NumPy Style docstrings for all complex functions.

```python
def calculate_archie_sw(phi: float, rt: float, rw: float, m: float = 2.0) -> float:
    """
    Calculates water saturation using Archie's equation.

    Parameters
    ----------
    phi : float
        Porosity (fraction).
    rt : float
        True formation resistivity (ohm-m).
    ...
    """
```

### 6.2 Testing (Pytest)

We adopt a "Babysteps" approach to testing.

-   **Requirement:** Any function performing a critical calculation (Reserves, Saturation, Net Pay) must have a corresponding unit test in `tests/`.
-   **Run:** Execute `pytest` in the root directory.

---

## 7. Tooling & Linting

We use **Ruff** for linting and formatting. It replaces Flake8, Black, and Isort.

-   **Setup:** Ensure your IDE (VS Code / PyCharm) is set to "Format on Save" using Ruff.
-   **Command Line:**
    -   Check: `ruff check .`
    -   Format: `ruff format .`
