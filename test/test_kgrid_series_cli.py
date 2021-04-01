import pathlib

from numpy.testing import assert_almost_equal
import ase
import ase.io
import pytest

import kgrid.series

data_dir = pathlib.Path('test/data')
sio2_file = data_dir / 'POSCAR'
sio2_atoms = ase.io.read(sio2_file)

nearly_cubic_atoms = ase.Atoms('Ag', cell=[1.0, 1.01, 1.001])

def test_get_increments():
    assert kgrid.series.get_increments([1, 2, 5]) == (0.5, 0.25, 0.1)


@pytest.mark.parametrize('args, kwargs, expected',
                         [([sio2_atoms, 3., 9.], {},
                           [4.0333, 4.2267, 5.3777, 6.34,
                             6.7221, 8.0665, 8.4533]),
                          ([nearly_cubic_atoms, 20, 21], {},
                           [20., 20.02, 20.2, 20.5, 20.5205, 20.705]),
                          ([nearly_cubic_atoms, 20, 21], {'decimals': 1},
                           [20., 20.2, 20.5, 20.7])
                         ])
def test_cutoff_series(args, kwargs, expected):
    result = kgrid.series.cutoff_series(*args, **kwargs)
    assert_almost_equal(result, expected)


@pytest.mark.parametrize('params, expected',
                         [([str(sio2_file), '-t', 'vasp',
                            '--min=4', '--max', '7',
                            '--comma_sep'],
                            "2 2 3,2 2 4,3 3 4,3 3 5,4 4 5\n"),
                          ([str(sio2_file),
                            '--min=2', '--max', '4',
                            '--castep'],
                           ('Length cutoff  MP SPACING    Samples\n'
                            '-------------  ----------  ------------\n'
                            '       2.113    0.236597     1   1   2\n'
                            '       2.689    0.185957     2   2   2\n'
                            )),])
def test_cli_output(capsys, params, expected):
    kgrid.series.main(params)
    captured = capsys.readouterr()

    assert captured.out == expected
