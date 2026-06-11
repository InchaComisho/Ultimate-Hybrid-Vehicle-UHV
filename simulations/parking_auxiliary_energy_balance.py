"""Parking auxiliary energy balance estimator for the UHV concept.

This script estimates a simplified daily auxiliary energy balance from protected
solar skin input, parked natural-wind auxiliary generation, and standby loads.
It is not a validated vehicle charging model.
"""

import argparse


def estimate_solar_wh_day(solar_area, solar_irradiance, solar_efficiency, solar_hours):
    """Estimate protected solar skin energy in Wh/day."""
    solar_power_w = solar_area * solar_irradiance * solar_efficiency
    return solar_power_w * solar_hours


def estimate_wind_wh_day(
    wind_area,
    wind_speed,
    cp,
    conversion_efficiency,
    operation_hours,
    air_density=1.2,
):
    """Estimate parked natural-wind auxiliary energy in Wh/day."""
    wind_power_w = (
        0.5
        * air_density
        * wind_area
        * wind_speed**3
        * cp
        * conversion_efficiency
    )
    return wind_power_w * operation_hours


def estimate_energy_balance(
    solar_area,
    solar_irradiance,
    solar_efficiency,
    solar_hours,
    wind_area,
    wind_speed,
    cp,
    conversion_efficiency,
    operation_hours,
    standby_load_w,
):
    """Return a simplified daily auxiliary energy balance."""
    solar_wh = estimate_solar_wh_day(
        solar_area,
        solar_irradiance,
        solar_efficiency,
        solar_hours,
    )
    wind_wh = estimate_wind_wh_day(
        wind_area,
        wind_speed,
        cp,
        conversion_efficiency,
        operation_hours,
    )
    standby_wh = standby_load_w * operation_hours
    total_wh = solar_wh + wind_wh
    return {
        "solar_wh_day": solar_wh,
        "wind_wh_day": wind_wh,
        "total_auxiliary_wh_day": total_wh,
        "standby_load_wh_day": standby_wh,
        "surplus_or_deficit_wh_day": total_wh - standby_wh,
    }


def parse_args():
    parser = argparse.ArgumentParser(
        description="Estimate simplified UHV parked auxiliary energy balance."
    )
    parser.add_argument("--solar-area", type=float, required=True, help="Solar area in m^2.")
    parser.add_argument(
        "--solar-irradiance",
        type=float,
        required=True,
        help="Representative solar irradiance in W/m^2.",
    )
    parser.add_argument(
        "--solar-efficiency",
        type=float,
        required=True,
        help="Protected solar module efficiency from 0 to 1.",
    )
    parser.add_argument(
        "--solar-hours",
        type=float,
        required=True,
        help="Equivalent sun hours per day.",
    )
    parser.add_argument(
        "--wind-area",
        type=float,
        required=True,
        help="Vertical-axis wind rotor or intake area in m^2.",
    )
    parser.add_argument(
        "--wind-speed",
        type=float,
        required=True,
        help="Average natural wind speed while parked in m/s.",
    )
    parser.add_argument("--cp", type=float, required=True, help="Wind power coefficient.")
    parser.add_argument(
        "--conversion-efficiency",
        type=float,
        required=True,
        help="Generator and charge conversion efficiency from 0 to 1.",
    )
    parser.add_argument(
        "--operation-hours",
        type=float,
        required=True,
        help="Hours per day for wind generation and standby load.",
    )
    parser.add_argument(
        "--standby-load-w",
        type=float,
        required=True,
        help="Auxiliary standby load in watts.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    result = estimate_energy_balance(
        args.solar_area,
        args.solar_irradiance,
        args.solar_efficiency,
        args.solar_hours,
        args.wind_area,
        args.wind_speed,
        args.cp,
        args.conversion_efficiency,
        args.operation_hours,
        args.standby_load_w,
    )

    print("Simplified UHV parking auxiliary energy balance")
    print(f"Estimated solar energy: {result['solar_wh_day']:.2f} Wh/day")
    print(f"Estimated wind energy: {result['wind_wh_day']:.2f} Wh/day")
    print(f"Total auxiliary energy: {result['total_auxiliary_wh_day']:.2f} Wh/day")
    print(f"Standby load: {result['standby_load_wh_day']:.2f} Wh/day")
    print(f"Surplus or deficit: {result['surplus_or_deficit_wh_day']:.2f} Wh/day")
    print(
        "Warning: This is a simplified auxiliary energy estimate, not a "
        "validated vehicle charging model."
    )
    print(
        "Warning: Main battery support requires certified BMS and DC-DC integration."
    )


if __name__ == "__main__":
    main()
