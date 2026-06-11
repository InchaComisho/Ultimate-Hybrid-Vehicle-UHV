"""Speed-energy profile estimator for the UHV concept.

The script compares theoretical Center-Mist latent cooling potential with
auxiliary AER-Loop wind recovery power across a speed range. It is a simplified
planning model, not validation of effective cooling or vehicle efficiency.
"""

import argparse
import csv


def estimate_latent_cooling_potential(
    mist_l_min,
    evap_efficiency,
    latent_heat_j_per_kg=2.4e6,
):
    """Estimate theoretical latent cooling potential in watts.

    Assumes 1 liter of water is approximately 1 kilogram. This is not validated
    effective cooling because it does not model droplet transport, humidity,
    road wetting, solar radiation, or human exposure.
    """
    mass_flow_kg_s = mist_l_min / 60.0
    return mass_flow_kg_s * latent_heat_j_per_kg * evap_efficiency


def estimate_wind_recovery_power(
    speed_kmh,
    rotor_area_m2,
    cp,
    conversion_efficiency,
    air_density_kg_m3=1.2,
):
    """Estimate auxiliary wind recovery power in watts.

    Vehicle-generated airflow recovery must be evaluated with aerodynamic drag.
    This should not be treated as main propulsion energy.
    """
    speed_m_s = speed_kmh / 3.6
    power_w = (
        0.5
        * air_density_kg_m3
        * rotor_area_m2
        * speed_m_s**3
        * cp
        * conversion_efficiency
    )
    return power_w


def build_profile(
    mist_l_min,
    evap_efficiency,
    rotor_area_m2,
    cp,
    conversion_efficiency,
    speed_min,
    speed_max,
    speed_step,
):
    """Build rows for a speed-energy profile table."""
    cooling_w = estimate_latent_cooling_potential(mist_l_min, evap_efficiency)
    rows = []
    speed = speed_min
    while speed <= speed_max + 1e-9:
        wind_w = estimate_wind_recovery_power(
            speed,
            rotor_area_m2,
            cp,
            conversion_efficiency,
        )
        rows.append({
            "speed_kmh": speed,
            "speed_m_s": speed / 3.6,
            "aer_loop_power_w": wind_w,
            "center_mist_theoretical_cooling_w": cooling_w,
        })
        speed += speed_step
    return rows


def write_csv(path, rows):
    """Write profile rows to CSV."""
    fieldnames = [
        "speed_kmh",
        "speed_m_s",
        "aer_loop_power_w",
        "center_mist_theoretical_cooling_w",
    ]
    with open(path, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def print_table(rows):
    """Print a simple aligned text table."""
    print("Speed-Energy Profile")
    print(
        f"{'Speed (km/h)':>12}  {'Speed (m/s)':>11}  "
        f"{'AER-Loop W':>12}  {'Center-Mist theoretical W':>28}"
    )
    print("-" * 72)
    for row in rows:
        print(
            f"{row['speed_kmh']:12.2f}  "
            f"{row['speed_m_s']:11.2f}  "
            f"{row['aer_loop_power_w']:12.2f}  "
            f"{row['center_mist_theoretical_cooling_w']:28.2f}"
        )


def parse_args():
    parser = argparse.ArgumentParser(
        description=(
            "Compare theoretical Center-Mist latent cooling potential with "
            "auxiliary AER-Loop wind recovery power across speed."
        )
    )
    parser.add_argument(
        "--mist-l-min",
        type=float,
        default=0.5,
        help="Mist water flow in liters per minute. Default: 0.5.",
    )
    parser.add_argument(
        "--evap-efficiency",
        type=float,
        default=0.7,
        help="Representative evaporation efficiency from 0 to 1. Default: 0.7.",
    )
    parser.add_argument(
        "--rotor-area",
        type=float,
        default=0.05,
        help="AER-Loop rotor or intake area in square meters. Default: 0.05.",
    )
    parser.add_argument(
        "--cp",
        type=float,
        default=0.15,
        help="Power coefficient for auxiliary wind recovery. Default: 0.15.",
    )
    parser.add_argument(
        "--conversion-efficiency",
        type=float,
        default=0.7,
        help="Generator and conversion efficiency from 0 to 1. Default: 0.7.",
    )
    parser.add_argument(
        "--speed-min",
        type=float,
        default=20.0,
        help="Minimum vehicle speed in km/h. Default: 20.",
    )
    parser.add_argument(
        "--speed-max",
        type=float,
        default=80.0,
        help="Maximum vehicle speed in km/h. Default: 80.",
    )
    parser.add_argument(
        "--speed-step",
        type=float,
        default=10.0,
        help="Vehicle speed step in km/h. Default: 10.",
    )
    parser.add_argument(
        "--csv",
        help="Optional CSV output path.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    if args.speed_step <= 0:
        raise SystemExit("--speed-step must be greater than 0")
    if args.speed_max < args.speed_min:
        raise SystemExit("--speed-max must be greater than or equal to --speed-min")

    rows = build_profile(
        args.mist_l_min,
        args.evap_efficiency,
        args.rotor_area,
        args.cp,
        args.conversion_efficiency,
        args.speed_min,
        args.speed_max,
        args.speed_step,
    )

    print_table(rows)
    print()
    print(
        "Warning: Cooling values are theoretical latent cooling potential, "
        "not validated effective cooling."
    )
    print(
        "Warning: Vehicle-generated airflow recovery must be evaluated "
        "together with aerodynamic drag."
    )

    if args.csv:
        write_csv(args.csv, rows)
        print(f"CSV written to: {args.csv}")


if __name__ == "__main__":
    main()
