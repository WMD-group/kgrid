#! /usr/bin/env python

"""Get k-grid parameters for desired length cutoff and input geometry"""

##############################################################################################
# Copyright 2015 Adam Jackson
##############################################################################################
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
##############################################################################################

import numpy as np
from optparse import OptionParser
import ase.io

def calc_grid(cutoff_length, filename='geometry.in', filetype=False, pretty_print=False):

    if filetype:
        atoms = ase.io.read(filename, format=filetype)
    else:
        atoms = ase.io.read(filename)

    # Import lattice vectors using ASE
    lattice_vectors = atoms.cell

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
    if pretty_print:
        print '{0:3.0f} {1:3.0f} {2:3.0f}'.format(k_samples[0],k_samples[1],k_samples[2])
    else:
        return k_samples


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-c", "--cutoff-length",
                      action="store", type="float", dest="cutoff_length", default=10.0,
                      help="Set length cutoff in Angstroms [default: 10]")
    parser.add_option("-f", "--file",
                      action="store", type="string", dest="file", default="geometry.in",
                      help="Path to input file [default: ./geometry.in]")
    parser.add_option("-t", "--type", action="store", type="string", default=False,
                      help="Input file type. If not provided, ASE will guess.")
    # Add further options here
    (options, args) = parser.parse_args()

    calc_grid(options.cutoff_length, filename=options.file, filetype=options.type, pretty_print=True)
