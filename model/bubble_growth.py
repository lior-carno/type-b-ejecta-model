from constants.initial_conditions_constants import INITIAL_INTERNAL_PRESSURE, INITIAL_BUBBLE_RADIUS, \
    THIN_SHELL_THICKNESS, EXTERNAL_PRESSURE, GLASS_TRANSITION_TEMP
from constants.simulation_constants import TIME_GRID, dt
from model.viscosity_temperature import time_dependent_viscosity
from model.viscosity_temperature import viscosity

GLASS_TRANSITION_VISC = viscosity(GLASS_TRANSITION_TEMP)


def thin_shell(r: float, m: float) -> float:
    """Calculates rate of bubble growth"""
    return ((((INITIAL_INTERNAL_PRESSURE * (INITIAL_BUBBLE_RADIUS ** 3)) / (r ** 3)) - EXTERNAL_PRESSURE) * r ** 4) / (
            12 * m * (INITIAL_BUBBLE_RADIUS ** 2) * THIN_SHELL_THICKNESS)


def grow_euler(radial_position: float) -> tuple[list, list]:
    """ Calculates bubble growth using euler equation?"""
    bubble_radius_values = []
    viscosity_values = []

    # Initial bubble radius
    bubble_radius = INITIAL_BUBBLE_RADIUS
    bubble_radius_values.append(bubble_radius)
    for idx, time in enumerate(TIME_GRID):
        # Viscosity variation with time for a given radial position
        time_dependent_visc = time_dependent_viscosity(radial_position)
        visc = time_dependent_visc[idx]
        viscosity_values.append(time_dependent_visc[idx])

        # Bubble will continue to grow if the viscosity is less than the glass transition viscosity
        if visc < GLASS_TRANSITION_VISC:

            bubble_radius += (thin_shell(bubble_radius, visc) * dt)  # propagates the bubble growth equation
            bubble_radius_values.append(bubble_radius)

        else:
            # CHECK THIS, why are we setting to initial radius?
            bubble_radius_values.append(bubble_radius)

    return bubble_radius_values, viscosity_values
