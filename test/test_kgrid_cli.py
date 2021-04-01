import pathlib

import pytest

import kgrid.cli

data_dir = pathlib.Path('test/data')
sio2 = data_dir / 'POSCAR'


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


@pytest.mark.parametrize('args, expected_args, expected_kwargs',
                         [(['the_file', '-a', '12'],
                           [12], {'filename': 'the_file',
                                  'mode': 'vasp_auto',
                                  'filetype': False,
                                  'realspace': False,
                                  'pretty_print': True}),
                          (['the_cell_file', '--castep_spacing', '0.05',
                            '-t', 'castep'],
                           [0.05], {'filename': 'the_cell_file',
                                    'mode': 'castep_mp_spacing',
                                    'filetype': 'castep',
                                    'realspace': False,
                                    'pretty_print': True}),
                          (['the_file', '-r'],
                           [10], {'filename': 'the_file',
                                  'mode': 'default',
                                  'filetype': False,
                                  'realspace': True,
                                  'pretty_print': True}),
                          ])
def test_kgrid_main(mocker, args, expected_args, expected_kwargs):
    mocked_calc_grid = mocker.patch('kgrid.cli.calc_grid',
                                    return_value=None)

    kgrid.cli.main(params=args)

    mocked_calc_grid.assert_called_with(*expected_args, **expected_kwargs)
