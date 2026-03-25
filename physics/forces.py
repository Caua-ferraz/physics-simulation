"""Pure physics force calculations — no side-effects, no UI dependencies."""
from __future__ import annotations

import math

from physics.vector import Vector2D


def compute_drag(
    velocity: Vector2D,
    wind_velocity: Vector2D,
    radius_m: float,
    drag_coefficient: float,
    air_density: float,
    mass: float,
) -> Vector2D:
    """Unified aerodynamic drag based on velocity relative to the air medium.

    Replaces the old separate air_resistance + wind_effect which double-counted drag.
    """
    relative = velocity - wind_velocity
    speed = relative.magnitude()
    if speed == 0:
        return Vector2D(0, 0)
    area = math.pi * radius_m ** 2
    drag_magnitude = 0.5 * drag_coefficient * air_density * area * speed ** 2
    return relative.normalized() * (-drag_magnitude / mass)


def compute_magnus_effect(
    velocity: Vector2D,
    angular_speed: float,
    radius_m: float,
    air_density: float,
    mass: float,
) -> Vector2D:
    """Magnus lift force perpendicular to velocity, proportional to spin.

    angular_speed is a scalar (rad/s) — rotation about the z-axis in 2D.
    Positive spin = counter-clockwise = lift to the left of the velocity vector.
    """
    speed = velocity.magnitude()
    if angular_speed == 0 or speed == 0:
        return Vector2D(0, 0)
    lift_coefficient = 0.1
    spin_parameter = (abs(angular_speed) * radius_m) / speed
    lift_magnitude = (
        0.5 * air_density * speed ** 2
        * math.pi * radius_m ** 2
        * lift_coefficient * spin_parameter
    )
    sign = 1.0 if angular_speed > 0 else -1.0
    lift_direction = Vector2D(-velocity.y, velocity.x).normalized()
    return lift_direction * (sign * lift_magnitude / mass)


def calculate_air_density(temperature_c: float, humidity_pct: float) -> float:
    """Tetens-formula air density for given temperature (C) and relative humidity (%)."""
    pressure = 101_325        # Pa
    R_dry = 287.05            # J/(kg*K)
    temp_k = temperature_c + 273.15
    e_s = 610.78 * math.exp((17.27 * temperature_c) / (temperature_c + 237.3))
    e = (humidity_pct / 100) * e_s
    return (pressure - 0.378 * e) / (R_dry * temp_k)
