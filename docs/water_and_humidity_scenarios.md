# Water and Humidity Scenarios

Water use is one of the central constraints for UHV Center-Mist Cooling. This document provides representative scenario calculations for vehicle water demand, fleet water demand, humidity risk, and water-resource tradeoffs. These are conceptual estimates only and require field validation.

## Water Use Per Vehicle

Water use can be estimated as:

```text
vehicle_water_l = water_flow_l_per_hour × operation_hours
```

Representative examples:

| Water flow | Operation time | Water per vehicle |
|---|---:|---:|
| 5 L/h | 4 h | 20 L |
| 8 L/h | 6 h | 48 L |
| 10 L/h | 8 h | 80 L |
| 12 L/h | 8 h | 96 L |

These values are package and logistics estimates. They do not prove cooling performance.

## Water Use Per Fleet

Fleet water use can be estimated as:

```text
fleet_water_l = vehicle_count × water_flow_l_per_hour × operation_hours
```

Representative examples:

| Fleet | Water flow | Operation time | Daily water use |
|---|---:|---:|---:|
| 10 service vehicles | 8 L/h | 6 h | 480 L/day |
| 20 buses | 8 L/h | 6 h | 960 L/day |
| 50 taxis | 5 L/h | 8 h | 2000 L/day |
| 100 fleet vehicles | 6 L/h | 8 h | 4800 L/day |

City-scale deployment should not be assumed practical unless water supply, refill logistics, hygiene, public safety, and measured cooling benefit justify the cost.

## Daily and Seasonal Demand

Seasonal water demand can be estimated by multiplying daily use by the number of operating days:

```text
seasonal_water_l = daily_water_l × operating_days
```

For example, a 20-bus pilot using `960 L/day` for `90 hot-season days` would require:

```text
960 × 90 = 86,400 L
```

This may be acceptable in one region and unacceptable in another. Local water scarcity, water pricing, and infrastructure constraints must be evaluated.

## Dry Climate Advantages

Dry climates can increase evaporation potential because the air has more capacity to accept water vapor. This may allow more of the sprayed water to evaporate before it reaches the ground.

Potential advantages include:

* higher evaporation fraction
* lower road-wetting risk at the same water flow
* stronger cooling per liter under favorable airflow
* clearer validation of mist behavior in open-air tests

These advantages are conditional and must be measured.

## Humid Climate Limitations

Humid air slows evaporation. In humid climates, the same water flow may produce less cooling and more liquid deposition. UHV operation may need to reduce mist, rely more on airflow, or disable external mist.

Validation should track:

* relative humidity before and after operation
* road and sidewalk wetness
* visibility
* perceived dampness near pedestrians
* droplet deposition on vehicle surfaces

## Night-Time and Low-Wind Risks

At night or in low-wind conditions, air mixing can be weak. Mist may linger or accumulate humidity near the vehicle, especially in enclosed stops, depots, parking areas, tunnels, or canopied sidewalks.

Candidate controls include:

* lower water flow at low wind speed
* automatic shutoff above a humidity threshold
* road wetness sensors
* visibility sensors
* geofenced low-output zones
* higher fan airflow without added mist

## Water Quality and Tank Hygiene

Vehicle-mounted tanks require sanitation and maintenance. Stagnant water can support biofilm, mold, or microbial growth. Any public deployment must address:

* cleanable tank design
* filtration
* drain cycles
* inspection intervals
* pump and nozzle cleaning
* water quality records
* prevention of aerosolized contamination

Early tests should use clean water and avoid additives unless approved by safety and environmental reviewers.

## Recycled, Treated, or Non-Potable Water

Recycled, treated, or non-potable water could reduce freshwater demand where regulations allow. However, using non-potable water may increase filtration, corrosion, odor, mineral-deposit, and microbial-safety requirements.

Any such use should be evaluated under local rules for:

* public exposure
* aerosol generation
* worker safety
* vehicle maintenance
* water storage
* discharge or runoff

## Cooling Benefit Versus Water-Resource Cost

The practical question is not simply whether mist cooling can produce a cooling effect. The question is whether the measured benefit justifies water use, maintenance, vehicle complexity, and safety controls.

Useful comparison metrics include:

* cooling watts per liter per hour
* liters per vehicle-hour
* liters per route-kilometer
* road-temperature change per liter
* pedestrian-zone temperature change per liter
* humidity increase per liter
* maintenance cost per operating hour

UHV should be advanced only where measured local cooling and human-comfort benefits outweigh water-resource and safety costs.
