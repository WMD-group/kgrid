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
import ase.io
from argparse import ArgumentParser
from kgrid import calc_kpt_tuple

def calc_grid(cutoff_length,
              mode='default',
              filename='geometry.in',
              filetype=False,
              realspace=False,
              pretty_print=False):

    if filetype:
        atoms = ase.io.read(filename, format=filetype)
    else:
        atoms = ase.io.read(filename)

    k_samples = calc_kpt_tuple(
        atoms, mode=mode, cutoff_length=cutoff_length, realspace=realspace)

    # Print vectors
    if pretty_print:
        print('{0:3.0f} {1:3.0f} {2:3.0f}'.format(*k_samples))
    else:
        return k_samples


def get_parser():
    parser = ArgumentParser()
    parser.add_argument(
        action="store",
        nargs="?",
        type=str,
        dest="file",
        default="geometry.in",
        help="Path to input file [default: ./geometry.in]")
    threshold = parser.add_mutually_exclusive_group()
    threshold.add_argument(
        "-c",
        "--cutoff-length",
        action="store",
        type=float,
        dest="cutoff_length",
        default=10.0,
        help="Set length cutoff in Angstroms [default: 10]")
    threshold.add_argument(
        "-a",
        "--vasp-auto",
        action="store",
        type=float,
        dest="vasp_auto",
        help="Real-space cutoff like Auto in VASP KPOINTS file")
    threshold.add_argument(
        "-s",
        "--vasp-kspacing",
        action="store",
        type=float,
        dest="kspacing",
        help="Reciprocal-space distance like KSPACING in VASP")
    threshold.add_argument(
        "--castep",
        "--castep_spacing",
        "--castep_mp_spacing",
        action="store",
        type=float,
        dest="castep_mp_spacing",
        help=("Reciprocal-space distance like KPOINTS_MP_SPACING in CASTEP; "
              "this differs from Vasp-like KSPACING by factor of 1/(2 pi)."))
    parser.add_argument(
        "-t",
        "--type",
        action="store",
        type=str,
        default=False,
        help="Input file type. If not provided, ASE will guess.")
    parser.add_argument(
        "-r",
        "--realspace",
        action="store_true",
        help="Use real-space vector lengths instead of "
        "computing reciprocal cell; not recommended!")

    return parser


def main(params=None):
    parser = get_parser()
    args = parser.parse_args(params)

    if args.vasp_auto:
        mode = 'vasp_auto'
        cutoff = args.vasp_auto
    elif args.kspacing:
        mode = 'kspacing'
        cutoff = args.kspacing
    elif args.castep_mp_spacing:
        mode = 'castep_mp_spacing'
        cutoff = args.castep_mp_spacing
    else:
        mode = 'default'
        cutoff = args.cutoff_length

    calc_grid(
        cutoff,
        mode=mode,
        filename=args.file,
        filetype=args.type,
        realspace=args.realspace,
        pretty_print=True)


if __name__ == '__main__':
    main()
