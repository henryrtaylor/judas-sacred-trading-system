from phase15_cap_sym.position_engine import calculate_position_size

def test_position_size_basic():
    assert calculate_position_size(100_000, 0.01, 2) == 500
