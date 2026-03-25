# Ball Launch Physics Simulation

A 2D physics simulator that launches a ball inside a bounded room and compares its trajectory across multiple celestial environments simultaneously. Built with Python, Tkinter, and Matplotlib.

---

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Installation](#installation)
- [Running the Simulation](#running-the-simulation)
- [User Interface](#user-interface)
- [Physics Model](#physics-model)
- [Graphs](#graphs)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [Security](#security)
- [License](#license)

---

## Features

- Simultaneous multi-planet comparison (Earth, Moon, Mars, Venus, Jupiter)
- Free-angle launch direction (0–360°) and wind direction
- Magnus effect via configurable spin (rad/s)
- Realistic air density from temperature and humidity (Tetens formula)
- Real-time plots: vertical position, vertical velocity, and speed
- Reset without restarting the application
- Modular architecture — physics engine has zero UI dependencies

---

## Project Structure

```
physics-simulation/
├── main.py                  Entry point and layout
├── constants.py             Celestial bodies and material presets
├── requirements.txt
├── physics/
│   ├── vector.py            Vector2D class
│   ├── environment.py       SimulationEnvironment, BallConfig dataclasses
│   ├── forces.py            Pure force functions (drag, Magnus, air density)
│   └── ball_physics.py      BallPhysics state machine
├── simulation/
│   ├── engine.py            Game loop, orchestration
│   └── data_recorder.py     Per-frame telemetry accumulator
└── ui/
    ├── ball_renderer.py     Tkinter oval sync
    ├── controls.py          Input panel
    └── plots.py             Matplotlib subplot panel
```

---

## Requirements

- Python 3.10+
- `matplotlib >= 3.9`
- `numpy >= 2.1`
- `tkinter` (included with standard Python on Windows and macOS; see [Troubleshooting](#troubleshooting) for Linux)

---

## Installation

```bash
# 1. Clone the repository
git clone https://github.com/Caua-ferraz/physics-simulation.git
cd physics-simulation

# 2. Create and activate a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

---

## Running the Simulation

```bash
python main.py
```

---

## User Interface

The window is split into two columns:

- **Left** — control panel for all simulation parameters
- **Right** — simulation canvas (top) and real-time plots (bottom)

### Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| Material | Preset elasticity (overridable) | Rubber |
| Elasticity | Coefficient of restitution (0–1) | 0.85 |
| Mass (kg) | Ball mass | 1.0 |
| Ball Size (cm) | Ball radius | 5.0 |
| Drag Coefficient | Aerodynamic drag (sphere ≈ 0.47) | 0.47 |
| Spin (rad/s) | Initial angular speed — enables Magnus effect | 0.0 |
| Force (N) | Launch impulse magnitude | 10.0 |
| Angle (deg) | Launch direction: 0=right, 90=up, 180=left, 270=down | 90 |
| Room Size (m) | Square room side length | 10.0 |
| Wind Speed (m/s) | Wind magnitude | 0.0 |
| Wind Angle (deg) | Wind direction (same convention as launch angle) | 0 |
| Temperature (°C) | Used to calculate air density | 20 |
| Humidity (%) | Used to calculate air density | 50 |
| Planet checkboxes | Select which environments to compare | Earth, Moon, Mars |

### Buttons

- **Throw Ball** — launches a new simulation with current parameters
- **Reset** — clears canvas and plots, ready for a new run

---

## Physics Model

All calculations use SI units. The physics layer (`physics/`) has no Tkinter dependencies and can be used or tested independently.

### Coordinate system

Physics uses Y-down convention (gravity is positive Y). The canvas maps directly — no inversion. The floor is at `y = room_size`, the ceiling at `y = 0`.

### Forces applied each time step

**1. Gravity**

```
a_gravity = (0, g)
```

`g` is taken from the selected celestial body (e.g. Earth: 9.81 m/s²).

**2. Aerodynamic drag** (unified — replaces old separate air resistance + wind)

```
F_drag = -0.5 * Cd * rho * A * |v_rel|^2 * v_rel_hat
a_drag = F_drag / m
```

Where `v_rel = v_ball - v_wind`. Using relative velocity to the air medium correctly handles both still-air drag and wind in a single expression.

**3. Magnus effect**

```
F_magnus = 0.5 * rho * |v|^2 * A * Cl * spin_param * lift_direction
spin_param = (|omega| * r) / |v|
lift_direction = perpendicular to velocity
```

Only active when spin ≠ 0. Positive spin curves the ball left relative to its velocity direction.

**4. Collisions**

All four walls reflect the velocity component normal to the wall, scaled by the elasticity coefficient. The tangential component is scaled by the friction factor (0.99). The ball stops when its speed falls below 0.1 m/s and it is resting on the floor.

### Air density

Calculated from temperature and humidity using the Tetens saturation vapour pressure formula:

```
rho = (P - 0.378 * e) / (R_dry * T_kelvin)
```

Celestial bodies with defined atmospheres (Moon: 0 kg/m³, Mars: 0.020 kg/m³) override the calculated value.

### Celestial bodies

| Body | Gravity (m/s²) | Air Density (kg/m³) |
|------|---------------|----------------------|
| Earth | 9.81 | 1.225 (from T/H input) |
| Moon | 1.62 | 0.0 |
| Mars | 3.71 | 0.020 |
| Venus | 8.87 | 65.0 |
| Jupiter | 24.79 | 0.16 |

---

## Graphs

Three real-time plots update at ~10 Hz during the simulation:

- **Vertical Position vs Time** — Y-axis inverted so falling appears downward
- **Vertical Velocity vs Time** — positive = downward
- **Speed vs Time** — total speed in km/h

Each selected planet is shown as a separate coloured line.

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `ModuleNotFoundError: tkinter` (Linux) | `sudo apt install python3-tk` |
| Simulation doesn't start | Ensure mass, ball size, and room size are all positive |
| No planets selected | Check at least one planet checkbox before throwing |
| Plots not visible | Resize the window — plots occupy the lower-right panel |
| Ball settles very slowly | Reduce elasticity or increase drag coefficient |

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for setup instructions, coding conventions, and the PR workflow.

---

## Security

See [SECURITY.md](SECURITY.md) for how to report vulnerabilities privately.

---

## License

MIT — see [LICENSE](LICENSE).
