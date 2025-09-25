import wingwalker.lednicer as lednicer


def test_lednicer_parsing():
    parser = lednicer.Parser('data/lednicerdatfile.txt')
    xs, ys, found_airfoil = parser.read(1.0)
    assert found_airfoil == 'NASA SC(2)-1010 AIRFOIL'
    assert len(xs) == 206
    assert len(ys) == 206
