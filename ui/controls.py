from __future__ import annotations

import tkinter as tk
from typing import Callable

from constants import CELESTIAL_BODIES, MATERIALS


class ControlPanel:
    """Left-side input panel with full flexibility for simulation parameters."""

    def __init__(
        self,
        parent: tk.Widget,
        on_launch: Callable[[], None],
        on_reset: Callable[[], None],
    ) -> None:
        self._on_launch = on_launch
        self._on_reset = on_reset

        frame = tk.Frame(parent)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self._build(frame)

    def _build(self, f: tk.Frame) -> None:
        r = 0

        def label(text: str) -> None:
            nonlocal r
            tk.Label(f, text=text).grid(row=r, column=0, padx=5, pady=3, sticky="w")

        def entry(var: tk.Variable, width: int = 10) -> None:
            tk.Entry(f, textvariable=var, width=width).grid(row=r, column=1, padx=5, pady=3, sticky="ew")

        # -- Ball properties --
        tk.Label(f, text="Ball Properties", font=("Arial", 9, "bold")).grid(
            row=r, column=0, columnspan=2, pady=(0, 2), sticky="w",
        )
        r += 1

        label("Material:")
        self.material_var = tk.StringVar(value="Rubber")
        tk.OptionMenu(f, self.material_var, *MATERIALS, command=self._on_material_change).grid(
            row=r, column=1, padx=5, pady=3, sticky="ew",
        )
        r += 1

        label("Elasticity (0-1):")
        self.elasticity_var = tk.DoubleVar(value=MATERIALS["Rubber"])
        entry(self.elasticity_var)
        r += 1

        label("Mass (kg):")
        self.mass_var = tk.DoubleVar(value=1.0)
        entry(self.mass_var)
        r += 1

        label("Ball Size (cm):")
        self.ball_size_var = tk.DoubleVar(value=5.0)
        entry(self.ball_size_var)
        r += 1

        label("Drag Coefficient:")
        self.drag_var = tk.DoubleVar(value=0.47)
        entry(self.drag_var)
        r += 1

        label("Spin (rad/s):")
        self.spin_var = tk.DoubleVar(value=0.0)
        entry(self.spin_var)
        r += 1

        # -- Launch --
        tk.Label(f, text="Launch", font=("Arial", 9, "bold")).grid(
            row=r, column=0, columnspan=2, pady=(8, 2), sticky="w",
        )
        r += 1

        label("Force (N):")
        self.force_var = tk.DoubleVar(value=10.0)
        entry(self.force_var)
        r += 1

        label("Angle (deg):")
        self.angle_var = tk.DoubleVar(value=90.0)
        entry(self.angle_var)
        r += 1

        # -- Environment --
        tk.Label(f, text="Environment", font=("Arial", 9, "bold")).grid(
            row=r, column=0, columnspan=2, pady=(8, 2), sticky="w",
        )
        r += 1

        label("Room Size (m):")
        self.room_size_var = tk.DoubleVar(value=10.0)
        entry(self.room_size_var)
        r += 1

        label("Wind Speed (m/s):")
        self.wind_speed_var = tk.DoubleVar(value=0.0)
        entry(self.wind_speed_var)
        r += 1

        label("Wind Angle (deg):")
        self.wind_angle_var = tk.DoubleVar(value=0.0)
        entry(self.wind_angle_var)
        r += 1

        label("Temperature (C):")
        self.temperature_var = tk.DoubleVar(value=20.0)
        entry(self.temperature_var)
        r += 1

        label("Humidity (%):")
        self.humidity_var = tk.DoubleVar(value=50.0)
        entry(self.humidity_var)
        r += 1

        # -- Planet selection --
        tk.Label(f, text="Compare Planets", font=("Arial", 9, "bold")).grid(
            row=r, column=0, columnspan=2, pady=(8, 2), sticky="w",
        )
        r += 1

        self.planet_vars: dict[str, tk.BooleanVar] = {}
        for name in CELESTIAL_BODIES:
            var = tk.BooleanVar(value=(name in ("Earth", "Moon", "Mars")))
            self.planet_vars[name] = var
            tk.Checkbutton(f, text=name, variable=var).grid(
                row=r, column=0, columnspan=2, padx=5, sticky="w",
            )
            r += 1

        # -- Buttons --
        btn_frame = tk.Frame(f)
        btn_frame.grid(row=r, column=0, columnspan=2, pady=10)
        tk.Button(btn_frame, text="Throw Ball", command=self._on_launch).pack(side=tk.LEFT, padx=4)
        tk.Button(btn_frame, text="Reset", command=self._on_reset).pack(side=tk.LEFT, padx=4)

    def _on_material_change(self, selection: str) -> None:
        if selection in MATERIALS:
            self.elasticity_var.set(MATERIALS[selection])

    def get_params(self) -> dict:
        return {
            "elasticity": self.elasticity_var.get(),
            "initial_force": self.force_var.get(),
            "launch_angle": self.angle_var.get(),
            "room_size": self.room_size_var.get(),
            "ball_size_cm": self.ball_size_var.get(),
            "mass": self.mass_var.get(),
            "drag_coefficient": self.drag_var.get(),
            "spin": self.spin_var.get(),
            "wind_speed": self.wind_speed_var.get(),
            "wind_angle": self.wind_angle_var.get(),
            "temperature": self.temperature_var.get(),
            "humidity": self.humidity_var.get(),
            "selected_planets": [
                name for name, var in self.planet_vars.items() if var.get()
            ],
        }
