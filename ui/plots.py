from __future__ import annotations

import tkinter as tk

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class PlotPanel:
    """Three stacked matplotlib subplots with optimized incremental updates."""

    def __init__(self, parent: tk.Widget) -> None:
        fig, (self.ax1, self.ax2, self.ax3) = plt.subplots(3, 1, figsize=(5, 8))
        plt.tight_layout(pad=3.0)

        self._fig = fig
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self._lines: dict[str, tuple] = {}
        self._setup_axes()

    def _setup_axes(self) -> None:
        self.ax1.set_title("Vertical Position over Time")
        self.ax1.set_xlabel("Time (s)")
        self.ax1.set_ylabel("Position (m)")
        self.ax1.invert_yaxis()

        self.ax2.set_title("Vertical Velocity over Time")
        self.ax2.set_xlabel("Time (s)")
        self.ax2.set_ylabel("Velocity (m/s)")

        self.ax3.set_title("Speed over Time")
        self.ax3.set_xlabel("Time (s)")
        self.ax3.set_ylabel("Speed (km/h)")

    def setup_lines(self, entries: list[dict]) -> None:
        """Create persistent line objects once per simulation launch.

        Each entry: {"label": str, "color": str}.
        """
        for ax in (self.ax1, self.ax2, self.ax3):
            ax.clear()
        self._setup_axes()

        self._lines.clear()
        for e in entries:
            (l1,) = self.ax1.plot([], [], label=e["label"], color=e["color"])
            (l2,) = self.ax2.plot([], [], label=e["label"], color=e["color"])
            (l3,) = self.ax3.plot([], [], label=e["label"], color=e["color"])
            self._lines[e["label"]] = (l1, l2, l3)

        self.ax1.legend()
        self.ax2.legend()
        self.ax3.legend()
        self._fig.canvas.draw()

    def update(self, ball_data: list[dict]) -> None:
        """Incrementally update line data — no cla()/re-plot per frame.

        Each dict: time, pos_y, vel_y, speed, label.
        """
        for d in ball_data:
            lines = self._lines.get(d["label"])
            if not lines:
                continue
            l1, l2, l3 = lines
            l1.set_data(d["time"], d["pos_y"])
            l2.set_data(d["time"], d["vel_y"])
            l3.set_data(d["time"], d["speed"])

        for ax in (self.ax1, self.ax2, self.ax3):
            ax.relim()
            ax.autoscale_view()

        self._fig.canvas.draw_idle()

    def clear(self) -> None:
        self._lines.clear()
        for ax in (self.ax1, self.ax2, self.ax3):
            ax.clear()
        self._setup_axes()
        self._fig.canvas.draw_idle()
