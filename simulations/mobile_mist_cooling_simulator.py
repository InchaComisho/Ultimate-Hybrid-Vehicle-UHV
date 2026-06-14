"""
mobile_mist_cooling_simulator.py

Illustrative simplified cooling estimate for ultrasonic-mist-equipped
mobility units operating across roads or urban corridors.

This is NOT a CFD simulation.
This does NOT predict certified real-world temperature reduction.
All outputs are conceptual assumption-based estimates only.
Field testing is required before making any engineering claims.
"""

import argparse
import json
import csv
import os
import sys

LATENT_HEAT_WATER_J_PER_KG = 2_450_000
AIR_DENSITY_KG_M3 = 1.2
AIR_SPECIFIC_HEAT_J_KG_K = 1005

DISCLAIMER = """
---
DISCLAIMER
This is an illustrative simplified cooling estimate.
It is not a CFD simulation.
It does not predict certified real-world temperature reduction.
Actual cooling depends on humidity, wind, solar radiation, road geometry,
traffic density, droplet size, evaporation rate, airflow, water quality,
maintenance condition, and urban heat storage.
All values are assumption-based estimates for conceptual comparison only.
Field testing is required before making any engineering claims.
---
"""


def run_simulation(args):
    vehicles = args.vehicles
    mist_output_lph = args.mist_output_lph
    operating_hours = args.operating_hours
    ambient_temp_c = args.ambient_temp_c
    relative_humidity = args.relative_humidity
    wind_speed_ms = args.wind_speed_ms
    road_corridor_width_m = args.road_corridor_width_m
    mixing_height_m = args.mixing_height_m
    vehicle_speed_kmh = args.vehicle_speed_kmh
    evaporation_efficiency = args.evaporation_efficiency
    coverage_efficiency = args.coverage_efficiency
    heat_loss_factor = args.heat_loss_factor
    max_temp_drop_c = args.max_temp_drop_c

    # Total mist water output
    total_mist_lph = vehicles * mist_output_lph  # liters per hour
    total_mist_kg_per_hour = total_mist_lph / 1000.0 * 1000.0  # 1 L = 1 kg for water
    total_water_use_liters = total_mist_lph * operating_hours

    # Latent cooling power (raw, if all water evaporated instantly)
    mist_kg_per_second = total_mist_kg_per_hour / 3600.0
    raw_cooling_power_w = mist_kg_per_second * LATENT_HEAT_WATER_J_PER_KG

    # Apply evaporation efficiency
    evap_cooling_w = raw_cooling_power_w * evaporation_efficiency

    # Apply coverage efficiency (fraction of corridor actually covered)
    covered_cooling_w = evap_cooling_w * coverage_efficiency

    # Apply heat loss / dilution factor (convection, wind mixing, losses)
    effective_cooling_w = covered_cooling_w * (1.0 - heat_loss_factor)

    # Estimate air volume in representative corridor segment
    # Assume corridor length based on vehicles at their speed spread over 1 hour
    # Use a simplified 1 km representative segment for scaling
    corridor_length_m = 1000.0
    air_volume_m3 = road_corridor_width_m * mixing_height_m * corridor_length_m
    air_mass_kg = air_volume_m3 * AIR_DENSITY_KG_M3

    # Effective cooling energy applied to corridor air mass over 1 hour
    effective_cooling_energy_j = effective_cooling_w * 3600.0

    # Temperature drop estimate (simplified, without accounting for solar reload)
    if air_mass_kg > 0 and AIR_SPECIFIC_HEAT_J_KG_K > 0:
        raw_temp_drop_c = effective_cooling_energy_j / (air_mass_kg * AIR_SPECIFIC_HEAT_J_KG_K)
    else:
        raw_temp_drop_c = 0.0

    # Cap the estimated temperature drop
    estimated_temp_drop_c = min(raw_temp_drop_c, max_temp_drop_c)

    # Humidity note: high humidity reduces evaporation efficiency
    humidity_note = ""
    if relative_humidity >= 70:
        humidity_note = "High humidity - evaporation efficiency may be significantly lower than assumed."
    elif relative_humidity >= 50:
        humidity_note = "Moderate humidity - evaporation efficiency may be reduced."
    else:
        humidity_note = "Low humidity - evaporative cooling conditions may be favorable."

    results = {
        "scenario": {
            "vehicles": vehicles,
            "mist_output_lph_per_vehicle": mist_output_lph,
            "operating_hours": operating_hours,
            "ambient_temp_c": ambient_temp_c,
            "relative_humidity_pct": relative_humidity,
            "wind_speed_ms": wind_speed_ms,
            "road_corridor_width_m": road_corridor_width_m,
            "mixing_height_m": mixing_height_m,
            "vehicle_speed_kmh": vehicle_speed_kmh,
            "evaporation_efficiency": evaporation_efficiency,
            "coverage_efficiency": coverage_efficiency,
            "heat_loss_factor": heat_loss_factor,
            "max_temp_drop_cap_c": max_temp_drop_c,
        },
        "estimates": {
            "total_mist_water_use_per_hour_liters": round(total_mist_lph, 2),
            "total_water_use_over_operating_hours_liters": round(total_water_use_liters, 2),
            "raw_latent_cooling_power_kw": round(raw_cooling_power_w / 1000.0, 3),
            "effective_cooling_power_after_efficiency_kw": round(effective_cooling_w / 1000.0, 3),
            "estimated_corridor_temperature_drop_c": round(estimated_temp_drop_c, 3),
            "raw_uncapped_temperature_drop_c": round(raw_temp_drop_c, 3),
            "humidity_note": humidity_note,
        },
        "disclaimer": (
            "This is an illustrative simplified cooling estimate. "
            "It is not a CFD simulation. "
            "It does not predict certified real-world temperature reduction. "
            "Actual cooling depends on humidity, wind, solar radiation, road geometry, "
            "traffic density, droplet size, evaporation rate, airflow, water quality, "
            "maintenance condition, and urban heat storage. "
            "Field testing is required before making any engineering claims."
        ),
    }
    return results


