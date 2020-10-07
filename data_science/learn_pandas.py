import pandas as pd
from numpy.random import exponential
import matplotlib.pyplot as plt

df = pd.DataFrame({'x': range(20), 'y': exponential(10, 20)})

df.y.hist()