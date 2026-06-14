"""
generate_mobile_mist_cooling_graphs.py

Generates illustrative graphs for the Mobile Mist Cooling conceptual model.

These graphs are for conceptual comparison only.
They are not CFD simulation results.
They do not represent certified or measured cooling performance.
All values are assumption-based estimates.
Field testing is required before making any engineering claims.
"""

import os
import sys

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
except ImportError:
    print("matplotlib is not available. Please install it to generate graphs.")
    print("pip install matplotlib")
    sys.exit(1)

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "images")
os.makedirs(OUTPUT_DIR, exist_ok=True)

DISCLAIMER = (
    "Conceptual estimate only - not a CFD result, not certified performance.\n"
    "Field testing required before any engineering claim."
)

SCENARIOS = [
    {
        "label": "Dry Climate\nDirect Tank Refill",
        "short": "Dry/Direct",
        "ambient_temp_c": 42.0,
        "relative_humidity": 15.0,
        "evaporation_efficiency": 0.70,
        "coverage_efficiency": 0.40,
        "heat_loss_factor": 0.55,
        "vehicles": 100,
        "mist_output_lph": 5.0,
        "operating_hours": 8.0,
        "road_corridor_width_m": 30.0,
        "mixing_height_m": 5.0,
        "max_temp_drop_c": 5.0,
        "note": "High evap. efficiency, low humidity",
        "color": "#e07b39",
    },
    {
        "label": "Rainy Climate\nDual Supply",
        "short": "Rainy/Dual",
        "ambient_temp_c": 32.0,
        "relative_humidity": 55.0,
        "evaporation_efficiency": 0.45,
        "coverage_efficiency": 0.40,
        "heat_loss_factor": 0.60,
        "vehicles": 100,
        "mist_output_lph": 5.0,
        "operating_hours": 8.0,
        "road_corridor_width_m": 30.0,
        "mixing_height_m": 5.0,
        "max_temp_drop_c": 5.0,
        "note": "Moderate temp, moderate humidity",
        "color": "#4a90c4",
    },
    {
        "label": "High Humidity\nLow Evaporation",
        "short": "High Humid.",
        "ambient_temp_c": 34.0,
        "relative_humidity": 80.0,
        "evaporation_efficiency": 0.20,
        "coverage_efficiency": 0.30,
        "heat_loss_factor": 0.65,
        "vehicles": 100,
        "mist_output_lph": 5.0,
        "operating_hours": 8.0,
        "road_corridor_width_m": 30.0,
        "mixing_height_m": 5.0,
        "max_temp_drop_c": 5.0,
        "note": "High humidity — evap. much reduced",
        "color": "#6ab0a8",
    },
    {
        "label": "Dusty Desert\nMaintenance Limited",
        "short": "Dusty/Maint.",
        "ambient_temp_c": 44.0,
        "relative_humidity": 10.0,
        "evaporation_efficiency": 0.50,
        "coverage_efficiency": 0.20,
        "heat_loss_factor": 0.70,
        "vehicles": 100,
        "mist_output_lph": 3.5,
        "operating_hours": 8.0,
        "road_corridor_width_m": 30.0,
        "mixing_height_m": 5.0,
        "max_temp_drop_c": 5.0,
        "note": "Clogging risk, reduced output",
        "color": "#c4a44a",
    },
]

LATENT_HEAT_WATER_J_PER_KG = 2_450_000
AIR_DENSITY_KG_M3 = 1.2
AIR_SPECIFIC_HEAT_J_KG_K = 1005


def compute(s):
    total_mist_lph = s["vehicles"] * s["mist_output_lph"]
    total_water = total_mist_lph * s["operating_hours"]
    mist_kg_s = total_mist_lph / 3600.0
    raw_kw = mist_kg_s * LATENT_HEAT_WATER_J_PER_KG / 1000.0
    eff_kw = raw_kw * s["evaporation_efficiency"] * s["coverage_efficiency"] * (1.0 - s["heat_loss_factor"])
    air_mass = 30.0 * s["mixing_height_m"] * 1000.0 * AIR_DENSITY_KG_M3
    cooling_j = eff_kw * 1000.0 * 3600.0
    raw_dt = cooling_j / (air_mass * AIR_SPECIFIC_HEAT_J_KG_K)
    dt = min(raw_dt, s["max_temp_drop_c"])
    return {
        "total_water_lph": total_mist_lph,
        "total_water_hrs": total_water,
        "raw_kw": raw_kw,
        "eff_kw": eff_kw,
        "temp_drop_c": dt,
    }