def print_results(results):
    s = results["scenario"]
    e = results["estimates"]
    print()
    print("=" * 60)
    print("Mobile Mist Cooling Simulator - Conceptual Estimate")
    print("=" * 60)
    print()
    print("Scenario Parameters:")
    print(f"  Vehicles:                   {s['vehicles']}")
    print(f"  Mist output per vehicle:    {s['mist_output_lph_per_vehicle']} L/hr")
    print(f"  Operating hours:            {s['operating_hours']} hr")
    print(f"  Ambient temperature:        {s['ambient_temp_c']} °C")
    print(f"  Relative humidity:          {s['relative_humidity_pct']} %")
    print(f"  Wind speed:                 {s['wind_speed_ms']} m/s")
    print(f"  Road corridor width:        {s['road_corridor_width_m']} m")
    print(f"  Mixing height:              {s['mixing_height_m']} m")
    print(f"  Vehicle speed:              {s['vehicle_speed_kmh']} km/h")
    print(f"  Evaporation efficiency:     {s['evaporation_efficiency']}")
    print(f"  Coverage efficiency:        {s['coverage_efficiency']}")
    print(f"  Heat loss / dilution:       {s['heat_loss_factor']}")
    print(f"  Max temp drop cap:          {s['max_temp_drop_cap_c']} °C")
    print()
    print("Illustrative Estimates:")
    print(f"  Total mist water use/hr:    {e['total_mist_water_use_per_hour_liters']:.1f} L/hr")
    print(f"  Total water use ({s['operating_hours']}h):    {e['total_water_use_over_operating_hours_liters']:.1f} L")
    print(f"  Raw latent cooling power:   {e['raw_latent_cooling_power_kw']:.2f} kW")
    print(f"  Effective cooling power:    {e['effective_cooling_power_after_efficiency_kw']:.2f} kW")
    print(f"  Est. corridor temp drop:    {e['estimated_corridor_temperature_drop_c']:.3f} °C (capped at {s['max_temp_drop_cap_c']} °C)")
    print(f"  Uncapped raw estimate:      {e['raw_uncapped_temperature_drop_c']:.3f} °C")
    print()
    print(f"  Humidity note: {e['humidity_note']}")
    print()
    print(DISCLAIMER)


