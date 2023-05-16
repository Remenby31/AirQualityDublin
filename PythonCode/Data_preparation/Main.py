from matrix import matrix
import numpy as np
from matplotlib import pyplot as plt

# On creer la matrice
matrice = matrix()

# On recupere la matrice 3D
matrix3D_pm25, matrix3D_pm10 = matrice.getMatrix()

# On enregistre la matrice 3D
np.save('matrix3D_pm25_v3.npy', matrix3D_pm25)
np.save('matrix3D_pm10_v3.npy', matrix3D_pm10)