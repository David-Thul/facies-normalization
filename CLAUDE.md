# facies-normalization — Claude Context
**Company:** PetroLuminary
**Repo:** `/Users/davidthul/Documents/github/facies-normalization`
**Last updated:** 2026-04-07

---

## What This Is

**Facies Normalization** provides Python utilities for standardizing geological sample descriptions — normalizing facies names, geologic environments, systems tracts, and lithological descriptions across inconsistent datasets. This is a data quality/standardization tool for subsurface interpretation workflows.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python |
| Environment | Conda (required per PetroLuminary standards) |
| Domain | Carbonate facies definitions/mappings |

---

## Key Content

```
carbonate facies/   # Carbonate facies definitions and name mappings
```

---

## Current Status

Early Stage. Core utilities being developed.

---

## PetroLuminary Style Guide

Follow PetroLuminary Style Guide:
- pathlib, Parquet, type hints
- Ruff, Pytest
- Conda environments

---

## Related Projects

- `regional-petrophysics` — Facies normalization outputs can enrich petrophysical interpretations
- `loop-forward` — Normalized facies vocabulary may feed the collaborative interpretation system
- `well-analysis` — Facies data is part of well log interpretation
- `petro-explo-flow` — Reference for code standards

---

## Conventions

- snake_case, rev# versioning
- Conda environment required — confirm naming with Dave