def write_markdown(results, path):
    s = results["scenario"]
    e = results["estimates"]
    lines = [
        "# Mobile Mist Cooling — Illustrative Sample Results",
        "",
        "> **Disclaimer:** This is an illustrative simplified cooling estimate.",
        "> It is not a CFD simulation.",
        "> It does not predict certified real-world temperature reduction.",
        "> Actual cooling depends on humidity, wind, solar radiation, road geometry,",
        "> traffic density, droplet size, evaporation rate, airflow, water quality,",
        "> maintenance condition, and urban heat storage.",
        "> Field testing is required before making any engineering claims.",
        "",
        "## Scenario Parameters",
        "",
        "| Parameter | Value |",
        "|---|---|",
        f"| Vehicles | {s['vehicles']} |",
        f"| Mist output per vehicle | {s['mist_output_lph_per_vehicle']} L/hr |",
        f"| Operating hours | {s['operating_hours']} hr |",
        f"| Ambient temperature | {s['ambient_temp_c']} °C |",
        f"| Relative humidity | {s['relative_humidity_pct']} % |",
        f"| Wind speed | {s['wind_speed_ms']} m/s |",
        f"| Road corridor width | {s['road_corridor_width_m']} m |",
        f"| Mixing height | {s['mixing_height_m']} m |",
        f"| Vehicle speed | {s['vehicle_speed_kmh']} km/h |",
        f"| Evaporation efficiency | {s['evaporation_efficiency']} |",
        f"| Coverage efficiency | {s['coverage_efficiency']} |",
        f"| Heat loss / dilution factor | {s['heat_loss_factor']} |",
        f"| Max temperature drop cap | {s['max_temp_drop_cap_c']} °C |",
        "",
        "## Illustrative Estimates",
        "",
        "| Output | Value |",
        "|---|---|",
        f"| Total mist water use per hour | {e['total_mist_water_use_per_hour_liters']:.1f} L/hr |",
        f"| Total water use over operating hours | {e['total_water_use_over_operating_hours_liters']:.1f} L |",
        f"| Raw latent cooling power | {e['raw_latent_cooling_power_kw']:.2f} kW |",
        f"| Effective cooling power (after efficiency) | {e['effective_cooling_power_after_efficiency_kw']:.2f} kW |",
        f"| Estimated corridor temperature drop | {e['estimated_corridor_temperature_drop_c']:.3f} °C (capped at {s['max_temp_drop_cap_c']} °C) |",
        f"| Uncapped raw temperature estimate | {e['raw_uncapped_temperature_drop_c']:.3f} °C |",
        "",
        f"**Humidity note:** {e['humidity_note']}",
        "",
        "## Interpretation",
        "",
        "This representative scenario uses 100 vehicles operating for 8 hours in a hot dry corridor.",
        "The estimated corridor temperature drop is a conceptual illustration only.",
        "It should not be interpreted as a guaranteed or measurable outcome.",
        "",
        "Actual results depend on:",
        "",
        "- Humidity and wind conditions",
        "- Solar radiation and urban heat storage",
        "- Droplet size and evaporation rate",
        "- Nozzle and filter maintenance condition",
        "- Water quality and mineral content",
        "- Road geometry and traffic density",
        "- Vehicle spacing and distribution",
        "",
        "This is a conceptual model. Field testing is required.",
    ]
    os.makedirs(os.path.dirname(path) if os.path.dirname(path) else ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"Markdown output written to: {path}")


