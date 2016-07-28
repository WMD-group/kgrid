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

[Unreleased]: https://github.com/wmd-group/kgrid/compare/v0.2...HEAD
[0.2]: https://github.com/wmd-group/kgrid/compare/v0.1...v0.2
