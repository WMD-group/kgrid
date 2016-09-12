#! /usr/bin/env python

"""Get k-grid parameters for desired length cutoff and input geometry"""

###############################################################################
# Copyright 2015 Adam Jackson
###############################################################################
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
###############################################################################

import numpy as np
from argparse import ArgumentParser
import ase.io

def calc_grid(cutoff_length, mode='default', filename='geometry.in',
              filetype=False, realspace=False, pretty_print=False):

    if filetype:
        atoms = ase.io.read(filename, format=filetype)
    else:
        atoms = ase.io.read(filename)

    k_samples = calc_kpt_tuple(atoms, mode=mode,
                               cutoff_length=cutoff_length,
                               realspace=realspace)

    # Print vectors
    if pretty_print:
        print '{0:3.0f} {1:3.0f} {2:3.0f}'.format(*k_samples)
    else:
        return k_samples


def calc_kpt_tuple(atoms, cutoff_length=10, realspace=False, mode='default'):
    """Calculate k-point mesh from ASE atoms object for real-space cutoff

    Args:
        :param atoms: Periodic crystal structure
        :type ase.atoms.Atoms
        :param cutoff_length: Parameter determining sample density
        :type float
        :param mode: Calculation mode; this determines the units of
            cutoff_length.
            default: Cutoff is length in Angstroms corresponding to
                non-overlapping radius in a hypothetical supercell
                (Moreno-Soler length cutoff).
            vasp_auto: Cutoff is length in Angstroms to be multiplied by
                reciprocal lattice -- equivalent to double the value used in
                default mode. This attempts to emulate the "fully automatic"
                option in a VASP k-points file.
            kspacing: Cutoff has units of reciprocal Angstroms and represents
                minimum sampling density in reciprocal space. Equivalent to
                1/(2*cutoff) in default mode. This attempts to emulate the
                KSPACING parameter in VASP.
        :type str
        :returns: Number of samples in each reciprocal lattice vector
        :rtype: 3-tuple
        """

    if mode.lower() == 'default':
        rounding = 'up'
    elif mode.lower() == 'vasp_auto':
        cutoff_length = (cutoff_length) / 2.
        rounding = 'nearest'
    elif mode.lower() == 'kspacing':
        cutoff_length = np.pi / cutoff_length
        rounding = 'up'

    if realspace:
        return calc_kpt_tuple_naive(atoms, cutoff_length=cutoff_length,
                                    rounding=rounding)
    else:
        return calc_kpt_tuple_recip(atoms, cutoff_length=cutoff_length,
                                    rounding=rounding)


def calc_kpt_tuple_naive(atoms, cutoff_length=10, rounding='up'):
    """Calculate k-point grid using real-space lattice vectors"""

    # Import lattice vectors using ASE
    lattice_vectors = atoms.cell

    # Get lattice vector magnitudes (a, b, c) according to Pythagoras' theorem
    abc = np.sqrt(np.sum(np.square(lattice_vectors),1))

    # k-point samples required = 2*cutoff_length/(magnitude of lattice vector)
    k_samples = np.divide(2*cutoff_length,abc)

    # Rounding
    if rounding == 'up':
        k_samples = np.ceil(k_samples)
    else:
        k_samples = np.floor(k_samples + 0.5)
    return tuple((int(x) for x in k_samples))


def calc_kpt_tuple_recip(atoms, cutoff_length=10, rounding='up'):
    """Calculate reciprocal-space sampling with real-space parameter"""
    # Get reciprocal lattice vectors with ASE. Note that ASE does NOT include
    # the 2*pi factor used in many definitions of these vectors; the underlying
    # method is just a matrix inversoin and transposition
    recip_cell = atoms.get_reciprocal_cell()

    # Get reciprocal cell vector magnitudes according to Pythagoras' theorem
    abc_recip = np.sqrt(np.sum(np.square(recip_cell),1))

    k_samples = abc_recip * 2 * cutoff_length

    # Rounding
    if rounding == 'up':
        k_samples = np.ceil(k_samples)
    else:
        k_samples = np.floor(k_samples + 0.5)
    return tuple((int(x) for x in k_samples))

if __name__ == '__main__':
    parser = ArgumentParser()
    threshold = parser.add_mutually_exclusive_group()
    threshold.add_argument("-c", "--cutoff-length",
                      action="store", type=float, dest="cutoff_length",
                      default=10.0,
                      help="Set length cutoff in Angstroms [default: 10]")
    threshold.add_argument("-a", "--vasp-auto", action="store", type=float,
                      dest="vasp_auto",
                      help="Real-space cutoff like Auto in VASP KPOINTS file")
    threshold.add_argument("-s", "--vasp-kspacing",
                      action="store", type=float, dest="kspacing",
                      help="Reciprocal space distance like KSPACING in VASP")

    parser.add_argument("-f", "--file",
                      action="store", type=str, dest="file",
                      default="geometry.in",
                      help="Path to input file [default: ./geometry.in]")
    parser.add_argument("-t", "--type", action="store", type=str,
                      default=False,
                      help="Input file type. If not provided, ASE will guess.")
    parser.add_argument("-r", "--realspace", action="store_true",
                      help="Use real-space vector lengths instead of "
                           "computing reciprocal cell; not recommended!")
    # Add further options here
    args = parser.parse_args()

    if args.vasp_auto:
        mode = 'vasp_auto'
        cutoff = args.vasp_auto
    elif args.kspacing:
        mode = 'kspacing'
        cutoff = args.kspacing
    else:
        mode = 'default'
        cutoff = args.cutoff_length

    calc_grid(cutoff, mode=mode, filename=args.file,
              filetype=args.type, realspace=args.realspace,
              pretty_print=True)
