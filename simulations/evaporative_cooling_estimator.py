"""Simplified evaporative cooling estimator for the UHV concept."""

import argparse


def estimate_evaporative_cooling(
    water_flow_l_per_hour,
    evaporation_efficiency=0.7,
    latent_heat_j_per_kg=2.4e6,
):
    """Estimate cooling power in watts from water flow and evaporation efficiency.

    This simplified model assumes 1 liter of water has a mass of 1 kilogram.
    It does not model humidity, droplet size, airflow, heat transfer limits, or
    incomplete mixing, so prototype and field measurements are still required.
    """
    mass_flow_kg_per_s = water_flow_l_per_hour / 3600.0
    return mass_flow_kg_per_s * latent_heat_j_per_kg * evaporation_efficiency


def main():
    parser = argparse.ArgumentParser(
        description="Estimate simplified evaporative cooling power for a UHV mist system."
    )
    parser.add_argument(
        "--water-flow",
        type=float,
        required=True,
        help="Water flow rate in liters per hour.",
    )
    parser.add_argument(
        "--efficiency",
        type=float,
        default=0.7,
        help="Evaporation efficiency factor from 0 to 1. Default: 0.7.",
    )
    parser.add_argument(
        "--latent-heat",
        type=float,
        default=2.4e6,
        help="Latent heat of vaporization in J/kg. Default: 2.4e6.",
    )
    args = parser.parse_args()

    cooling_w = estimate_evaporative_cooling(
        args.water_flow,
        evaporation_efficiency=args.efficiency,
        latent_heat_j_per_kg=args.latent_heat,
    )

    print("Simplified evaporative cooling estimate")
    print(f"Cooling power: {cooling_w:.2f} W")
    print(f"Cooling power: {cooling_w / 1000.0:.3f} kW")


if __name__ == "__main__":
    main()
