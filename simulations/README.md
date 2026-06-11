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

All outputs in these tools are simplified estimates for validation planning. They should not be presented as proven cooling performance, guaranteed city-scale effect, or improved vehicle efficiency.