def graph_water_use():
    labels = [s["short"] for s in SCENARIOS]
    colors = [s["color"] for s in SCENARIOS]
    vals_lph = []
    vals_total = []
    for s in SCENARIOS:
        r = compute(s)
        vals_lph.append(r["total_water_lph"])
        vals_total.append(r["total_water_hrs"])

    x = range(len(SCENARIOS))
    width = 0.35

    fig, ax = plt.subplots(figsize=(9, 5))
    bars1 = ax.bar([i - width / 2 for i in x], vals_lph, width, label="Water use per hour (L/hr)", color=colors, alpha=0.85)
    bars2 = ax.bar([i + width / 2 for i in x], [v / 100 for v in vals_total], width,
                   label=f"Total water use / 100 ({SCENARIOS[0]['operating_hours']:.0f}h) (L/100)",
                   color=colors, alpha=0.5, hatch="//")
    ax.set_xticks(list(x))
    ax.set_xticklabels(labels, fontsize=9)
    ax.set_ylabel("Liters", fontsize=10)
    ax.set_title("Illustrative Water Use — Four Scenarios\n(100 vehicles, conceptual estimate)", fontsize=11)
    ax.legend(fontsize=8)
    ax.text(0.5, -0.18, DISCLAIMER, transform=ax.transAxes,
            ha="center", va="top", fontsize=7, color="gray",
            wrap=True)
    plt.tight_layout()
    out = os.path.join(OUTPUT_DIR, "mobile_mist_cooling_water_use.png")
    plt.savefig(out, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Saved: {out}")


def graph_temperature_drop():
    labels = [s["short"] for s in SCENARIOS]
    colors = [s["color"] for s in SCENARIOS]
    vals = [compute(s)["temp_drop_c"] for s in SCENARIOS]
    notes = [s["note"] for s in SCENARIOS]

    fig, ax = plt.subplots(figsize=(9, 5))
    bars = ax.bar(labels, vals, color=colors, alpha=0.85, edgecolor="white")
    for bar, v, note in zip(bars, vals, notes):
        ax.text(bar.get_x() + bar.get_width() / 2.0, v + 0.03,
                f"{v:.3f} °C", ha="center", va="bottom", fontsize=9, fontweight="bold")
        ax.text(bar.get_x() + bar.get_width() / 2.0, v / 2.0,
                note, ha="center", va="center", fontsize=7, color="white", wrap=True)
    ax.set_ylabel("Illustrative Corridor Temperature Drop (°C)", fontsize=10)
    ax.set_title("Estimated Corridor Temperature Drop — Four Scenarios\n"
                 "(Conceptual model, assumption-based, capped at 5 °C)", fontsize=11)
    ax.set_ylim(0, max(vals) * 1.4 + 0.1)
    ax.text(0.5, -0.18, DISCLAIMER, transform=ax.transAxes,
            ha="center", va="top", fontsize=7, color="gray")
    plt.tight_layout()
    out = os.path.join(OUTPUT_DIR, "mobile_mist_cooling_temperature_drop.png")
    plt.savefig(out, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Saved: {out}")


def graph_scenario_comparison():
    labels = [s["short"] for s in SCENARIOS]
    colors = [s["color"] for s in SCENARIOS]
    metrics = ["evaporation_efficiency", "coverage_efficiency"]
    metric_labels = ["Evap. Efficiency", "Coverage Efficiency"]

    results = [compute(s) for s in SCENARIOS]
    eff_kws = [r["eff_kw"] for r in results]
    temp_drops = [r["temp_drop_c"] for r in results]
    evap_effs = [s["evaporation_efficiency"] for s in SCENARIOS]
    cov_effs = [s["coverage_efficiency"] for s in SCENARIOS]
    humidities = [s["relative_humidity"] for s in SCENARIOS]

    fig, axes = plt.subplots(1, 3, figsize=(14, 5))
    fig.suptitle("Mobile Mist Cooling — Scenario Comparison (Conceptual Estimates)", fontsize=12)

    x = range(len(SCENARIOS))

    # Panel 1: effective cooling power
    axes[0].bar(labels, eff_kws, color=colors, alpha=0.85)
    axes[0].set_title("Effective Cooling Power (kW)", fontsize=10)
    axes[0].set_ylabel("kW (illustrative)", fontsize=9)
    for i, v in enumerate(eff_kws):
        axes[0].text(i, v + 0.5, f"{v:.1f}", ha="center", va="bottom", fontsize=8)

    # Panel 2: temperature drop
    axes[1].bar(labels, temp_drops, color=colors, alpha=0.85)
    axes[1].set_title("Illustrative Temp. Drop (°C)", fontsize=10)
    axes[1].set_ylabel("°C (illustrative, capped)", fontsize=9)
    for i, v in enumerate(temp_drops):
        axes[1].text(i, v + 0.02, f"{v:.3f}", ha="center", va="bottom", fontsize=8)

    # Panel 3: key efficiency assumptions
    w = 0.35
    axes[2].bar([i - w / 2 for i in x], evap_effs, w, label="Evap. efficiency",
                color=colors, alpha=0.85)
    axes[2].bar([i + w / 2 for i in x], cov_effs, w, label="Coverage efficiency",
                color=colors, alpha=0.5, hatch="//")
    axes[2].set_xticks(list(x))
    axes[2].set_xticklabels(labels, fontsize=8)
    axes[2].set_title("Key Efficiency Assumptions", fontsize=10)
    axes[2].set_ylabel("Fraction (0–1)", fontsize=9)
    axes[2].legend(fontsize=8)

    for humidity, xi in zip(humidities, x):
        axes[2].text(xi, 0.02, f"RH {humidity:.0f}%", ha="center", va="bottom",
                     fontsize=7, color="black")

    fig.text(0.5, -0.04, DISCLAIMER, ha="center", va="top", fontsize=7, color="gray")
    plt.tight_layout()
    out = os.path.join(OUTPUT_DIR, "mobile_mist_cooling_scenario_comparison.png")
    plt.savefig(out, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Saved: {out}")


def main():
    print("Generating mobile mist cooling illustrative graphs...")
    print(f"Output directory: {OUTPUT_DIR}")
    graph_water_use()
    graph_temperature_drop()
    graph_scenario_comparison()
    print()
    print("All graphs generated.")
    print()
    print(DISCLAIMER)


if __name__ == "__main__":
    main()
