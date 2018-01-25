#! /usr/bin/env python

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
from __future__ import print_function
from argparse import ArgumentParser
import numpy as np

import ase.io
from kgrid import calc_kpt_tuple


def get_increments(lattice_lengths):
    """
    Calculate the vector l0 of increments between significant length cutoffs
    for each reciprocal lattice vector.

    :param lattice_lengths: Lengths of reciprocal lattice vectors
    :type 3-tuple

    :returns: Vector l0 of significant increments
    :rtype: 3-tuple
    """

    return tuple([1. / (2 * a) for a in lattice_lengths])


def cutoff_series(atoms, l_min, l_max, decimals=4):
    """Find multiples of l0 members within a range

    :param atoms: Crystal structure
    :type ase.atoms.Atoms
    :param l_min: Minimum real-space cutoff
    :type float
    :param l_max: Maximum real-space cutoff
    :type float
    :param decimals: Number of decimal places used when rounding to remove
        duplicates
    :type int

    :returns: Sorted list of cutoffs
    :rtype: list
"""
    recip_cell = atoms.get_reciprocal_cell()
    lattice_lengths = np.sqrt(np.sum(np.square(recip_cell), 1))

    l0 = get_increments(lattice_lengths)

    members = set()
    for li in l0:
        n_min = np.ceil(l_min / li)
        members.update(
            set(np.around(
                np.arange(n_min * li, l_max, li), decimals=decimals)))
    return sorted(members)


def kspacing_series(atoms, l_min, l_max, decimals=4):
    """Find series of KSPACING values with different results

    NB: It is strongly recommended to ADD a small delta to these values
    to account for truncation/rounding errors

    :param atoms: Crystal structure
    :type ase.atoms.Atoms
    :param l_min: Minimum real-space cutoff
    :type float
    :param l_max: Maximum real-space cutoff
    :type float

    :returns: Sorted list of KSPACING values
    :rtype: list
    """

    return [np.pi / c for c in
            cutoff_series(atoms, l_min, l_max, decimals=decimals)]


def main():
    parser = ArgumentParser("Calculate a systematic series of k-point samples")
    parser.add_argument(
        "structure",
        type=str,
        help="Path to input file",
        nargs='?',
        default=None
        )
    parser.add_argument(
        "-f",
        "--file",
        action="store",
        type=str,
        dest="file",
        default="geometry.in",
        help="Path to input file [default: ./geometry.in]")    
    parser.add_argument(
        '-t',
        '--type',
        type=str,
        default=None,
        help='Format of crystal structure file')
    parser.add_argument(
        '--min',
        type=float,
        default=10,
        help='Minimum real-space cutoff / angstroms')
    parser.add_argument(
        '--max',
        type=float,
        default=30,
        help='Maximum real-space cutoff / angstroms')

    args = parser.parse_args()

    if args.structure is None:
        filename = args.file
    else:
        filename = args.structure        

    if args.type:
        atoms = ase.io.read(filename, format=args.type)
    else:
        atoms = ase.io.read(filename)

    cutoffs = cutoff_series(atoms, args.min, args.max)

    kspacing = [np.pi / c for c in cutoffs]

    samples = [calc_kpt_tuple(
        atoms, cutoff_length=(cutoff - 1e-4)) for cutoff in cutoffs]

    print("Length cutoff  KSPACING    Samples")
    print("-------------  --------  ------------")

    fstring = "{0:12.3f}   {1:7.4f}   {2:3d} {3:3d} {4:3d}"
    for cutoff, s, sample in zip(cutoffs, kspacing, samples):
        print(fstring.format(cutoff, s, *sample))


if __name__ == '__main__':
    main()
