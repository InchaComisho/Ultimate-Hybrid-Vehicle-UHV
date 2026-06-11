# AER-Loop Model

AER-Loop is the airflow energy recovery layer of the UHV concept. It proposes recovering limited auxiliary power from vehicle-related airflow, crosswind, natural wind while parked, braking, and rotational losses. It must not be described as perpetual motion or as a main propulsion energy source.

## Wind Power Estimate

A simplified wind power estimate is:

```text
P_wind = 1/2 × rho × A × v^3 × C_p × eta
```

Where:

* `P_wind` is recoverable wind power [W]
* `rho` is air density [kg/m^3]
* `A` is swept or intake area [m^2]
* `v` is relative wind speed [m/s]
* `C_p` is the power coefficient of the turbine or recovery device
* `eta` is generator, rectifier, wiring, and power-conversion efficiency

This equation is useful for first-order estimates only. Real systems require wind-tunnel tests, on-road measurements, aerodynamic drag assessment, and electrical efficiency measurement.

## Main Propulsion Limitation

When airflow is produced by the vehicle's own motion, extracting power from that airflow increases aerodynamic resistance or redirects energy that originated from the vehicle drivetrain. The recovered power must therefore be evaluated together with the added drag, mass, turbulence, and control losses.

For this reason, AER-Loop should be treated as an auxiliary recovery concept. It cannot supply unlimited energy, cannot replace the main drivetrain, and should not be framed as a self-charging propulsion system.

## Realistic Use Cases

Practical AER-Loop targets include:

* low-power environmental sensors
* cooling fans for external mist modules
* emergency lights
* communication modules
* auxiliary battery charging
* control electronics
* warning beacons
* natural-wind generation while parked

Parked generation is a distinct case because natural wind is not created by vehicle propulsion. Even there, output depends strongly on local wind speed, swept area, turbine design, and installation constraints.

## Evaluation Requirements

Any AER-Loop prototype should report:

* recovered electrical power
* added aerodynamic drag
* change in vehicle energy consumption
* turbine noise
* vibration
* mounting safety
* performance in crosswind and turbulent flow
* waterproofing and dust resistance

The most useful result is not peak generated power alone, but net system value after drag, reliability, maintenance, and safety are considered.
