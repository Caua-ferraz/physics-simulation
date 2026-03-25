from __future__ import annotations

from dataclasses import dataclass, field

from physics.vector import Vector2D


@dataclass
class SimulationEnvironment:
    gravity: float          # m/s²
    air_density: float      # kg/m³
    wind_velocity: Vector2D = field(default_factory=lambda: Vector2D(0, 0))


@dataclass
class BallConfig:
    mass: float             # kg
    radius_m: float         # metres
    drag_coefficient: float
    elasticity: float       # coefficient of restitution
    friction: float = 0.99  # lateral friction factor applied on bounce
