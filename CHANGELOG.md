# Change Log

Notable changes are logged here by release. This project is not
expected to be especially active and follows a simplified Semantic Versioning:

- Version numbers take the format X.Y
- X is associated with major API breakage / changes in algorithm and results.
- Y is associated with minor updates and improvements
- Small amounts of code tidying, refactoring and documentation do not
  lead to a new release, and simply sit on the Development branch of
  the Git repository.

The changelog format is inspired by [keep-a-changelog](https://github.com/olivierlacan/keep-a-changelog).

## [Unreleased]

### Fixed
- ASE > 3.21 compatibility, backwards-compatible to ASE 3.18.

### Changed
- Atoms method (`atoms.get_reciprocal_cell()`) replaced by Cell method (`atoms.cell.reciprocal()`).

## [1.1] - 2018-04-30

### Fixed
- Python3 compatibility
- Bug in decimal place tolerance option

### Added
- Comma-separated kgrid-series output option
- CASTEP-like reciprocal spacing cutoff (2 pi factor smaller than KSPACING)

### Changed
- Make filename a positional argument; -f or --filename no longer needed

## [1.0] - 2016-10-07

### Changed
- Correctly calculate reciprocal lattice vectors using whole
  cell. This is the new default behaviour. Former behaviour ("naive"
  apprach using only lengths of real-space cell) made available as
  option through Python interface and CLI.
- Restructure repository for packaging with setuptools
- Installation instructions in README

### Added
- New emulation of VASP Auto and KSPACING modes.
- Setuptools installation
- New range generator for convergence testing: **kgrid-series**

## [0.2] - 2016-07-28

### Added
- Present useful Python API for use with [Atomic Simulation Environment (ASE)](https://wiki.fysik.dtu.dk/ase/) calculators

### Changed
- Import routine uses [Atomic Simulation Environment](https://wiki.fysik.dtu.dk/ase/). This adds a
  dependency, but permits import of almost any major crystal structure
  file format.

## 0.1 - 2013-06-01

### Added
- Basic codebase reading from FHI-aims input files
- Optparse-based interface
- GPL

[Unreleased]: https://github.com/wmd-group/kgrid/compare/v1.1...HEAD
[1.1]: https://github.com/wmd-group/kgrid/compare/v1.0...v1.1
[1.0]: https://github.com/wmd-group/kgrid/compare/v0.2...v1.0
[0.2]: https://github.com/wmd-group/kgrid/compare/v0.1...v0.2
