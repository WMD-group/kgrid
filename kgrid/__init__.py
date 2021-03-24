###############################################################################
# Copyright 2016 Adam Jackson
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
    elif mode.lower() == 'castep_mp_spacing':
        cutoff_length = 1 / (2 * cutoff_length)
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
    recip_cell = atoms.cell.reciprocal()

    # Get reciprocal cell vector magnitudes according to Pythagoras' theorem
    abc_recip = np.sqrt(np.sum(np.square(recip_cell),1))

    k_samples = abc_recip * 2 * cutoff_length

    # Rounding
    if rounding == 'up':
        k_samples = np.ceil(k_samples)
    else:
        k_samples = np.floor(k_samples + 0.5)
    return tuple((int(x) for x in k_samples))

