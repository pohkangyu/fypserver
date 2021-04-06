import pandas as pd
from idtxlmodules import MultiVariateTime
from idtxl.data import Data
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg

dataframe = pd.read_csv("C:\\Users\\kangyu\\Desktop\\FYP\\stock.csv")
numpy_format = dataframe.to_numpy()
arr_format = numpy_format.reshape((3, len(numpy_format), 1))
settings = {'cmi_estimator': 'JidtGaussianCMI',
            'max_lag_sources': 5,
            'min_lag_sources': 1}

mod = MultiVariateTime(Data(arr_format), settings)
a, b = mod.run()
b
b.savefig("test.png")
