# Source register & confidentiality

**Confidentiality — read before sharing the repository.** This repo contains third-party
data that is likely **not redistributable**. Verify rights before making it public or sending
the GitHub link outside the authorised academic context.

| Path | Origin | Sensitivity | Notes |
|---|---|---|---|
| `data/bloomberg/Memoire_de_master.xlsx` | **Bloomberg** (via analyst) | High | Bloomberg index levels — redistribution restricted by Bloomberg licence |
| `data/bloomberg/CHF hedged data.xlsx` | Bloomberg | High | CHF-hedged Global Aggregate |
| `data/bloomberg/Consolidation_allocations.xlsx` | **VZ** | High | VZ AP5 allocation history |
| `docs/source_materials/**` | **VZ** (Kundendoku slide, **PM email**) | High | Internal VZ material; the PM email should not be publicly accessible |
| `data/processed/*.csv` | Derived | Medium | Transformed series; still Bloomberg-derived |
| `src/`, `docs/*.md`, `reports/*.md`, `analysis/*.csv` | This project | Low | Code, methodology, derived results |

**Recommendation.** Keep the repository **private**. If a public/shareable version is needed,
gitignore `data/bloomberg/`, `data/raw/` and `docs/source_materials/`, and publish only the
code, the methodology, the data dictionary, and derived results whose redistribution is
permitted. A `.gitignore` with those paths is provided but **commented** — enabling it removes
the files needed to reproduce from raw, so decide deliberately.
