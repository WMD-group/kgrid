kgrid
=====

Generates a suitably converged **k**-point grid for solid-state quantum chemical calculations.

Current status
--------------

* Acts on FHI-aims geometry.in file in the working directory
* Target length cutoff of 10Å is coded into program
* A **k**-point density is selected to satisfy this length cutoff, as described by Moreno & Soler (1992)[1]
* Returns the **k**-point grid to standard output

Short-term goals
----------------

* Take input file and length cutoff as optional arguments
* Default to working directory and 10Å (generally well-converged for semiconducting or insulating materials)
* Support for VASP (delegated to Lee Burton)

Long-term goals
---------------

* Generate suitable input files directly
    * This may involve integrating this script into a larger, more general program

Disclaimer
----------

This program is not affiliated with FHI-aims. You are welcome to use it and build on it, but do so at your own risk.

References
----------

[1] Moreno, J., & Soler, J. (1992). Optimal meshes for integrals in real- and reciprocal-space unit cells. *Physical Review B*, 45(24), 13891–13898. [doi:10.1103/PhysRevB.45.13891](http://dx.doi.org/10.1103/PhysRevB.45.13891)
