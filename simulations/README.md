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
