import importlib.util
import os
import pytest

def load_module():
    spec = importlib.util.spec_from_file_location("tribonacci_constant", "MODULE_FILENAME")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def test_tribonacci_constant_digits():
    module = load_module()
    digits = module.compute_tribonacci_constant_hpc(100)
    assert len(digits) == 100
    # Tribonacci constant is 1.839286755214161132551852564653...
    expected_prefix = "183928675521416113255185256465"
    assert digits.startswith(expected_prefix)

    raw_file = "Tribonacci_Constant_100_digits.txt"
    b_file = "b_file_Tribonacci_Constant_100.txt"
    assert os.path.exists(raw_file)
    assert os.path.exists(b_file)

    os.remove(raw_file)
    os.remove(b_file)