def write_csv(results, path):
    s = results["scenario"]
    e = results["estimates"]
    rows = [
        ["parameter_or_output", "value", "unit"],
        ["vehicles", s["vehicles"], "count"],
        ["mist_output_per_vehicle", s["mist_output_lph_per_vehicle"], "L/hr"],
        ["operating_hours", s["operating_hours"], "hr"],
        ["ambient_temp_c", s["ambient_temp_c"], "°C"],
        ["relative_humidity", s["relative_humidity_pct"], "%"],
        ["wind_speed_ms", s["wind_speed_ms"], "m/s"],
        ["road_corridor_width_m", s["road_corridor_width_m"], "m"],
        ["mixing_height_m", s["mixing_height_m"], "m"],
        ["vehicle_speed_kmh", s["vehicle_speed_kmh"], "km/h"],
        ["evaporation_efficiency", s["evaporation_efficiency"], "fraction"],
        ["coverage_efficiency", s["coverage_efficiency"], "fraction"],
        ["heat_loss_factor", s["heat_loss_factor"], "fraction"],
        ["max_temp_drop_cap", s["max_temp_drop_cap_c"], "°C"],
        ["total_mist_water_use_per_hour", e["total_mist_water_use_per_hour_liters"], "L/hr"],
        ["total_water_use_over_operating_hours", e["total_water_use_over_operating_hours_liters"], "L"],
        ["raw_latent_cooling_power_kw", e["raw_latent_cooling_power_kw"], "kW"],
        ["effective_cooling_power_kw", e["effective_cooling_power_after_efficiency_kw"], "kW"],
        ["estimated_corridor_temp_drop_c", e["estimated_corridor_temperature_drop_c"], "°C (capped)"],
        ["raw_uncapped_temp_drop_c", e["raw_uncapped_temperature_drop_c"], "°C"],
    ]
    os.makedirs(os.path.dirname(path) if os.path.dirname(path) else ".", exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(rows)
    print(f"CSV output written to: {path}")


def write_summary_json(results, path):
    os.makedirs(os.path.dirname(path) if os.path.dirname(path) else ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"JSON summary written to: {path}")


def parse_args():
    parser = argparse.ArgumentParser(
        description=(
            "Mobile Mist Cooling Simulator — conceptual estimate only. "
            "Not a CFD model. Not a certified thermal forecast."
        )
    )
    parser.add_argument("--vehicles", type=int, default=100)
    parser.add_argument("--mist-output-lph", type=float, default=5.0,
                        dest="mist_output_lph",
                        help="Mist output per vehicle in liters per hour")
    parser.add_argument("--operating-hours", type=float, default=8.0,
                        dest="operating_hours")
    parser.add_argument("--ambient-temp-c", type=float, default=40.0,
                        dest="ambient_temp_c")
    parser.add_argument("--relative-humidity", type=float, default=25.0,
                        dest="relative_humidity",
                        help="Relative humidity in percent (0-100)")
    parser.add_argument("--wind-speed-ms", type=float, default=2.0,
                        dest="wind_speed_ms")
    parser.add_argument("--road-corridor-width-m", type=float, default=30.0,
                        dest="road_corridor_width_m")
    parser.add_argument("--mixing-height-m", type=float, default=5.0,
                        dest="mixing_height_m")
    parser.add_argument("--vehicle-speed-kmh", type=float, default=30.0,
                        dest="vehicle_speed_kmh")
    parser.add_argument("--evaporation-efficiency", type=float, default=0.55,
                        dest="evaporation_efficiency",
                        help="Fraction of mist that evaporates (0-1)")
    parser.add_argument("--coverage-efficiency", type=float, default=0.35,
                        dest="coverage_efficiency",
                        help="Fraction of corridor actually cooled (0-1)")
    parser.add_argument("--heat-loss-factor", type=float, default=0.60,
                        dest="heat_loss_factor",
                        help="Fraction of cooling lost to convection/wind dilution (0-1)")
    parser.add_argument("--max-temp-drop-c", type=float, default=5.0,
                        dest="max_temp_drop_c",
                        help="Cap on estimated temperature drop in °C")
    parser.add_argument("--output-markdown", type=str, default=None,
                        dest="output_markdown")
    parser.add_argument("--output-csv", type=str, default=None,
                        dest="output_csv")
    parser.add_argument("--output-summary-json", type=str, default=None,
                        dest="output_summary_json")
    return parser.parse_args()


def main():
    args = parse_args()
    results = run_simulation(args)
    print_results(results)

    if args.output_markdown:
        write_markdown(results, args.output_markdown)
    if args.output_csv:
        write_csv(results, args.output_csv)
    if args.output_summary_json:
        write_summary_json(results, args.output_summary_json)


if __name__ == "__main__":
    main()
