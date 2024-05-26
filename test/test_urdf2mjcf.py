import sys
from pathlib import Path

from urdf2mjcf.core import _parse_element, tostring
from urdf2mjcf.app import full_pipeline as urdf_to_mjcf

_test_dir = Path(__file__).resolve().parent
sys.path.append(str(_test_dir))


def _urdf():
    return _parse_element(_test_dir / "inputs" / "panda.urdf")


def _sensor_config():
    return _parse_element(_test_dir / "inputs" / "sensors.xml")


def _mujoco_node():
    return _parse_element(_test_dir / "inputs" / "mujoco.xml")


def _remove_assets(mjcf):
    for asset_element in mjcf.findall("./asset"):
        mjcf.remove(asset_element)


def test_urdf2mjcf_mjnode():
    result_object = urdf_to_mjcf(_urdf(), mujoco_node=_mujoco_node())
    _remove_assets(result_object)
    result_string = tostring(result_object, encoding="unicode")

    control_object = _parse_element(_test_dir / "outputs" / "panda_mjnoded.xml")
    _remove_assets(control_object)
    control_string = tostring(control_object, encoding="unicode")

    assert result_string == control_string


def test_urdf2mjcf_sensored():
    result_object = urdf_to_mjcf(_urdf(), sensor_config=_sensor_config())
    _remove_assets(result_object)
    result_string = tostring(result_object, encoding="unicode")

    control_object = _parse_element(_test_dir / "outputs" / "panda_sensored.xml")
    _remove_assets(control_object)
    control_string = tostring(control_object, encoding="unicode")

    assert result_string == control_string
