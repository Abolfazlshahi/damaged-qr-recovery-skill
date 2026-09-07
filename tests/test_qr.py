from damaged_qr_recovery.qr import mask_bit, size_from_version, version_from_size


def test_version_round_trip():
    for version in [1, 2, 4, 7, 40]:
        assert version_from_size(size_from_version(version)) == version


def test_mask_patterns_are_binary():
    for mask in range(8):
        for row, col in [(0, 0), (1, 2), (12, 17)]:
            assert mask_bit(mask, row, col) in (0, 1)
