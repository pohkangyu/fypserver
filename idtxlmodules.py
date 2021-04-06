# Import classes
from idtxl.multivariate_te import MultivariateTE
from idtxl.data import Data
from idtxl.visualise_graph import plot_network
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from idtxl.data import Data

class MultiVariateTime():
    def __init__(self, data, settings):
        self.data = data
        self.settings = settings

    def run(self):
        network_analysis = MultivariateTE()
        results = network_analysis.analyse_network(settings=self.settings, data=self.data)
        #results.print_edge_list(weights='max_te_lag', fdr=False)
        return plot_network(results=results, weights='max_te_lag', fdr=False)
