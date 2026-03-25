MATERIALS: dict[str, float] = {
    "Rubber": 0.85,
    "Tennis Ball": 0.75,
    "Glass": 0.65,
    "Metal": 0.6,
    "Wood": 0.5,
    "Soft Plastic": 0.4,
    "Clay": 0.2,
}

CELESTIAL_BODIES: dict[str, dict] = {
    "Earth":   {"gravity": 9.81,  "air_density": 1.225, "color": "#2e8b57"},
    "Moon":    {"gravity": 1.62,  "air_density": 0.0,   "color": "#4682b4"},
    "Mars":    {"gravity": 3.71,  "air_density": 0.020, "color": "#cd5c5c"},
    "Venus":   {"gravity": 8.87,  "air_density": 65.0,  "color": "#ff8c00"},
    "Jupiter": {"gravity": 24.79, "air_density": 0.16,  "color": "#8b6914"},
}
