"""
orbit_plot.py — 3D interactive heliocentric orbit visualization with Plotly.

Renders:
  - Heliocentric reference frame (J2000)
  - Sun + Earth orbit ring
  - Asteroid orbit trace (risk-colored)
  - Monte Carlo trajectory scatter
"""

import numpy as np
import plotly.graph_objects as go
from src.physics.kepler import propagate

RISK_COLORS = {
    "MINIMAL":  "#00ff9d",
    "LOW":      "#ffe600",
    "ELEVATED": "#ff8c00",
    "CRITICAL": "#ff2d55",
}


def _earth_orbit() -> tuple:
    """Generate Earth's approximate circular orbit points."""
    theta = np.linspace(0, 2 * np.pi, 360)
    return np.cos(theta), np.sin(theta), np.zeros(360)


def plot_orbit_3d(params: dict, risk_level: str = "MINIMAL",
                  mc_states=None, show_earth: bool = True,
                  n_orbit_steps: int = 360) -> go.Figure:
    """
    Generate 3D interactive heliocentric orbit visualization.

    Args:
        params:          Orbital element dict
        risk_level:      MINIMAL / LOW / ELEVATED / CRITICAL
        mc_states:       Optional list of OrbitalState from monte_carlo()
        show_earth:      Draw Earth orbit ring
        n_orbit_steps:   Orbit curve resolution

    Returns:
        plotly.graph_objects.Figure
    """
    color = RISK_COLORS.get(risk_level, "#00ff9d")
    name  = params.get("name", "Asteroid")

    # ── Orbit trace ──────────────────────────────────────────────────────────
    orbit_x, orbit_y, orbit_z = [], [], []
    for i in range(n_orbit_steps + 1):
        state = propagate(params, i * 365.0 / n_orbit_steps)
        orbit_x.append(state.x)
        orbit_y.append(state.y)
        orbit_z.append(state.z)

    # Current position (epoch)
    pos0 = propagate(params, 0)

    traces = [
        go.Scatter3d(
            x=[0], y=[0], z=[0], mode="markers",
            marker=dict(size=14, color="#FFF176", symbol="circle"),
            name="☀ Sun"
        ),
        go.Scatter3d(
            x=orbit_x, y=orbit_y, z=orbit_z, mode="lines",
            line=dict(color=color, width=2, dash="dash"),
            name=f"{name} orbit"
        ),
        go.Scatter3d(
            x=[pos0.x], y=[pos0.y], z=[pos0.z], mode="markers",
            marker=dict(size=9, color=color, symbol="circle",
                        line=dict(color="white", width=1)),
            name=f"{name} (epoch)"
        ),
    ]

    if show_earth:
        ex, ey, ez = _earth_orbit()
        traces.append(go.Scatter3d(
            x=ex, y=ey, z=ez, mode="lines",
            line=dict(color="#4fc3f7", width=2),
            name="Earth orbit"
        ))
        # Earth position (arbitrary)
        traces.append(go.Scatter3d(
            x=[1.0], y=[0.0], z=[0.0], mode="markers",
            marker=dict(size=7, color="#4fc3f7", symbol="circle"),
            name="Earth"
        ))

    if mc_states:
        step = max(1, len(mc_states) // 100)
        mx = [s.x for s in mc_states[::step]]
        my = [s.y for s in mc_states[::step]]
        mz = [s.z for s in mc_states[::step]]
        traces.append(go.Scatter3d(
            x=mx, y=my, z=mz, mode="markers",
            marker=dict(size=2, color=color, opacity=0.25),
            name="MC trajectories"
        ))

    fig = go.Figure(data=traces)
    fig.update_layout(
        title=dict(
            text=f"AstroMind — {name} | Risk: {risk_level}",
            font=dict(color="#e0e8ff", size=16, family="Space Mono")
        ),
        scene=dict(
            bgcolor="#060a12",
            xaxis=dict(title="X (AU)", color="#4fc3f7", gridcolor="#1a2a4a", zerolinecolor="#1a2a4a"),
            yaxis=dict(title="Y (AU)", color="#4fc3f7", gridcolor="#1a2a4a", zerolinecolor="#1a2a4a"),
            zaxis=dict(title="Z (AU)", color="#4fc3f7", gridcolor="#1a2a4a", zerolinecolor="#1a2a4a"),
            aspectratio=dict(x=1, y=1, z=0.4),
        ),
        paper_bgcolor="#060a12",
        plot_bgcolor="#060a12",
        font=dict(color="#e0e8ff", family="Space Mono"),
        legend=dict(bgcolor="#0a0f1e", bordercolor="#1a2a4a", borderwidth=1,
                    font=dict(color="#e0e8ff", size=11)),
        margin=dict(l=0, r=0, t=50, b=0),
    )
    return fig
