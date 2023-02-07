from math import pi
import numpy as np

from constants.initial_conditions_constants import BUBBLE_NUMBER, INITIAL_TEMPERATURE
from constants.simulation_constants import PARTICLE_RADIUS, SIMULATION_LENGTH


def calculate_volume(radius: float) -> float:
    return (4 / 3) * pi * (radius ** 3)


def calculate_particle_diameters(radius: float) -> float:
    return radius * (10 ** 6) * 2


def calculate_bubble_diameter(bubble_radii: list) -> list:
    np_array = np.array(bubble_radii) * 2 * 10 ** 6
    return np_array.tolist()


def calculate_bubble_initial_positions(bubble_positions: list) -> list:
    np_array = np.array(bubble_positions) * PARTICLE_RADIUS * 10 ** 6
    return np_array.tolist()


def calculate_bubble_volume_ratio(raw_bubble_radii: list) -> float:
    total_vol = 0
    for index, _ in enumerate(raw_bubble_radii):
        total_vol += calculate_volume(raw_bubble_radii[index])

    ratio = total_vol / calculate_volume(PARTICLE_RADIUS)
    return ratio


def print_initial_simulation_info() -> None:
    print(f'Initial temperature: {INITIAL_TEMPERATURE}K')
    print(f'Simulation length:{SIMULATION_LENGTH}s')
    print(f'Particle_radius:{PARTICLE_RADIUS}\u03BCm')
    print(f'Particle volume: {calculate_volume(PARTICLE_RADIUS)}\u03BCm ^3')
    print('-------------------------------------------------------------')


def print_final_simulation_info(grown_bubble_radii: list, bubble_initial_positions: list) -> None:
    print(f'Number of bubbles per probe: {int(BUBBLE_NUMBER * PARTICLE_RADIUS)}')
    print(f'Total bubble number: {int(BUBBLE_NUMBER * PARTICLE_RADIUS) * 10}')
    print(f'Final bubble diameters: {calculate_bubble_diameter(grown_bubble_radii)}')
    print(f'Bubble initial positions (normalised): {bubble_initial_positions}')
    print(
        f'Bubble initial positions (raw): {calculate_bubble_initial_positions(bubble_initial_positions)}')
    # print(f'Bubble volume percentage: {calculate_bubble_volume_ratio(grown_bubble_radii) * 100}%')
