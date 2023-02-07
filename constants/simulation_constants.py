import numpy as np

dR = 10 ** -8  # Radial grid spacing
dt = 10 ** -4  # Time step
SIMULATION_LENGTH = 0.02  # Final time
PARTICLE_RADIUS = 384.5 * (10 ** -6)  # Particle radius

POSITION_GRID = np.arange(10 ** -20, PARTICLE_RADIUS, dR)
TIME_GRID = np.arange(0, SIMULATION_LENGTH, dt)
