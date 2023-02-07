class GraphPlotter:
    def __init__(self, y_data, x_label="Bubble Diameter [\u03BCm]", y_label="", x_data=None):
        import matplotlib.pyplot as plt

        self.x_data = x_data
        self.y_data = y_data
        self.x_label = x_label
        self.y_label = y_label
        self.plot = plt

    def plot_histogram(self, y_label="Probability Density", save_fig=False, figure_title=None):
        self.plot.figure()
        self.plot.hist(self.y_data, density=True)
        self.plot.xlabel(self.x_label)
        self.plot.ylabel(y_label if y_label else self.y_label)
        self.plot.grid(which='both', axis='both', linestyle='--')
        if save_fig:
            self.plot.savefig(figure_title)

        self.plot.show()

    def _extract_hist_data(self):
        import numpy as np
        counts, bins = np.histogram(self.y_data, bins=20, density=True)
        scatter_points = []
        for idx in range(1, len(bins)):
            scatter_points.append((bins[idx] + bins[idx - 1]) / 2)

        return counts, scatter_points

    def plot_scatter_graph_from_histogram(self, y_label="Frequency", save_fig=False, figure_title=None):
        import numpy as np

        counts, scatter_points = self._extract_hist_data()

        self.plot.figure()
        # plot larger points line
        self.plot.scatter(scatter_points, counts, marker='o', linewidth=0.1)
        # plot continuous line
        self.plot.plot(scatter_points, counts, linewidth=1)
        self.plot.xlabel(self.x_label)
        self.plot.ylabel(y_label if y_label else self.y_label)
        # Plot initial position straight line
        self.plot.plot(np.linspace(17.6, 17.6, len(counts)), counts, 'k', linewidth=0)
        self.plot.grid(which='both', axis='both', linestyle='--')
        if save_fig:
            self.plot.savefig(figure_title)
        self.plot.show()
