"""
Speed Governance and Life-Protection Control Layer — Conceptual Simulation

WARNING: This is a conceptual safety-governance example, not certified vehicle safety software.
Real implementation requires automotive safety engineering, redundancy, validation, legal
approval, and regulatory compliance. No guarantee of accident reduction is made or implied.
"""

import argparse
import sys


_DISCLAIMER = (
    "WARNING: This is a conceptual safety-governance example, "
    "not certified vehicle safety software.\n"
    "Real implementation requires automotive safety engineering, redundancy, "
    "validation, legal approval, and regulatory compliance."
)

_FAILSAFE_SPEED_KMH = 30


def run_governance(args):
    driver_request = args.driver_speed_request
    legal_limit = args.legal_speed_limit

    warnings = []
    reasons = []
    safety_mode = "normal"

    # Sensor fault takes priority — enter fail-safe mode immediately.
    if args.sensor_fault:
        safety_mode = "failsafe"
        target_speed = _FAILSAFE_SPEED_KMH
        warnings.append("SENSOR FAULT DETECTED — entering fail-safe limited-speed mode")
        reasons.append(
            f"One or more sensors reported a fault. Speed limited to {_FAILSAFE_SPEED_KMH} km/h. "
            "Driver alert required. Seek service."
        )
        return target_speed, safety_mode, warnings, reasons

    # Start from driver request, apply legal limit as upper bound.
    target_speed = driver_request

    if legal_limit is not None and driver_request > legal_limit:
        target_speed = legal_limit
        reasons.append(
            f"Driver requested {driver_request} km/h exceeds legal limit of {legal_limit} km/h. "
            f"Target capped at {legal_limit} km/h."
        )

    # High-risk context: school zone, pedestrian, or intersection.
    if args.school_zone or args.pedestrian_near or args.intersection_near:
        safety_mode = "reduced_speed"
        context_parts = []
        if args.school_zone:
            context_parts.append("school zone")
        if args.pedestrian_near:
            context_parts.append("pedestrian detected nearby")
        if args.intersection_near:
            context_parts.append("intersection proximity")

        # Candidate reduced speed: lower of current target or legal limit / 2, minimum 10.
        base = legal_limit if legal_limit is not None else target_speed
        reduced = max(10, min(target_speed, base // 2))
        if reduced < target_speed:
            target_speed = reduced
            reasons.append(
                f"High-risk context detected ({', '.join(context_parts)}). "
                f"Speed reduced to {target_speed} km/h. "
                "Specific threshold requires validation and regulatory guidance."
            )

    # Weather conditions.
    if args.road_wet or args.rain or not args.visibility_ok:
        safety_mode = "weather_adjusted"
        weather_parts = []
        if args.rain:
            weather_parts.append("rain")
        if args.road_wet:
            weather_parts.append("wet road")
        if not args.visibility_ok:
            weather_parts.append("reduced visibility")

        # Candidate weather adjustment: reduce target by 20%, minimum 10.
        adjusted = max(10, int(target_speed * 0.8))
        if adjusted < target_speed:
            target_speed = adjusted
            reasons.append(
                f"Weather condition detected ({', '.join(weather_parts)}). "
                f"Speed reduced to {target_speed} km/h. "
                "Specific threshold requires validation and regulatory guidance."
            )

    # Motorcycle or cyclist in blind spot.
    if args.motorcycle_blind_spot:
        warnings.append(
            "VULNERABLE ROAD USER: Motorcycle or cyclist detected in blind spot. "
            "Turning acceleration restricted. Braking assist on standby."
        )
        reasons.append(
            "Motorcycle or bicycle in blind spot: turning restriction and braking assist prepared. "
            "Driver warned."
        )
        if safety_mode == "normal":
            safety_mode = "blind_spot_alert"

    # Cyclist near (general proximity, not necessarily blind spot).
    if args.cyclist_near:
        warnings.append(
            "CYCLIST PROXIMITY: Cyclist detected nearby. Maintain safe distance."
        )
        reasons.append("Cyclist detected in proximity zone.")
        if safety_mode == "normal":
            safety_mode = "vulnerable_user_alert"

    # Infrastructure warning from roadside node.
    if args.infrastructure_warning:
        warnings.append(
            "INFRASTRUCTURE NODE: Cross-traffic or hazard reported ahead. "
            "Speed reduction applied before intersection."
        )
        adjusted = max(10, int(target_speed * 0.75))
        if adjusted < target_speed:
            target_speed = adjusted
            reasons.append(
                f"Roadside infrastructure node reports cross-traffic or hazard. "
                f"Speed reduced to {target_speed} km/h as precaution."
            )
        if safety_mode == "normal":
            safety_mode = "infrastructure_alert"

    if not reasons:
        reasons.append(
            f"No governance constraints active. Target speed: {target_speed} km/h."
        )

    return target_speed, safety_mode, warnings, reasons


def main():
    print(_DISCLAIMER)
    print()

    parser = argparse.ArgumentParser(
        description=(
            "Conceptual Speed Governance and Life-Protection Control Layer simulator. "
            "NOT certified vehicle safety software."
        )
    )
    parser.add_argument(
        "--driver-speed-request",
        type=float,
        required=True,
        metavar="KMH",
        help="Speed requested by the driver in km/h.",
    )
    parser.add_argument(
        "--legal-speed-limit",
        type=float,
        default=None,
        metavar="KMH",
        help="Legal speed limit for the current road segment in km/h.",
    )
    parser.add_argument(
        "--school-zone",
        action="store_true",
        help="Vehicle is in or approaching a school zone.",
    )
    parser.add_argument(
        "--intersection-near",
        action="store_true",
        help="Vehicle is approaching an intersection.",
    )
    parser.add_argument(
        "--pedestrian-near",
        action="store_true",
        help="Pedestrian detected in proximity.",
    )
    parser.add_argument(
        "--cyclist-near",
        action="store_true",
        help="Cyclist detected in proximity.",
    )
    parser.add_argument(
        "--motorcycle-blind-spot",
        action="store_true",
        help="Motorcycle or cyclist detected in blind spot.",
    )
    parser.add_argument(
        "--visibility-ok",
        action="store_true",
        default=False,
        help="Visibility is adequate (clear conditions). Omit for reduced visibility.",
    )
    parser.add_argument(
        "--road-wet",
        action="store_true",
        help="Road surface is wet.",
    )
    parser.add_argument(
        "--rain",
        action="store_true",
        help="Rain is detected.",
    )
    parser.add_argument(
        "--infrastructure-warning",
        action="store_true",
        help="Roadside infrastructure node has reported a hazard or cross-traffic warning.",
    )
    parser.add_argument(
        "--sensor-fault",
        action="store_true",
        help="One or more sensors have reported a fault.",
    )

    args = parser.parse_args()

    target_speed, safety_mode, warnings, reasons = run_governance(args)

    print("=" * 60)
    print("SPEED GOVERNANCE OUTPUT")
    print("=" * 60)
    print(f"  Driver requested speed : {args.driver_speed_request:.1f} km/h")
    if args.legal_speed_limit is not None:
        print(f"  Legal speed limit      : {args.legal_speed_limit:.1f} km/h")
    else:
        print("  Legal speed limit      : not detected")
    print(f"  Allowed target speed   : {target_speed:.1f} km/h")
    print(f"  Safety mode            : {safety_mode}")
    print()

    if warnings:
        print("WARNINGS:")
        for w in warnings:
            print(f"  [!] {w}")
        print()

    print("REASONS:")
    for r in reasons:
        print(f"  - {r}")
    print()

    print("NOTE: All outputs are conceptual estimates for design exploration.")
    print("      Threshold values require calibration, validation, and regulatory review.")
    print("      This tool does not constitute certified vehicle safety software.")


if __name__ == "__main__":
    main()
