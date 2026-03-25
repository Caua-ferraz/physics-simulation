from __future__ import annotations


class DataRecorder:
    """Accumulates per-frame telemetry for a single ball."""

    def __init__(self) -> None:
        self.time_steps: list[float] = []
        self.positions_y: list[float] = []
        self.velocities_y: list[float] = []
        self.speeds: list[float] = []  # km/h

    def record(self, t: float, pos_y: float, vel_y: float, speed_ms: float) -> None:
        self.time_steps.append(t)
        self.positions_y.append(pos_y)
        self.velocities_y.append(vel_y)
        self.speeds.append(speed_ms * 3.6)

    def clear(self) -> None:
        self.time_steps.clear()
        self.positions_y.clear()
        self.velocities_y.clear()
        self.speeds.clear()
