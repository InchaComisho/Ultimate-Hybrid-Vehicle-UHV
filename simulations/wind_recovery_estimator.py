"""Simplified auxiliary wind recovery estimator for the UHV concept."""

import argparse


def estimate_wind_power(
    area_m2,
    wind_speed_m_s,
    cp=0.25,
    efficiency=0.7,
    air_density=1.225,
):
    """Estimate recoverable wind power in watts.

    Uses P = 0.5 * rho * A * v^3 * Cp * eta.

    For vehicle-generated airflow, recovered power must be evaluated together
    with increased aerodynamic drag. This is not a main propulsion energy source.
    """
    return 0.5 * air_density * area_m2 * wind_speed_m_s**3 * cp * efficiency


def main():
    parser = argparse.ArgumentParser(
        description="Estimate simplified auxiliary wind recovery power for UHV."
    )
    parser.add_argument("--area", type=float, required=True, help="Swept or intake area in m^2.")
    parser.add_argument("--speed", type=float, required=True, help="Wind speed in m/s.")
    parser.add_argument("--cp", type=float, default=0.25, help="Power coefficient. Default: 0.25.")
    parser.add_argument(
        "--efficiency",
        type=float,
        default=0.7,
        help="Generator and conversion efficiency. Default: 0.7.",
    )
    parser.add_argument(
        "--air-density",
        type=float,
        default=1.225,
        help="Air density in kg/m^3. Default: 1.225.",
    )
    args = parser.parse_args()

    power_w = estimate_wind_power(
        args.area,
        args.speed,
        cp=args.cp,
        efficiency=args.efficiency,
        air_density=args.air_density,
    )

    print("Simplified auxiliary wind recovery estimate")
    print(f"Recovered auxiliary power: {power_w:.2f} W")
    print(f"Recovered auxiliary power: {power_w / 1000.0:.3f} kW")
    print(
        "Warning: For vehicle-generated airflow, recovered power must be evaluated "
        "together with increased aerodynamic drag. This is not a main propulsion energy source."
    )


if __name__ == "__main__":
    main()
