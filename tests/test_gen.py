from genRandSVG import gen


def test_checkNewPoint():
    width = 1280
    height = 1024
    distance = 100
    num_el = 15
    attempts = 30
    g = gen.generator(width, height, distance, num_el, attempts)
    assert (g.checkNewPoint(100, 100))
