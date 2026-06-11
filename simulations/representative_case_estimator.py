"""Representative UHV case estimator.

This script provides simplified order-of-magnitude estimates for v0.2.0
candidate validation planning. It does not validate UHV performance.
"""

import argparse


CASE_PRESETS = {
    "dry_desert_road": {
        "description": "Dry desert road representative case",
        "humidity_risk": "lower, if droplets evaporate before road contact",
        "airflow_note": "driving airflow may support evaporation, but wind direction matters",
    },
    "urban_bus_route": {
        "description": "Urban bus route representative case",
        "humidity_risk": "medium near stops and sidewalks",
        "airflow_note": "stop-and-go operation may reduce evaporation time",
    },
    "airport_port_service": {
        "description": "Airport or port service vehicle representative case",
        "humidity_risk": "site-specific; open yards may disperse humidity",
        "airflow_note": "crosswind and operating rules require validation",
    },
    "humid_climate": {
        "description": "Humid climate limitation representative case",
        "humidity_risk": "high; mist output may need to be reduced or disabled",
        "airflow_note": "evaporation may be slow even with vehicle airflow",
    },
    "night_low_wind": {
        "description": "Night or low-wind limitation representative case",
        "humidity_risk": "medium to high in enclosed or stagnant zones",
        "airflow_note": "low wind can allow local humidity accumulation",
    },
}


def estimate_evaporative_cooling(
    water_flow_l_per_hour,
    evaporation_efficiency=0.7,
    latent_heat_j_per_kg=2.4e6,
):
    """Estimate conceptual evaporative cooling power in watts.

    Assumes 1 liter of water is approximately 1 kilogram. The result is a
    simplified estimate and does not include droplet size, local wind, humidity
    saturation, road wetting, or vehicle aerodynamic effects.
    """
    mass_flow_kg_per_s = water_flow_l_per_hour / 3600.0
    return mass_flow_kg_per_s * latent_heat_j_per_kg * evaporation_efficiency


def estimate_water_use(vehicle_count, water_flow_l_per_hour, operation_hours):
    """Estimate total water use in liters for a vehicle group."""
    return vehicle_count * water_flow_l_per_hour * operation_hours


def estimate_representative_case(
    case_name,
    vehicle_count,
    water_flow_l_per_hour,
    operation_hours,
    evaporation_efficiency,
):
    """Return a dictionary of simplified representative case estimates."""
    preset = CASE_PRESETS.get(case_name, {
        "description": "Custom representative case",
        "humidity_risk": "unknown; requires site validation",
        "airflow_note": "airflow assumptions must be measured",
    })
    per_vehicle_w = estimate_evaporative_cooling(
        water_flow_l_per_hour,
        evaporation_efficiency=evaporation_efficiency,
    )
    total_water_l = estimate_water_use(
        vehicle_count,
        water_flow_l_per_hour,
        operation_hours,
    )
    return {
        "case_name": case_name,
        "description": preset["description"],
        "vehicle_count": vehicle_count,
        "water_flow_l_per_hour": water_flow_l_per_hour,
        "operation_hours": operation_hours,
        "evaporation_efficiency": evaporation_efficiency,
        "cooling_power_per_vehicle_w": per_vehicle_w,
        "cooling_power_total_w": per_vehicle_w * vehicle_count,
        "water_use_total_l": total_water_l,
        "humidity_risk": preset["humidity_risk"],
        "airflow_note": preset["airflow_note"],
    }


def main():
    parser = argparse.ArgumentParser(
        description="Estimate simplified representative UHV cooling and water-use cases."
    )
    parser.add_argument(
        "--case",
        default="dry_desert_road",
        choices=sorted(CASE_PRESETS.keys()) + ["custom"],
        help="Representative case name.",
    )
    parser.add_argument("--vehicles", type=int, default=1, help="Vehicle count.")
    parser.add_argument(
        "--water-flow",
        type=float,
        default=10.0,
        help="Water flow per vehicle in liters per hour.",
    )
    parser.add_argument(
        "--hours",
        type=float,
        default=1.0,
        help="Operation time in hours.",
    )
    parser.add_argument(
        "--efficiency",
        type=float,
        default=0.7,
        help="Representative evaporation efficiency from 0 to 1.",
    )
    args = parser.parse_args()

    result = estimate_representative_case(
        args.case,
        args.vehicles,
        args.water_flow,
        args.hours,
        args.efficiency,
    )

    print("Simplified UHV representative case estimate")
    print(f"Case: {result['description']}")
    print(f"Vehicles: {result['vehicle_count']}")
    print(f"Water flow per vehicle: {result['water_flow_l_per_hour']:.2f} L/h")
    print(f"Operation time: {result['operation_hours']:.2f} h")
    print(f"Evaporation efficiency: {result['evaporation_efficiency']:.2f}")
    print(f"Cooling per vehicle: {result['cooling_power_per_vehicle_w']:.2f} W")
    print(f"Cooling total: {result['cooling_power_total_w']:.2f} W")
    print(f"Water use total: {result['water_use_total_l']:.2f} L")
    print(f"Humidity risk: {result['humidity_risk']}")
    print(f"Airflow note: {result['airflow_note']}")
    print(
        "Warning: outputs are simplified conceptual estimates. They are not "
        "validated cooling results and do not include drag, visibility, road "
        "wetting, human exposure, or local climate validation."
    )


if __name__ == "__main__":
    main()
