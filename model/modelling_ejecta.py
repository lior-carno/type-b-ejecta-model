import random
import numpy as np
from constants.simulation_constants import SIMULATION_LENGTH, PARTICLE_RADIUS, POSITION_GRID, dt, dR
from constants.initial_conditions_constants import INITIAL_BUBBLE_RADIUS, BUBBLE_NUMBER
from model.bubble_growth import grow_euler


def bubble_nucleation() -> np.array:
    """Initialises bubble nucleation sites along a 1D profile. """
    # Must always have integer number of bubbles
    bubble_number = int(BUBBLE_NUMBER * PARTICLE_RADIUS)
    # Converts numpy array to a list for the randomiser
    grid_list = POSITION_GRID.tolist()

    if bubble_number > len(POSITION_GRID):
        raise ValueError("Bubble number exceeds grid resolution. Use a finer grid!")
    bubble_nucleation_sites = np.array(random.sample(grid_list, bubble_number))
    print(f"Particle size = {PARTICLE_RADIUS} m. \nGrid resolution = {dR}m. \nNumber of bubbles = {bubble_number}. \n")

    return bubble_nucleation_sites


def grow_bubbles_in_particle(probe_number: int = 10) -> dict[float:float]:
    """Bubble growth simulated  <probe_number> number of times  using the same temperature and
    viscosity profile for multiple bubbles with different initial positions along a 1D grid """

    position_to_final_radius = {}

    # Simulation repeated <probe_number> number of times
    for probe in range(probe_number):

        print(
            f"Simulation length = {SIMULATION_LENGTH}.\nTime resolution = {dt}.\nBubble starting radius = {INITIAL_BUBBLE_RADIUS}.\n")

        bubble_nucleation_sites = bubble_nucleation()
        for idx, _ in enumerate(bubble_nucleation_sites):
            bubble_position = bubble_nucleation_sites[idx] / PARTICLE_RADIUS
            bubble_radial_growth, _ = grow_euler(bubble_nucleation_sites[idx])
            # {bubble position:final bubble radius}
            position_to_final_radius[bubble_position] = bubble_radial_growth[-1]

            print(f"Bubble position = {bubble_position}")

    return position_to_final_radius
