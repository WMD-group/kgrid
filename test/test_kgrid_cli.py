import pathlib

import pytest

import kgrid.cli

data_dir = pathlib.Path('test/data')
sio2 = data_dir / 'POSCAR'

# ga2o3 = ase.io.read(data_dir / 'geometry.in')


def test_calc_grid_output(capsys):
    kgrid.cli.calc_grid(15., filename=str(sio2), pretty_print=True)
    captured = capsys.readouterr()

    assert captured.out == '  8   8  12\n'

def test_calc_grid_format(tmp_path):
    tmpdir = tmp_path / "calc-grid"
    tmpdir.mkdir()

    with open(sio2) as fd:
        poscar_data = fd.read()

    (tmpdir / 'ambiguous-name').write_text(poscar_data)

    assert kgrid.cli.calc_grid(15., filename=(tmpdir / 'ambiguous-name'),
                               filetype='vasp') == (8, 8, 12)
