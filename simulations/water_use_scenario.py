"""Water-use scenario estimator for UHV validation planning."""

import argparse


def estimate_water_use(vehicle_count, water_flow_l_per_hour, operation_hours):
    """Estimate total water use in liters."""
    return vehicle_count * water_flow_l_per_hour * operation_hours


def main():
    parser = argparse.ArgumentParser(
        description="Estimate simplified water demand for UHV mist-cooling scenarios."
    )
    parser.add_argument("--vehicles", type=int, required=True, help="Number of vehicles.")
    parser.add_argument(
        "--water-flow",
        type=float,
        required=True,
        help="Water flow per vehicle in liters per hour.",
    )
    parser.add_argument(
        "--hours",
        type=float,
        required=True,
        help="Operation hours per day.",
    )
    parser.add_argument(
        "--days",
        type=float,
        default=1.0,
        help="Number of operating days for seasonal estimate.",
    )
    args = parser.parse_args()

    daily_l = estimate_water_use(args.vehicles, args.water_flow, args.hours)
    seasonal_l = daily_l * args.days

    print("Simplified UHV water-use scenario")
    print(f"Vehicles: {args.vehicles}")
    print(f"Water flow per vehicle: {args.water_flow:.2f} L/h")
    print(f"Operation: {args.hours:.2f} h/day")
    print(f"Daily water use: {daily_l:.2f} L/day")
    print(f"Seasonal water use: {seasonal_l:.2f} L over {args.days:.1f} days")
    print(
        "Warning: water demand must be compared with measured cooling benefit, "
        "local water-resource constraints, hygiene requirements, and regulations."
    )


if __name__ == "__main__":
    main()
