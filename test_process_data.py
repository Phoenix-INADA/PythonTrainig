from main import NumberStack, process_data


def test_process_data():
    stack = NumberStack([10, 20, 30])
    assert process_data(100, *stack, multiplier=2, calc=lambda a, b: a + b) == 220
