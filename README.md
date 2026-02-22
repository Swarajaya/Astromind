# ☄ AstroMind — AI-Driven Near-Earth Object Risk Simulator

> **Planetary defense modeling powered by Quantum ML + Classical AI + Real NASA data.**

---

## What It Does

AstroMind predicts asteroid trajectory deviations and impact probabilities using a **hybrid Quantum-Classical ML pipeline**:

| Module | Technology | Role |
|--------|-----------|------|
| Quantum VQC | Qiskit + PennyLane | Orbital state encoding & anomaly scoring |
| GBM Ensemble | XGBoost + LightGBM | Classical impact probability estimation |
| Kepler Propagator | SciPy + Astropy | Physics-based orbit integration |
| Monte Carlo | NumPy | Uncertainty quantification over 1000 runs |
| 3D Visualization | Plotly + React/Three.js | Interactive heliocentric orbit renderer |

---

## Language & Stack

| Layer | Language / Framework |
|-------|---------------------|
| Core engine | **Python 3.10+** |
| Quantum circuits | **Qiskit 1.1** + **PennyLane 0.36** |
| ML models | **XGBoost**, **LightGBM**, **PyTorch** |
| Orbital mechanics | **Poliastro**, **Astropy**, **SciPy** |
| Data API | **NASA NeoWs**, **JPL SBDB**, **JPL Horizons** |
| Frontend UI | **React 18** + **Three.js** (JSX artifact) |
| Visualization | **Plotly**, **Matplotlib** |
| Dev server | **Flask 3** |

---

## Project Structure

```
astromind/
├── README.md
├── requirements.txt          # All Python dependencies
├── setup.py                  # Package install config
├── .env.example              # Environment variable template
├── main.py                   # CLI entry point
│
├── src/
│   ├── quantum/
│   │   ├── __init__.py
│   │   └── vqc.py            # Variational Quantum Circuit (8-qubit, 2-layer)
│   │                         #  - ZZFeatureMap orbital encoding
│   │                         #  - RealAmplitudes ansatz
│   │                         #  - Z-basis measurement → impact score
│   │
│   ├── ml/
│   │   ├── __init__.py
│   │   └── ensemble.py       # Hybrid Q-ML ensemble
│   │                         #  - Feature extraction from orbital elements
│   │                         #  - GBM (XGBoost + LightGBM) stacking
│   │                         #  - Hybrid weighting: 35% VQC + 35% GBM + 30% MC
│   │
│   ├── physics/
│   │   ├── __init__.py
│   │   └── kepler.py         # Keplerian orbital propagator
│   │                         #  - Newton-Raphson Kepler equation solver
│   │                         #  - 6-element → Cartesian ECI conversion
│   │                         #  - Monte Carlo uncertainty propagation
│   │
│   ├── visualization/
│   │   ├── __init__.py
│   │   └── orbit_plot.py     # 3D interactive Plotly orbit visualization
│   │                         #  - Heliocentric coordinate frame
│   │                         #  - MC scatter + risk-colored orbits
│   │
│   └── data/
│       ├── __init__.py
│       └── neo_loader.py     # NASA data fetching & caching
│                             #  - NASA NeoWs REST API
│                             #  - JPL Small-Body Database (SBDB)
│                             #  - JPL Horizons ephemeris system
│
├── tests/
│   ├── __init__.py
│   ├── test_kepler.py        # Kepler propagator unit tests
│   ├── test_vqc.py           # Quantum VQC unit tests
│   └── test_ensemble.py      # ML ensemble unit tests
│
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_quantum_circuit_demo.ipynb
│   └── 03_monte_carlo_analysis.ipynb
│
├── scripts/
│   └── fetch_neo_batch.py    # Batch-fetch NEO data from NASA
│
└── docs/
    ├── architecture.md       # System design & data flow
    └── quantum_model.md      # VQC math & circuit diagrams
```

---

## Setup & Installation

### 1. Clone

```bash
git clone https://github.com/your-org/astromind.git
cd astromind
```

### 2. Python Environment

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
cp .env.example .env
# Edit .env — add your NASA API key (free at https://api.nasa.gov)
```

### 4. Run CLI

```bash
# Analyze a specific NEO
python main.py --neo "Apophis"

# With 3D interactive plot
python main.py --neo "Apophis" --plot

# Increase Monte Carlo precision
python main.py --neo "Bennu" --runs 5000 --plot

# List all NEOs in database
python main.py --list
```

### 5. Run Tests

```bash
pytest tests/ -v --cov=src
```

---

## NASA APIs Used

| API | URL | Auth |
|-----|-----|------|
| NeoWs (Near Earth Object Web Service) | `api.nasa.gov/neo/rest/v1/feed` | Free API key |
| JPL Small-Body Database | `ssd-api.jpl.nasa.gov/sbdb.api` | None (public) |
| JPL Horizons System | `ssd.jpl.nasa.gov/api/horizons.api` | None (public) |

Get your free NASA API key at: https://api.nasa.gov

---

## Quantum ML Architecture

```
Orbital Elements (6D)
        │
        ▼
ZZFeatureMap          ← amplitude encodes into 8-qubit Hilbert space
        │
        ▼
VQC Layer 1           ← parameterized Rz / Rx rotations + CNOT entanglement
        │
        ▼
VQC Layer 2           ← second variational layer
        │
        ▼
Z-basis Measurement   → quantum impact score ∈ [0, 1]
        │
        ├──── 35% weight ────────────────────────┐
        │                                        │
GBM Ensemble (XGBoost + LightGBM)               │
  12 orbital features → sigmoid → prob           │
        │                                        │
        ├──── 35% weight ──────────────────────► Hybrid
        │                                        │
Monte Carlo (1000 runs, Kepler propagation)     │
  Gaussian noise → impact count / runs           │
        │                                        │
        └──── 30% weight ────────────────────────┘
                                                 │
                                                 ▼
                                    Final Impact Probability
```

---

## NEO Database (Built-in)

| Name | Diameter | SMA (AU) | ECC | PHA |
|------|----------|----------|-----|-----|
| 2023 DW | 49 m | 1.014 | 0.198 | ✓ |
| Apophis | 370 m | 0.922 | 0.191 | ✓ |
| Bennu | 490 m | 1.126 | 0.204 | ✓ |
| 1950 DA | 1300 m | 1.699 | 0.508 | ✓ |
| 2020 NK1 | 160 m | 1.45 | 0.39 | — |
| 2007 FT3 | 340 m | 1.021 | 0.247 | ✓ |

PHA = Potentially Hazardous Asteroid (MOID < 0.05 AU & H < 22)

---

## Risk Levels (Torino Scale Mapping)

| Probability | Level | Color |
|-------------|-------|-------|
| < 0.1% | MINIMAL | 🟢 |
| 0.1% – 1% | LOW | 🟡 |
| 1% – 5% | ELEVATED | 🟠 |
| > 5% | CRITICAL | 🔴 |

---

## License

MIT — See LICENSE for details.

---

> *"The dinosaurs didn't have a space program. We do."* — Carl Sagan
