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

Disclaimer
----------

This program is not affiliated with ASE or any particular quantum chemistry code.
This program is made available under the GNU General Public License; you are free to modify and use the code, but do so at your own risk.

References
----------

[1] Moreno, J., & Soler, J. (1992). Optimal meshes for integrals in real- and reciprocal-space unit cells. *Physical Review B*, 45(24), 13891–13898. [doi:10.1103/PhysRevB.45.13891](http://dx.doi.org/10.1103/PhysRevB.45.13891)
