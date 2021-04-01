import pathlib

import pytest
import ase.io

import kgrid

data_dir = pathlib.Path('test/data')
sio2 = ase.io.read(data_dir / 'POSCAR')
ga2o3 = ase.io.read(data_dir / 'geometry.in')


@pytest.mark.parametrize('atoms, expected, kwargs',
                         [(sio2, (5, 5, 8), {}),
                          (ga2o3, (2, 7, 4), {}),
                          (sio2, (2, 2, 4), {'mode': 'vasp_auto'}),
                          (sio2, (5, 5, 8), {'mode': 'kspacing',
                                             'cutoff_length': 0.3}),
                          (sio2, (5, 5, 8), {'mode': 'castep_mp_spacing',
                                             'cutoff_length': 0.05})])
def test_calc_kpt_tuple(atoms, expected, kwargs):
    assert kgrid.calc_kpt_tuple(atoms, **kwargs) == expected
