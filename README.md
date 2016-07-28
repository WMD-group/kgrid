kgrid
=====

Generates a suitably converged **k**-point grid for solid-state
quantum chemical calculations.

Current status
--------------

* Reads specified input file using Atomic Simulation Environment ([supported formats](https://wiki.fysik.dtu.dk/ase/ase/io.html#module-ase.io))
  * If none is specified, looks for geometry.in (FHI-aims) in working directory
* A **k**-point density is selected to satisfy a given length cutoff, as
  described by Moreno & Soler (1992)[1]
* This **k**-point grid is expressed as a number of samples in each
  lattice vector and passed to standard output
* Default **k**-point cutoff is 10Å (generally well-converged for
  semiconducting or insulating materials)
* Optional arguments are implemented with conventional GNU/POSIX
  syntax, including -h help option

Requirements
------------

* Developed with Python 2.7; not tested with other versions
* [Atomic Simulation Environment](https://wiki.fysik.dtu.dk/ase) (ASE)
* [Numpy](www.numpy.org) (Also a requirement for ASE.)

Usage
-----

From the command line

```
    kgrid.py -f FILE -t TYPE -c CUTOFF
```

will return a suggested set of mesh dimensions. FILE can be any
[file format supported by ASE](https://wiki.fysik.dtu.dk/ase/ase/io/io.html);
if no FILE is specified, **kgrid** will look for a *geometry.in* file in
the current directory. TYPE is a string specifying the format of this
file; usually this argument can be left out and the correct type will
be inferred by ASE. CUTOFF is the real-space cutoff parameter in Å and
defaults to 10.0.

There is an internal Python function which may prove useful to ASE users, with the form
```
kgrid.calc_kpt_tuple(atoms, cutoff_length=10)
```

where `atoms` is an ASE atoms object and the function returns a
tuple. As such, **kgrid** may be used while setting up a calculation
with a typical ASE calculator. For example:

```
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


Disclaimer
----------

This program is not affiliated with ASE or any particular quantum chemistry code.
This program is made available under the GNU General Public License; you are free to modify and use the code, but do so at your own risk.

References
----------

[1] Moreno, J., & Soler, J. (1992). Optimal meshes for integrals in real- and reciprocal-space unit cells. *Physical Review B*, 45(24), 13891–13898. [doi:10.1103/PhysRevB.45.13891](http://dx.doi.org/10.1103/PhysRevB.45.13891)
