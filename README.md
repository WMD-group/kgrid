kgrid
=====

Version 1.2: [Change log](./CHANGELOG.md)

Generates a suitably converged **k**-point grid for solid-state
quantum chemical calculations.

Current status
--------------

Two programs are provided: kgrid and kgrid-series

### kgrid
* The specified input file is read using Atomic Simulation Environment ([supported formats](https://wiki.fysik.dtu.dk/ase/ase/io.html#module-ase.io))
  * If none is specified, looks for geometry.in (FHI-aims) in working directory
* A **k**-point density is selected to satisfy a given length cutoff,
  as described by Moreno & Soler (1992)[1]. The length cutoff
  corresponds to a radius about repeated images that would be needed
  in a gamma-point supercell calculation to achieve the same sampling.
* This **k**-point grid is expressed as a number of samples in each
  lattice vector and passed to standard output. (Note that this is NOT
  a Moreno-Soler grid as it does not use symmetry information to
  minimise the required number of points. It is a uniform grid
  specified with the same length parameter notation.)
* Default **k**-point cutoff is 10Å (generally well-converged for
  semiconducting or insulating materials)
* Optional arguments are implemented with conventional GNU/POSIX
  syntax, including -h help option

### kgrid-series
* Reports a series of "critical" cutoffs and KSPACING values with
  their corresponding k-point grids.
* These may be very useful for convergence testing, but users should be
  wary of rounding behaviour near these values.

Requirements
------------

* Python 3.6
* [Atomic Simulation Environment](https://wiki.fysik.dtu.dk/ase) (ASE) version 3.18

Usage
-----

### kgrid
From the command line

``` bash
    kgrid FILE -t TYPE -c CUTOFF
```

will return a suggested set of mesh dimensions. FILE can be any
[file format supported by ASE](https://wiki.fysik.dtu.dk/ase/ase/io/io.html);
if no FILE is specified, **kgrid** will look for a *geometry.in* file in
the current directory. TYPE is a string specifying the format of this
file; usually this argument can be left out and the correct type will
be inferred by ASE. CUTOFF is the real-space cutoff parameter in Å and
defaults to 10.0.

There is an internal Python function which may prove useful to ASE users, with the form
``` python
kgrid.calc_kpt_tuple(atoms, cutoff_length=10)
```

where `atoms` is an ASE atoms object and the function returns a
tuple. As such, **kgrid** may be used while setting up a calculation
with a typical ASE calculator. For example:

``` python
import kgrid
from ase.io import read
from ase.calculators.vasp import Vasp

atoms = read('my_favourite_structure.cif')
calc = Vasp(xc='PBE',
            kpts=kgrid.calc_kpt_tuple(atoms))
atoms.set_calculator(calc)
atoms.get_total_energy()
```

would perform a VASP calculation in the current directory with the PBE
functional, using **kgrid** to determine the reciprocal-space sampling.

### kgrid-series

``` bash
kgrid-series FILE -t TYPE --min MIN --max MAX
```

Example output:

``` bash
Length cutoff  KSPACING    Samples
-------------  --------  ------------
      10.630    0.2956     2   7   4
      11.260    0.2790     2   8   4
      11.860    0.2649     2   8   5
      12.148    0.2586     3   8   5
      13.666    0.2299     3   9   5
      14.075    0.2232     3  10   5
      15.185    0.2069     3  10   6
      16.703    0.1881     3  11   6
      16.890    0.1860     3  12   6
      17.790    0.1766     3  12   7
      18.222    0.1724     4  12   7
      19.705    0.1594     4  13   7
      19.741    0.1591     4  13   8
      21.259    0.1478     4  14   8
      22.520    0.1395     4  15   8
      22.777    0.1379     4  15   9
      23.720    0.1324     4  16   9
      24.296    0.1293     5  16   9
      25.335    0.1240     5  17   9
      25.814    0.1217     5  17  10
      27.333    0.1149     5  18  10
      28.150    0.1116     5  19  10
      28.852    0.1089     5  19  11
      29.650    0.1060     5  20  11

```

Use the `--castep` option to replace KSPACING with "MP SPACING", which
corresponds to the *KPOINTS_MP_SPACING* parameter in CASTEP
(i.e. divide by 2π).

INSTALLATION
------------

**kgrid** uses setuptools; from a reasonable healthy Python environment you can use

    pip install .

with the usual pip caveats:

- the `--user` flag is highly recommended and avoids the need for administrator privileges, but on a somewhat unhealthy Python installation the user packages location may not be on your paths yet.
- the `-e` flag creates an "editable" installation which links to this repository and enables easy updates with git.

**kgrid** is not developed on Windows but no problems are anticipated; the Anaconda Python distribution includes pip. We have had good experiences using the Windows subsystem for Linux (WSL), available on Windows 10.
On Mac OSX, the system Python does not include pip but there are various ways of getting a more complete distribution such as Homebrew or Anaconda.

Testing
-------

To run the unit tests, install `pytest` and `pytest-mock` and run
`pytest` from the project directory (i.e. the folder containing this
README.)

Disclaimer
----------

This program is not affiliated with ASE or any particular quantum chemistry code.
This program is made available under the GNU General Public License; you are free to modify and use the code, but do so at your own risk.

References
----------

[1] Moreno, J., & Soler, J. (1992). Optimal meshes for integrals in real- and reciprocal-space unit cells. *Physical Review B*, 45(24), 13891–13898. [doi:10.1103/PhysRevB.45.13891](http://dx.doi.org/10.1103/PhysRevB.45.13891)
