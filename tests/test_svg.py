import wingwalker as ww
import pytest
import os
from tests.setup.config_tests import dir_setup

def verify_exists(svg_path):
    assert(os.path.exists(svg_path), f"{svg_path} does not exist")


@pytest.mark.svg
def test_selig_svg(dir_setup):
    selig_file = 'data/seligdatfile.txt'
    base_file = 'out/test_selig_svg'
    chord = 256
    c_units = 'mm'
    ww.svg.main(
        infile=selig_file,
        outbase=base_file,
        c_len=chord,
        units=c_units,
        lednicer=False,
        trace=True,
        fill=True,
        poly=True,
        mirror=True
    )
    verify_exists(f"{base_file}_filled.svg")
    verify_exists(f"{base_file}_poly.svg")
    verify_exists(f"{base_file}_shape.svg")
    verify_exists(f"{base_file}_poly_mirror.svg")
    verify_exists(f"{base_file}_filled_mirror.svg")
    verify_exists(f"{base_file}_shape_mirror.svg")

@pytest.mark.svg
def test_lednicer_svg(dir_setup):
    selig_file = 'data/lednicerdatfile.txt'
    base_file = 'out/test_lednicer_svg'
    chord = 256
    c_units = 'mm'
    ww.svg.main(
        infile=selig_file,
        outbase=base_file,
        c_len=chord,
        units=c_units,
        lednicer=True,
        trace=True,
        fill=True,
        poly=True,
        mirror=True
    )
    verify_exists(f"{base_file}_filled.svg")
    verify_exists(f"{base_file}_poly.svg")
    verify_exists(f"{base_file}_shape.svg")
    verify_exists(f"{base_file}_poly_mirror.svg")
    verify_exists(f"{base_file}_filled_mirror.svg")
    verify_exists(f"{base_file}_filled_mirror.svg")
    verify_exists(f"{base_file}_shape_mirror.svg")