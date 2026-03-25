from __future__ import annotations

import math
import tkinter as tk
from dataclasses import dataclass
from tkinter import messagebox

from constants import CELESTIAL_BODIES
from physics.ball_physics import BallPhysics
from physics.environment import BallConfig, SimulationEnvironment
from physics.forces import calculate_air_density
from physics.vector import Vector2D
from simulation.data_recorder import DataRecorder
from ui.ball_renderer import BallRenderer
from ui.plots import PlotPanel

PLOT_UPDATE_EVERY = 5  # redraw plots every N frames (not every tick)


@dataclass
class _BallEntry:
    name: str
    color: str
    ball: BallPhysics
    renderer: BallRenderer
    recorder: DataRecorder


class SimulationEngine:
    TIME_STEP = 0.02  # seconds (50 fps)

    def __init__(
        self,
        root: tk.Tk,
        canvas: tk.Canvas,
        canvas_width: int,
        canvas_height: int,
        plot_panel: PlotPanel,
    ) -> None:
        self._root = root
        self._canvas = canvas
        self._canvas_width = canvas_width
        self._canvas_height = canvas_height
        self._plot_panel = plot_panel
        self._entries: list[_BallEntry] = []
        self._running = False
        self._time_elapsed = 0.0
        self._after_id: str | None = None
        self._frame_count = 0

    @property
    def is_running(self) -> bool:
        return self._running

    def launch(self, params: dict) -> None:
        if self._running:
            messagebox.showinfo("Simulation Running", "The simulation is already running.")
            return

        try:
            mass = params["mass"]
            ball_size_cm = params["ball_size_cm"]
            room_size = params["room_size"]
            selected = params["selected_planets"]

            if mass <= 0 or ball_size_cm <= 0 or room_size <= 0:
                messagebox.showerror("Invalid Input", "Mass, Ball Size, and Room Size must be positive.")
                return
            if not selected:
                messagebox.showerror("Invalid Input", "Select at least one planet.")
                return

            air_density_base = calculate_air_density(params["temperature"], params["humidity"])
            wind_velocity = _angle_to_vector(params["wind_angle"], params["wind_speed"])
            launch_dir = _angle_to_vector(params["launch_angle"], 1.0)
            scale = min(self._canvas_width / room_size, self._canvas_height / room_size)
            radius_m = ball_size_cm / 100

            self._clear()

            line_entries: list[dict] = []
            for name in selected:
                body = CELESTIAL_BODIES[name]
                env = SimulationEnvironment(
                    gravity=body["gravity"],
                    air_density=body["air_density"] if body["air_density"] > 0 else air_density_base * 0,
                    wind_velocity=wind_velocity,
                )
                config = BallConfig(
                    mass=mass,
                    radius_m=radius_m,
                    drag_coefficient=params["drag_coefficient"],
                    elasticity=params["elasticity"],
                )
                initial_velocity = launch_dir * (params["initial_force"] / mass)
                ball = BallPhysics(config, env, room_size, initial_velocity, params["spin"])
                renderer = BallRenderer(self._canvas, ball, body["color"], scale)
                entry = _BallEntry(name, body["color"], ball, renderer, DataRecorder())
                self._entries.append(entry)
                line_entries.append({"label": name, "color": body["color"]})

            self._plot_panel.setup_lines(line_entries)

            self._running = True
            self._time_elapsed = 0.0
            self._frame_count = 0
            self._tick()

        except Exception as exc:
            messagebox.showerror("Error", f"An error occurred: {exc}")

    def stop(self) -> None:
        if self._after_id is not None:
            self._root.after_cancel(self._after_id)
            self._after_id = None
        self._running = False

    def reset(self) -> None:
        self.stop()
        self._clear()
        self._canvas.delete("results")
        self._plot_panel.clear()

    def _tick(self) -> None:
        if not self._running:
            return

        all_stopped = True
        for entry in self._entries:
            if entry.ball.is_moving:
                entry.ball.step(self.TIME_STEP)
                entry.renderer.sync()
                entry.recorder.record(
                    self._time_elapsed,
                    entry.ball.position.y,
                    entry.ball.velocity.y,
                    entry.ball.velocity.magnitude(),
                )
                all_stopped = False

        self._frame_count += 1
        if self._frame_count % PLOT_UPDATE_EVERY == 0 or all_stopped:
            self._update_plots()

        self._time_elapsed += self.TIME_STEP

        if all_stopped:
            self._running = False
            self._after_id = None
            self._display_results()
        else:
            self._after_id = self._root.after(int(self.TIME_STEP * 1000), self._tick)

    def _update_plots(self) -> None:
        self._plot_panel.update([
            {
                "time": e.recorder.time_steps,
                "pos_y": e.recorder.positions_y,
                "vel_y": e.recorder.velocities_y,
                "speed": e.recorder.speeds,
                "label": e.name,
            }
            for e in self._entries
        ])

    def _display_results(self) -> None:
        y_pos = self._canvas_height / 2 - 20
        for entry in self._entries:
            text = (
                f"{entry.name}: Stopped after {entry.ball.bounce_count} bounces, "
                f"Distance: {entry.ball.total_distance:.2f} m"
            )
            self._canvas.create_text(
                self._canvas_width / 2, y_pos,
                text=text, fill=entry.color, font=("Arial", 12), tags="results",
            )
            y_pos += 20

    def _clear(self) -> None:
        for entry in self._entries:
            entry.renderer.remove()
        self._entries.clear()
        self._canvas.delete("results")


def _angle_to_vector(angle_deg: float, magnitude: float) -> Vector2D:
    """Convert angle in degrees to a Vector2D.

    Convention: 0=right, 90=up, 180=left, 270=down.
    Physics uses Y-down, so 90 degrees (up) maps to -Y.
    """
    rad = math.radians(angle_deg)
    return Vector2D(math.cos(rad) * magnitude, -math.sin(rad) * magnitude)
