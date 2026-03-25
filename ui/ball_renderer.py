from __future__ import annotations

import tkinter as tk

from physics.ball_physics import BallPhysics


class BallRenderer:
    """Owns a single Tkinter oval and keeps it in sync with a BallPhysics instance."""

    def __init__(
        self,
        canvas: tk.Canvas,
        ball: BallPhysics,
        color: str,
        scale: float,
    ) -> None:
        self._canvas = canvas
        self._ball = ball
        self._scale = scale
        self.color = color
        self._radius_px = ball.config.radius_m * scale

        cx, cy = self._to_canvas(ball.position.x, ball.position.y)
        r = self._radius_px
        self._oval_id = canvas.create_oval(
            cx - r, cy - r, cx + r, cy + r, fill=color,
        )

    def sync(self) -> None:
        cx, cy = self._to_canvas(self._ball.position.x, self._ball.position.y)
        r = self._radius_px
        self._canvas.coords(self._oval_id, cx - r, cy - r, cx + r, cy + r)

    def remove(self) -> None:
        self._canvas.delete(self._oval_id)

    def _to_canvas(self, x_m: float, y_m: float) -> tuple[float, float]:
        # Physics Y-down matches canvas Y-down — no inversion needed.
        return x_m * self._scale, y_m * self._scale
