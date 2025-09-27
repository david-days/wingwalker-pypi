import wingwalker as ww
import pytest
import os
from tests.setup.config_dirs import dir_setup

def verify_exists(svg_path):
    assert os.path.exists(svg_path), f"{svg_path} does not exist"


@pytest.mark.svg
@pytest.mark.parametrize('do_trace', [True, False])
@pytest.mark.parametrize('do_fill', [ True, False])
@pytest.mark.parametrize('do_poly', [ True, False])
@pytest.mark.parametrize('do_mirror', [ True, False])
@pytest.mark.parametrize('selig_file,base_file', [
    ('data/seligdatfile.txt', 'selig_data_output'),
    ('data/selig_supercritical_nasa-sc2-1010.dat', 'selig_sc1010_output'),
    ('data/selig_symmetrical_n0011sc-il.dat', 'selig_n0011sc_output')
])
def test_selig_svg(
        selig_file: str,
        base_file:str,
        do_trace: bool,
        do_fill: bool,
        do_poly: bool,
        do_mirror: bool,
        write_dir='out/selig/svg_test'):
    """
    Run the SVG generation process according to the combination of parameters
    Args:
        selig_file: path to selig-formatted airfoil data
        base_file: output base file path and name
        do_trace: create a trace (_shape.svg)
        do_fill: create a filled image (_fill.svg)
        do_poly: create a polygon structure in the svg (_poly.svg)
        do_mirror: create a mirror of each of the other types of svg (_{type}_mirror.svg)
        write_dir: output file directory

    Returns:
        None

    """
    dir_setup(write_dir)
    selig_base = f'{write_dir}{os.path.sep}{base_file}_{do_trace}_{do_fill}_{do_poly}_{do_mirror}'
    chord = 256
    c_units = 'mm'
    ww.svg.main(
        infile=selig_file,
        outbase=selig_base,
        c_len=chord,
        units=c_units,
        lednicer=False,
        trace=do_trace,
        fill=do_fill,
        poly=do_poly,
        mirror=do_mirror
    )
    if do_trace:
        verify_exists(f"{selig_base}_shape.svg")
        if do_mirror:
            verify_exists(f"{selig_base}_shape_mirror.svg")

    if do_fill:
        verify_exists(f"{selig_base}_filled.svg")
        if do_mirror:
            verify_exists(f"{selig_base}_filled_mirror.svg")

    if do_poly:
        verify_exists(f"{selig_base}_poly.svg")
        if do_mirror:
            verify_exists(f"{selig_base}_poly_mirror.svg")



@pytest.mark.svg
@pytest.mark.parametrize('do_trace', [True, False])
@pytest.mark.parametrize('do_fill', [ True, False])
@pytest.mark.parametrize('do_poly', [ True, False])
@pytest.mark.parametrize('do_mirror', [ True, False])
@pytest.mark.parametrize('lednicer_file,base_file', [
    ('data/lednicerdatfile.txt', 'lednicer_data_output'),
    ('data/lednicer_supercritical_nasa-sc2-1010.dat', 'lednicer_sc1010_output'),
    ('data/lednicer_symmetrical_n0011sc-il.dat', 'lednicer_n0011sc_output')
])
def test_lednicer_svg(
        lednicer_file: str,
        base_file: str,
        do_trace: bool,
        do_fill: bool,
        do_poly: bool,
        do_mirror: bool,
        write_dir='out/selig/svg_test'):
    """
    Run the SVG generation process according to the combination of parameters
    Args:
        lednicer_file: path to lednicer-formatted airfoil data
        base_file: output base file path and name
        do_trace: create a trace (_shape.svg)
        do_fill: create a filled image (_fill.svg)
        do_poly: create a polygon structure in the svg (_poly.svg)
        do_mirror: create a mirror of each of the other types of svg (_{type}_mirror.svg)
        write_dir: output file directory

    Returns:
        None

    """
    dir_setup(write_dir)
    lednicer_base = f'{write_dir}{os.path.sep}{base_file}_{do_trace}_{do_fill}_{do_poly}_{do_mirror}'
    chord = 256
    c_units = 'mm'
    ww.svg.main(
        infile=lednicer_file,
        outbase=lednicer_base,
        c_len=chord,
        units=c_units,
        lednicer=True,
        trace=do_trace,
        fill=do_fill,
        poly=do_poly,
        mirror=do_mirror
    )
    if do_trace:
        verify_exists(f"{lednicer_base}_shape.svg")
        if do_mirror:
            verify_exists(f"{lednicer_base}_shape_mirror.svg")

    if do_fill:
        verify_exists(f"{lednicer_base}_filled.svg")
        if do_mirror:
            verify_exists(f"{lednicer_base}_filled_mirror.svg")

    if do_poly:
        verify_exists(f"{lednicer_base}_poly.svg")
        if do_mirror:
            verify_exists(f"{lednicer_base}_poly_mirror.svg")
