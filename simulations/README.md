# Simulations

This directory contains simple Python 3 estimators for early UHV concept exploration. They use no external dependencies and are intended for first-order calculations only. Prototype and field measurements are required before making engineering claims.

## Evaporative Cooling Estimator

`evaporative_cooling_estimator.py` estimates cooling power from water flow and evaporation efficiency:

```text
Q_evap = m_dot × L_v × eta_evap
```

Example:

```bash
python evaporative_cooling_estimator.py --water-flow 10 --efficiency 0.7
```

Units:

* `--water-flow`: liters per hour
* `--efficiency`: evaporation efficiency from 0 to 1
* output: watts and kilowatts

## Wind Recovery Estimator

`wind_recovery_estimator.py` estimates auxiliary wind recovery power:

```text
P = 0.5 * rho * A * v^3 * Cp * eta
```

Example:

```bash
python wind_recovery_estimator.py --area 0.1 --speed 20 --cp 0.25 --efficiency 0.7
```

Units:

* `--area`: swept or intake area in square meters
* `--speed`: wind speed in meters per second
* `--cp`: power coefficient
* `--efficiency`: generator and conversion efficiency from 0 to 1
* output: watts and kilowatts

For vehicle-generated airflow, recovered power must be evaluated together with increased aerodynamic drag. This is not a main propulsion energy source.

## Representative Case Estimator

`representative_case_estimator.py` combines simplified cooling and water-use estimates for representative validation scenarios such as dry desert roads, urban bus routes, airport or port service vehicles, humid climate limits, and night or low-wind limits.

Example:

```bash
python representative_case_estimator.py --case dry_desert_road --vehicles 1 --water-flow 10 --hours 1 --efficiency 0.7
```

Units:

* `--vehicles`: vehicle count
* `--water-flow`: liters per vehicle per hour
* `--hours`: operation hours
* `--efficiency`: representative evaporation efficiency from 0 to 1
* output: conceptual cooling power and water use

## Droplet Evaporation Time Estimator

`droplet_evaporation_time_estimator.py` provides a heuristic screening estimate for droplet evaporation time. It is not a validated droplet-physics model.

Example:

```bash
python droplet_evaporation_time_estimator.py --diameter 20 --temperature 40 --humidity 20 --wind-speed 3
```

Units:

* `--diameter`: droplet diameter in micrometers
* `--temperature`: ambient temperature in degrees Celsius
* `--humidity`: relative humidity in percent
* `--wind-speed`: local wind or airflow speed in meters per second
* output: estimated evaporation time in seconds

## Water Use Scenario

`water_use_scenario.py` estimates daily and seasonal water demand for a vehicle or fleet.

Example:

```bash
python water_use_scenario.py --vehicles 20 --water-flow 8 --hours 6 --days 90
```

Units:

* `--vehicles`: vehicle count
* `--water-flow`: liters per vehicle per hour
* `--hours`: operation hours per day
* `--days`: operating days
* output: liters per day and liters over the selected period

## Speed-Energy Profile

`speed_energy_profile.py` compares theoretical Center-Mist latent cooling potential with auxiliary AER-Loop wind recovery power across a vehicle speed range. The cooling value is a latent heat potential, not validated effective cooling. The AER-Loop value is auxiliary only and must be evaluated together with aerodynamic drag.

Example:

```bash
python speed_energy_profile.py --mist-l-min 0.5 --evap-efficiency 0.7 --speed-min 20 --speed-max 80 --speed-step 10
```

CSV example:

```bash
python speed_energy_profile.py --mist-l-min 0.5 --evap-efficiency 0.7 --csv speed_profile.csv
```

Users may plot the CSV output with external tools such as Python/matplotlib, spreadsheets, or gnuplot. The repository script itself remains standard-library only.

## Parking Auxiliary Energy Balance

`parking_auxiliary_energy_balance.py` estimates a simplified daily auxiliary energy balance from protected solar skin input, parked natural-wind auxiliary generation, and standby loads. It is not a validated vehicle charging model and does not imply main traction battery charging.

Example:

```bash
python parking_auxiliary_energy_balance.py --solar-area 2.0 --solar-efficiency 0.12 --solar-hours 5 --solar-irradiance 800 --wind-area 0.05 --wind-speed 4 --cp 0.15 --conversion-efficiency 0.7 --operation-hours 24 --standby-load-w 5
```

Units:

* `--solar-area`: protected solar area in square meters
* `--solar-irradiance`: representative solar irradiance in W/m^2
* `--solar-efficiency`: representative protected-module conversion efficiency
* `--solar-hours`: equivalent sun hours per day
* `--wind-area`: vertical-axis rotor or intake area in square meters
* `--wind-speed`: average natural wind speed in m/s
* `--cp`: wind power coefficient
* `--conversion-efficiency`: generator and charge conversion efficiency
* `--operation-hours`: hours per day for wind generation and standby load
* `--standby-load-w`: auxiliary standby load in watts
* output: Wh/day generation, load, and surplus or deficit

