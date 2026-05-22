# Conda Environment Registry
*PetroLuminary — facies-normalization*
*Last updated: 2026-04-24*

---

## Active Environments

### `carb_facies_normalization`
| Field | Value |
|---|---|
| **Status** | Active |
| **Python** | 3.12 |
| **Purpose** | Carbonate facies normalization — Jupyter-driven analysis + Excel export |
| **Spec file** | `carbonate facies/environment.yml` |

**Key packages:**
| Package | Role |
|---|---|
| pandas, numpy | Tabular data |
| matplotlib, seaborn, plotly | Visualization |
| jupyter, notebook, ipykernel, ipywidgets | Notebook runtime + interactive widgets |
| openpyxl, xlrd | Excel read/write (.xlsx and .xls) |
| thefuzz, python-levenshtein (pip) | Fuzzy string matching |

**Create / activate:**
```bash
conda env create -f "carbonate facies/environment.yml"
conda activate carb_facies_normalization
```

---

## Notes

- **Never use the base conda environment.** Always create and activate the named env.
- **Name collision warning:** `well-analysis/carbonates/environment.yml` also
  declares an env named `carb_facies_normalization`. Creating both on the same
  machine will overwrite whichever was installed last. Either rename one or
  keep only one installed at a time. See `well-analysis/conda_environments.md`.
