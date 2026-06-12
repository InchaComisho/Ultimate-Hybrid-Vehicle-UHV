"""Conceptual UHV control-state example.

This script is a simplified reference for discussing candidate control logic.
It is not certified vehicle safety software.
"""

import argparse


def evaluate_control_state(args):
    """Evaluate a conceptual UHV control state from CLI arguments."""
    reasons = []

    if args.fault:
        return "FAIL_SAFE_OFF", "disabled", ["fault detected"]

    if args.rain:
        reasons.append("rain detected")
    if not args.visibility_ok:
        reasons.append("visibility not confirmed safe")
    if args.road_wet:
        reasons.append("road surface wet")
    if args.pedestrian_near:
        reasons.append("pedestrian or cyclist proximity")
    if not args.water_quality_ok:
        reasons.append("water quality not confirmed safe")
    if args.humidity >= 75:
        reasons.append("humidity too high")
    if args.battery_soc < 20:
        reasons.append("auxiliary battery state too low")
    if args.temperature_c <= 0:
        reasons.append("freezing conditions possible")

    if args.speed_kmh == 0:
        mode = "PARKING_SHIELD"
        if reasons:
            return mode, "disabled", reasons
        if args.temperature_c >= 30 and args.humidity < 65:
            return mode, "allowed", ["parking checks passed"]
        return mode, "reduced", ["parking mode but thermal/dryness conditions are marginal"]

    if args.speed_kmh <= 10:
        mode = "LOW_SPEED_STANDBY"
        if reasons:
            return mode, "disabled", reasons
        return mode, "reduced", ["low-speed area; pedestrian safety priority"]

    if args.speed_kmh <= 40:
        mode = "LOW_SPEED_URBAN"
        if reasons:
            return mode, "disabled", reasons
        if args.temperature_c >= 30 and args.humidity < 60:
            return mode, "allowed", ["dry hot low-speed candidate conditions"]
        return mode, "reduced", ["urban mode but thermal/dryness conditions are marginal"]

    if args.speed_kmh <= 60:
        mode = "REDUCED_OUTPUT"
        if reasons:
            return mode, "disabled", reasons
        return mode, "reduced", ["40-60 km/h conceptual baseline reduces exterior mist"]

    return "HIGH_SPEED_DISABLED", "disabled", ["speed exceeds conceptual exterior mist range"]


def parse_args():
    parser = argparse.ArgumentParser(
        description="Evaluate a conceptual UHV adaptive control state."
    )
    parser.add_argument("--speed-kmh", type=float, required=True, help="Vehicle speed in km/h.")
    parser.add_argument("--temperature-c", type=float, required=True, help="Ambient temperature in C.")
    parser.add_argument("--humidity", type=float, required=True, help="Relative humidity percent.")
    parser.add_argument("--visibility-ok", action="store_true", help="Set when visibility is acceptable.")
    parser.add_argument("--road-wet", action="store_true", help="Set when road surface is wet.")
    parser.add_argument("--pedestrian-near", action="store_true", help="Set when pedestrians/cyclists are nearby.")
    parser.add_argument("--water-quality-ok", action="store_true", help="Set when water quality is acceptable.")
    parser.add_argument("--battery-soc", type=float, required=True, help="Auxiliary battery state of charge percent.")
    parser.add_argument("--rain", action="store_true", help="Set when rain is detected.")
    parser.add_argument("--fault", action="store_true", help="Set when any sensor/system fault is detected.")
    return parser.parse_args()


def main():
    args = parse_args()
    mode, permission, reasons = evaluate_control_state(args)

    print("UHV conceptual control-state evaluation")
    print(f"Selected mode: {mode}")
    print(f"Mist permission: {permission}")
    print("Reasons:")
    for reason in reasons:
        print(f"- {reason}")
    print(
        "Warning: This is a conceptual control-state example, not certified "
        "vehicle safety software."
    )
    print(
        "Warning: Real implementation requires automotive safety engineering, "
        "redundancy, validation, and legal approval."
    )


if __name__ == "__main__":
    main()
