from __future__ import annotations

from physics import forces
from physics.environment import BallConfig, SimulationEnvironment
from physics.vector import Vector2D


class BallPhysics:
    MIN_VELOCITY_THRESHOLD = 0.1  # m/s

    def __init__(
        self,
        config: BallConfig,
        env: SimulationEnvironment,
        room_size_m: float,
        initial_velocity: Vector2D,
        initial_spin: float = 0.0,
    ) -> None:
        self.config = config
        self.env = env
        self.room_size_m = room_size_m

        self.position = Vector2D(room_size_m / 2, room_size_m / 2)
        self.velocity = initial_velocity
        self.angular_speed = initial_spin  # rad/s, scalar (2D rotation about z)

        self.total_distance = 0.0
        self.bounce_count = 0
        self.is_moving = True

    def step(self, dt: float) -> None:
        if not self.is_moving:
            return

        gravity_acc = Vector2D(0, self.env.gravity)
        drag_acc = forces.compute_drag(
            self.velocity, self.env.wind_velocity,
            self.config.radius_m, self.config.drag_coefficient,
            self.env.air_density, self.config.mass,
        )
        magnus_acc = forces.compute_magnus_effect(
            self.velocity, self.angular_speed,
            self.config.radius_m, self.env.air_density, self.config.mass,
        )

        net_acc = gravity_acc + drag_acc + magnus_acc
        self.velocity = self.velocity + (net_acc * dt)

        displacement = self.velocity * dt
        self.total_distance += displacement.magnitude()
        self.position = self.position + displacement

        self.angular_speed *= 0.99  # spin decay

        self._handle_collisions()

    def _handle_collisions(self) -> None:
        room = self.room_size_m
        r = self.config.radius_m
        e = self.config.elasticity
        f = self.config.friction

        # Bottom wall (floor)
        if self.position.y + r >= room and self.velocity.y > 0:
            self.velocity.y = -abs(self.velocity.y) * e
            self.velocity.x *= f
            self.position.y = room - r
            self.bounce_count += 1

        # Top wall (ceiling)
        if self.position.y - r <= 0 and self.velocity.y < 0:
            self.velocity.y = abs(self.velocity.y) * e
            self.velocity.x *= f
            self.position.y = r
            self.bounce_count += 1

        # Right wall
        if self.position.x + r >= room and self.velocity.x > 0:
            self.velocity.x = -abs(self.velocity.x) * e
            self.velocity.y *= f
            self.position.x = room - r
            self.bounce_count += 1

        # Left wall
        if self.position.x - r <= 0 and self.velocity.x < 0:
            self.velocity.x = abs(self.velocity.x) * e
            self.velocity.y *= f
            self.position.x = r
            self.bounce_count += 1

        # Stopping condition: near floor and slow enough
        if (
            abs(self.velocity.x) < self.MIN_VELOCITY_THRESHOLD
            and abs(self.velocity.y) < self.MIN_VELOCITY_THRESHOLD
            and self.position.y + r >= room - 0.01
        ):
            self.is_moving = False
            self.position.y = room - r
