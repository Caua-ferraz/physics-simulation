# Contributing

Thanks for your interest in contributing to this project.

## Getting Started

1. Fork the repository and clone it locally.
2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Run the app to confirm everything works:
   ```bash
   python main.py
   ```

## How to Contribute

### Reporting Bugs
Open an issue with:
- A clear title and description
- Steps to reproduce
- Expected vs actual behavior
- Python version and OS

### Suggesting Features
Open an issue tagged `enhancement`. Describe the use case, not just the feature.

### Submitting a Pull Request

1. Create a branch from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```
2. Make focused, minimal changes — one concern per PR.
3. Test manually: launch the simulation, throw a ball, verify plots update correctly.
4. Write a clear commit message (see format below).
5. Open a PR against `main` with a description of what changed and why.

## Commit Message Format

```
Short summary (max 72 chars)

- Bullet points for each meaningful change
- Focus on *why*, not just *what*
```

## Code Style

- Python 3.10+, type hints on all public functions.
- No UI references inside `physics/` — keep it pure.
- Prefer `dataclasses` for config/state objects.
- Keep functions small and single-purpose.

## Project Structure

```
physics/       Pure physics logic (no tkinter)
simulation/    Engine and data recording
ui/            Tkinter canvas, controls, plots
constants.py   Shared lookup tables
main.py        Entry point and layout
```
