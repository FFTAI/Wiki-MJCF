import sys
from pathlib import Path

from urdf2mjcf.core import pass_through_mujoco

_test_dir = Path(__file__).resolve().parent
sys.path.append(str(_test_dir))

from utils import pass_through as _pass_through


def test_basic_mjcf2mjcf():
    input_model = _test_dir / "inputs" / "ip_model_1.xml"
    output_model = _test_dir / "outputs" / "op_model_1.xml"

    result = _pass_through(input_model, pass_through_mujoco)

    with open(output_model, "r") as file:
        control = file.read()

    assert result == control


def test_basic_urdf2mjcf():
    input_model = _test_dir / "inputs" / "ip_model_2.urdf"
    output_model = _test_dir / "outputs" / "op_model_2.xml"

    result = _pass_through(input_model, pass_through_mujoco)

    with open(output_model, "r") as file:
        control = file.read()

    assert result == control
