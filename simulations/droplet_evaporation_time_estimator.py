"""Simplified droplet evaporation time estimator for UHV mist screening."""

import argparse


def estimate_droplet_evaporation_time(
    droplet_diameter_um,
    temperature_c,
    relative_humidity_percent,
    wind_speed_m_s,
):
    """Estimate conceptual droplet evaporation time in seconds.

    This is a heuristic screening model, not a physical validation model. It
    uses droplet diameter squared, humidity, temperature, and wind speed as
    coarse drivers so prototype teams can compare relative scenarios.
    """
    diameter_factor = (droplet_diameter_um / 20.0) ** 2
    humidity_factor = 1.0 / max(0.05, 1.0 - relative_humidity_percent / 100.0)
    temperature_factor = 30.0 / max(5.0, temperature_c)
    wind_factor = 1.0 / (1.0 + 0.35 * max(0.0, wind_speed_m_s))
    base_seconds = 0.8
    return base_seconds * diameter_factor * humidity_factor * temperature_factor * wind_factor


def main():
    parser = argparse.ArgumentParser(
        description="Estimate simplified mist droplet evaporation time for scenario screening."
    )
    parser.add_argument(
        "--diameter",
        type=float,
        required=True,
        help="Droplet diameter in micrometers.",
    )
    parser.add_argument(
        "--temperature",
        type=float,
        required=True,
        help="Ambient temperature in degrees Celsius.",
    )
    parser.add_argument(
        "--humidity",
        type=float,
        required=True,
        help="Relative humidity in percent.",
    )
    parser.add_argument(
        "--wind-speed",
        type=float,
        default=1.0,
        help="Local wind or airflow speed in m/s.",
    )
    args = parser.parse_args()

    seconds = estimate_droplet_evaporation_time(
        args.diameter,
        args.temperature,
        args.humidity,
        args.wind_speed,
    )

    print("Simplified droplet evaporation time estimate")
    print(f"Estimated time: {seconds:.2f} s")
    print(
        "Warning: this is a heuristic conceptual estimate, not a validated "
        "droplet physics model. Use controlled tests for real design decisions."
    )


if __name__ == "__main__":
    main()
