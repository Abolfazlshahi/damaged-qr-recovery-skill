from damaged_qr_recovery.rs import gf_div, gf_inverse, gf_mul, gf_pow


def test_gf_inverse():
    for a in [1, 2, 3, 17, 255]:
        assert gf_mul(a, gf_inverse(a)) == 1


def test_gf_div_round_trip():
    for a, b in [(1, 7), (42, 19), (255, 13)]:
        assert gf_mul(gf_div(a, b), b) == a


def test_gf_pow_zero_power():
    for a in [0, 1, 7, 255]:
        assert gf_pow(a, 0) == 1
