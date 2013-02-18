########### How to import lattice vectors from POSCAR #######
import numpy as np

# Open file
f = open('POSCAR')
# Throw away the first two lines
_ = f.readline()
_ = f.readline()

# Copy lattice vector lines to strings
a_string = f.readline()
b_string = f.readline()
c_string = f.readline()

# Convert to numpy vectors and concatenate
a_vect = np.array([float(x) for x in a_string.split])
b_vect = np.array([float(x) for x in b_string.split])
c_vect = np.array([float(x) for x in c_string.split])

lattice_vectors = np.array([a_vect,b_vect,c_vect])

