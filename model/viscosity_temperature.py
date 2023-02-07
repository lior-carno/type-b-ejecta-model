from constants.simulation_constants import PARTICLE_RADIUS, TIME_GRID
from math import sin, cos, tan, e
from scipy.optimize import fsolve
from constants.initial_conditions_constants import INITIAL_TEMPERATURE, EXTERNAL_TEMPERATURE

# PHYSICAL CONSTANTS:
k = 1.5  # Particle conductivity
c = 1096  # Particle heat capacity
p = 2400  # Particle Density
a = k / (p * c)
Pr = 0.71  # Ambient air Prandtl number
n_g = 1.71 * 10 ** -5  # Viscosity of ambient air
k_g = 0.0260  # Conductivity of ambient air
v_c = 360  # Velocity of particle (same as shockwave)
v_g = 1.6  # Velocity of air (wind speed)

# Reynolds number
Re = (2 * abs(v_g - v_c) * PARTICLE_RADIUS * 1.225) / n_g
# Nusselt number
x = (p * (2.2 * 10 ** -4)) + 0.31
Nu = 2 + x * (Re ** 0.5) * (Pr ** (1 / 3))
# Heat transfer coefficient
h = (Nu * k_g) / (2 * PARTICLE_RADIUS)
# Biot number
B = (h * PARTICLE_RADIUS) / k


def dimensionless_pos(position: float) -> float:
    """Returns dimensionless position with relation to particle radius."""
    return position / PARTICLE_RADIUS


def dimensionless_time(time: float) -> float:
    """Returns dimensionless time."""
    return (a * time) / (PARTICLE_RADIUS ** 2)


def constant_1(unknown: float) -> float:
    """Solution of this function provides constant required to calculate
    second constant, used in analytical temperature solution."""
    return 1 - (unknown / tan(unknown)) - B


def constant_2(constant_sol: float) -> float:
    """Constant used to calculate analytical temperature solution"""
    numerator = 4 * (sin(constant_sol) - (constant_sol * cos(constant_sol)))
    denominator = 2 * constant_sol - sin(2 * constant_sol)
    return numerator / denominator


CONSTANT_1_SOL = float(fsolve(constant_1, B)[0])
CONSTANT_2_SOL = constant_2(CONSTANT_1_SOL)


def _dimensionless_temperature(r: float, t: float) -> float:
    """Calculates dimensionless temperature as a function of position, r and time, t."""
    exponential = e ** (- CONSTANT_1_SOL ** 2 * dimensionless_time(t))
    return CONSTANT_2_SOL * exponential * (1 / (CONSTANT_1_SOL * dimensionless_pos(r))) * \
        sin(CONSTANT_1_SOL * dimensionless_pos(r))


def time_dependent_temperature(radial_position: float) -> list:
    """Calculates temperature as a function of time for a given radial position within a particle. """
    temperature_vals = []
    for idx, time_step in enumerate(TIME_GRID):
        normal_temp = EXTERNAL_TEMPERATURE + (_dimensionless_temperature(radial_position, time_step) * (
                INITIAL_TEMPERATURE - EXTERNAL_TEMPERATURE))
        # Imposing boundary conditions
        if idx == 0:
            temperature_vals.append(INITIAL_TEMPERATURE)
        elif normal_temp >= INITIAL_TEMPERATURE:
            temperature_vals.append(INITIAL_TEMPERATURE)
        else:
            temperature_vals.append(normal_temp)

    return temperature_vals


def viscosity(temperature: float) -> float:
    """Calculates viscosity as a function of temperature in Kelvins."""
    # TODO: check values for A,B,C are correct
    # TODO: check 873 glass transition temp?

    if temperature > 873:
        return 10 ** (-4.55 + (13389 / (temperature - 311.4)))
    return 10 ** (-4.55 + (13389 / (873 - 311.4)))


def time_dependent_viscosity(r: float) -> list:
    """Returns viscosity variation with time for a given radial position, r."""
    temp_values = time_dependent_temperature(r)
    viscosity_vals = []
    for temp in temp_values:
        viscosity_vals.append(viscosity(temp))
    return viscosity_vals
