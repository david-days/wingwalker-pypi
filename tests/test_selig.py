import wingwalker.selig as selig


def test_selig_parsing():
    parser = selig.Parser('data/seligdatfile.txt')
    xs, ys, found_airfoil = parser.read(1.0)
    assert found_airfoil == 'NASA SC(2)-1010 AIRFOIL'
    assert len(xs) == 205
    assert len(xs) == 205
