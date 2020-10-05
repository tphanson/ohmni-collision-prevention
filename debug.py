import numpy as np
from src.pathplanning import PathPlanning

pp = PathPlanning()
trajectory = pp.dijkstra(np.zeros(pp.density), [6, 6], [0, 11])
print(trajectory)
