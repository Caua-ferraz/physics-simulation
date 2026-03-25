import tkinter as tk
from tkinter import messagebox

from simulation.engine import SimulationEngine
from ui.controls import ControlPanel
from ui.plots import PlotPanel

CANVAS_WIDTH = 600
CANVAS_HEIGHT = 400


def main() -> None:
    root = tk.Tk()
    root.title("Ball Launch Physics Simulation")
    root.geometry("1280x750")
    root.minsize(950, 650)

    # Two-column grid: [controls | canvas + plots]
    root.columnconfigure(0, weight=0)
    root.columnconfigure(1, weight=1)
    root.rowconfigure(0, weight=1)

    left_frame = tk.Frame(root)
    left_frame.grid(row=0, column=0, sticky="ns", padx=(10, 0), pady=10)

    right_frame = tk.Frame(root)
    right_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
    right_frame.rowconfigure(0, weight=0)
    right_frame.rowconfigure(1, weight=1)
    right_frame.columnconfigure(0, weight=1)

    canvas = tk.Canvas(right_frame, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg="white")
    canvas.grid(row=0, column=0, sticky="ew")

    plot_frame = tk.Frame(right_frame)
    plot_frame.grid(row=1, column=0, sticky="nsew")
    plot_panel = PlotPanel(plot_frame)

    engine = SimulationEngine(root, canvas, CANVAS_WIDTH, CANVAS_HEIGHT, plot_panel)

    def on_launch() -> None:
        engine.launch(controls.get_params())

    def on_reset() -> None:
        engine.reset()

    controls = ControlPanel(left_frame, on_launch, on_reset)

    def on_closing() -> None:
        if engine.is_running:
            if messagebox.askokcancel("Quit", "Simulation is running. Do you want to quit?"):
                engine.stop()
                root.destroy()
        else:
            root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()
