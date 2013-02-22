#! /usr/bin/env python

"""Get k-grid parameters for desired length cutoff and input geometry"""

import numpy as np
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-c", "--cutoff-length",
                  action="store", type="float", dest="cutoff_length", default=10.0,
                  help="Set length cutoff in Angstroms [default: 10]")
parser.add_option("-f", "--file",
                  action="store", type="string", dest="file", default="geometry.in",
                  help="Path to input file [default: ./geometry.in]")
# Add further options here
(options, args) = parser.parse_args()

cutoff_length = options.cutoff_length

# Import columns 2:4 (python indexes from 0) from FHI-aims input file
lattice_vectors = np.genfromtxt(options.file,skip_header=0, comments='#',usecols=(1,2,3))
# Truncate to top 3 rows
lattice_vectors = lattice_vectors[0:3,:]

# Get lattice vector magnitudes (a, b, c) according to Pythagoras' theorem
abc = np.sqrt(np.sum(np.square(lattice_vectors),1))

# k-point samples required = 2*cutoff_length/(magnitude of lattice vector)
k_samples = np.divide(2*cutoff_length,abc)
# Round up
k_samples = np.ceil(k_samples)

#### NOTE: For some schemes it is preferred to only use odd or even numbers of
#### k-points. This is unlikely to be necessary in FHI-aims as the Gamma point
#### is always included. For VASP however this may be worth considering.

# Print vectors
print '{0:3.0f} {1:3.0f} {2:3.0f}'.format(k_samples[0],k_samples[1],k_samples[2])

