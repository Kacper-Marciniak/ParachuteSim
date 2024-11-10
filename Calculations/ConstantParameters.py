LAPSE_RATE = 9.8e-3 # [K/m]
KELVIN_OFFSET = 273.15
MOLAR_MASS_AIR = 0.0289644 # [kg/mol]
MOLAR_MASS_VAPOUR = 0.018016 # [kg/mol]
UNIVERSAL_GAS_CONSTANT = 8.3144598 # [J/(mol·K)]
WATER_VAPOUR_GAS_CONSTANT = 461.495 # [J/(kg·K)]

COEFF_INFO = {
    "spherical": "0.62 - 0.77",
    "flat_disk": "0.75 - 0.80",
    "conical": "0.75 - 0.90",
    "biconical": "0.75 - 0.92",
    "triconical": "0.80 - 0.96",
    "annular": "0.85 - 0.95",
    "cross": "0.60 - 0.85"
}

COEFF_VALUES_DEFAULT = {
    "spherical": 0.70,
    "flat_disk": 0.75,
    "conical": 0.80,
    "biconical": 0.85,
    "triconical": 0.90,
}

AVAILABLE_CANOPY_TYPES = list(COEFF_VALUES_DEFAULT.keys())

INPUT_PARAMETERS = {
    "AIR_DENSITY": 1.3, #[kg/m3]
    "DRAG_COEFF": COEFF_VALUES_DEFAULT["spherical"], #[-]
    "G_ACCELERATION": 9.81, #[m/s**2]
    "DRAG_INTEGRAL": 0.45, # [-],
    "INFLATION_CANOPY_FILL_CONST": 5, #[-],
    "DECCELERATION_EXPONENT": 0.85, #[-],
    "OPENING_LOAD_SHOCK_FACTOR": 1.6, #[-],
    "OPENING_FORCE_REDUCTION_FACTOR": 0.9, #[-]
    "CANOPY_TYPE": "spherical"
}