## UHV Control State Machine

`uhv_control_state_machine.py` evaluates a simplified conceptual control state for speed-adaptive mist permission, parking shield behavior, and fail-safe shutoff conditions. It is not certified vehicle safety software.

Example:

```bash
python uhv_control_state_machine.py --speed-kmh 30 --temperature-c 38 --humidity 35 --visibility-ok --water-quality-ok --battery-soc 80
```

Inputs include speed, temperature, humidity, visibility, road wetness, pedestrian proximity, water quality, battery state, rain, and fault flags. Output includes selected mode, mist permission, and reason list.

## Speed Governance Controller

`speed_governance_controller.py` evaluates a conceptual speed governance and life-protection control layer. It is not certified vehicle safety software.

Example — legal speed limit with pedestrian and intersection:

```bash
python speed_governance_controller.py --driver-speed-request 80 --legal-speed-limit 40 --intersection-near --pedestrian-near
```

Example — weather-adjusted safe speed:

```bash
python speed_governance_controller.py --driver-speed-request 60 --legal-speed-limit 60 --road-wet --rain
```

Example — motorcycle blind spot:

```bash
python speed_governance_controller.py --driver-speed-request 50 --legal-speed-limit 50 --motorcycle-blind-spot
```

Inputs include driver speed request, legal speed limit, school zone, intersection proximity, pedestrian proximity, cyclist proximity, motorcycle blind spot, visibility, road wetness, rain, infrastructure warning, and sensor fault flags. Output includes allowed target speed, safety mode, warning list, and reason list.

All outputs in these tools are simplified estimates for validation planning. They should not be presented as proven cooling performance, guaranteed city-scale effect, or improved vehicle efficiency.

## Mobile Mist Cooling Simulator

`mobile_mist_cooling_simulator.py` provides an illustrative estimate of local cooling potential when ultrasonic-mist-equipped mobility units operate across roads or urban corridors.

It is not a CFD model and not a certified thermal forecast.
All outputs are assumption-based estimates for conceptual comparison only.
Field testing is required before making any engineering claims.

Example:

```bash
python simulations/mobile_mist_cooling_simulator.py --vehicles 100 --mist-output-lph 5 --operating-hours 8 --ambient-temp-c 40 --relative-humidity 25
```

Optional output flags: `--output-markdown`, `--output-csv`, `--output-summary-json`

Key inputs: `--vehicles`, `--mist-output-lph`, `--operating-hours`, `--ambient-temp-c`, `--relative-humidity`, `--wind-speed-ms`, `--road-corridor-width-m`, `--mixing-height-m`, `--evaporation-efficiency`, `--coverage-efficiency`, `--heat-loss-factor`, `--max-temp-drop-c`

## Maintenance assumptions

Mobile mist cooling simulations assume the system is operating normally.

In real deployment, cooling output and water use depend on maintenance intervals, tank hygiene, filter condition, clogging risk, and water quality.

See:

- [Center-Mist Maintenance Schedule](../docs/center_mist_maintenance_schedule.md)

---

## Tank Hygiene and Gravity-Fed Recovery

Mobile mist cooling simulations assume that the mist system is functioning normally. In real deployment, cooling output depends on tank hygiene, filter condition, water quality, clogging risk, and maintenance intervals.

Gravity-fed micro hydropower recovery is a small auxiliary recovery concept and should not be modeled as net energy generation.

For details on tank hygiene and recovery design, see [docs/center_mist_tank_hygiene_and_recovery.md](../docs/center_mist_tank_hygiene_and_recovery.md).

## Mobile Mist Cooling Graph Generator

`generate_mobile_mist_cooling_graphs.py` generates illustrative comparison graphs for four representative scenarios:

1. Dry climate direct tank refill
2. Rainy climate dual supply
3. High humidity low evaporation
4. Dusty desert maintenance-limited

Requires matplotlib. Outputs to `images/`.

Example:

```bash
python simulations/generate_mobile_mist_cooling_graphs.py
```

---

## Author

Master / inchacomusho / InchaComisho

An independent Japanese concept designer, observer, proposer, AI tuner, and definer of Artificial Wisdom.  
Founder and advocate of the academic framework of Natural Complementary Science.  
Publicly active in natural-law philosophy, planetary circulation restoration, and co-creation with AI.

---

## License

CC BY 4.0

This article is released under the Creative Commons Attribution 4.0 International License (CC BY 4.0).  
Sharing, redistribution, translation, adaptation, and reuse are permitted as long as proper attribution is given.
