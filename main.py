"""
main.py — AstroMind CLI entry point.

Usage:
    python main.py --neo "Apophis"           # Analyze a specific NEO
    python main.py --neo "Apophis" --plot    # With 3D orbit plot
    python main.py --list                    # List all NEOs in DB
    python main.py --runs 5000 --neo Bennu   # High-precision Monte Carlo
"""

import argparse
import json
import numpy as np
from src.data.neo_loader import load_neo_dataframe
from src.quantum.vqc import vqc_predict
from src.physics.kepler import monte_carlo
from src.ml.ensemble import hybrid_predict


def analyze(name: str, runs: int = 1000, plot: bool = False):
    df = load_neo_dataframe()
    match = df[df["name"].str.lower() == name.lower()]

    if match.empty:
        print(f"\n[ERROR] NEO '{name}' not found. Use --list to see available objects.\n")
        return

    params = match.iloc[0].to_dict()

    print(f"\n{'='*62}")
    print(f"  ☄  AstroMind — Analyzing: {params['name']}")
    print(f"{'='*62}")
    print(f"  SMA={params['sma']} AU  |  ECC={params['ecc']}  |  INC={params['inc']}°")
    print(f"  Diameter: {params['diameter_m']} m  |  PHA: {params['pha']}\n")

    print("[1/3] Quantum VQC encoding orbital state vector...")
    qml_score = vqc_predict(params)
    print(f"      Q-ML Score  : {qml_score:.6f}\n")

    print(f"[2/3] Monte Carlo trajectory simulation ({runs} runs × 365 days)...")
    mc = monte_carlo(params, runs=runs)
    print(f"      MC Impact Prob   : {mc['impact_probability']*100:.4f}%")
    print(f"      Min approach dist: {mc['min_r']:.4f} AU\n")

    print("[3/3] Hybrid ensemble prediction (35% VQC + 35% GBM + 30% MC)...")
    result = hybrid_predict(params, qml_score, mc["impact_probability"])

    print(f"\n{'─'*62}")
    print(f"  ✦  HYBRID IMPACT PROBABILITY : {result['hybrid_probability']*100:.6f}%")
    print(f"  ✦  RISK LEVEL                : {result['risk_level']}")
    print(f"{'─'*62}\n")
    print(json.dumps(result, indent=2))

    if plot:
        print("\n[LAUNCH] Opening full AstroMind dashboard in browser...")
        import subprocess, sys, threading, webbrowser, time
        # Write static dashboard first
        import importlib.util, os
        spec = importlib.util.spec_from_file_location("server", os.path.join(os.path.dirname(__file__), "server.py"))
        srv = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(srv)
        srv.write_dashboard()
        # Start Flask server in background thread
        def run_server():
            srv.app.run(host="127.0.0.1", port=5000, debug=False, use_reloader=False)
        t = threading.Thread(target=run_server, daemon=True)
        t.start()
        time.sleep(1.5)
        webbrowser.open(f"http://127.0.0.1:5000")
        print("  ✓ Dashboard open at http://127.0.0.1:5000")
        print("  Press Ctrl+C to stop.\n")
        try:
            while True: time.sleep(1)
        except KeyboardInterrupt:
            print("\n  Server stopped.")


def main():
    parser = argparse.ArgumentParser(
        description="AstroMind — Quantum-ML NEO Risk Simulator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --list
  python main.py --neo "Apophis"
  python main.py --neo "Bennu" --runs 5000 --plot
        """
    )
    parser.add_argument("--neo",   type=str,            help="NEO name to analyze")
    parser.add_argument("--runs",  type=int, default=1000, help="Monte Carlo runs (default: 1000)")
    parser.add_argument("--plot",  action="store_true", help="Show 3D Plotly orbit visualization")
    parser.add_argument("--list",  action="store_true", help="List all NEOs in built-in database")
    args = parser.parse_args()

    if args.list:
        df = load_neo_dataframe()
        print(f"\n  {'Name':<20} {'SMA':>7} {'ECC':>7} {'INC':>6} {'Diam(m)':>9} {'PHA':>5}")
        print("  " + "─" * 60)
        for _, row in df.iterrows():
            print(f"  {row['name']:<20} {row['sma']:>7.3f} {row['ecc']:>7.3f} "
                  f"{row['inc']:>6.1f} {row['diameter_m']:>9} {'✓' if row['pha'] else '':>5}")
        print()
        return

    if args.neo:
        analyze(args.neo, runs=args.runs, plot=args.plot)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
