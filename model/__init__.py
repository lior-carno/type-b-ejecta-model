from model.modelling_ejecta import grow_bubbles_in_particle
from utils.graph_plotter_utils import GraphPlotter
from utils.process_simulation_data_utils import calculate_bubble_diameter, print_final_simulation_info, \
    print_initial_simulation_info

if __name__ == "__main__":
    while True:
        user_input = input('Would you like to enter interactive mode? Y/N ')
        if user_input == "Y".casefold():
            print("Entering interactive mode!")
        else:
            print("Simulation running with default variables:")
            print_initial_simulation_info()

            break
    position_to_final_bubble_radius = grow_bubbles_in_particle()
    bubble_nucleation_sites_raw = [p for p in position_to_final_bubble_radius.keys()]
    grown_bubble_radii_raw = [r for r in position_to_final_bubble_radius.values()]
    grown_bubble_diameters = calculate_bubble_diameter(grown_bubble_radii_raw)

    GraphPlotter(y_data=grown_bubble_diameters).plot_histogram()
    GraphPlotter(y_data=grown_bubble_diameters).plot_scatter_graph_from_histogram()
    print_final_simulation_info(grown_bubble_radii=grown_bubble_radii_raw,
                                bubble_initial_positions=bubble_nucleation_sites_raw)

