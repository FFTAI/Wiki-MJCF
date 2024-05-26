from typing import Dict

from ..core import Element, SubElement
from ..utils import _update_with_defaults

DEFAULT_LIGHT = {
    "pos": "0 0 1000",
    "castshadow": "true",
}
"""TODO: docstring
"""


def add_lighting(mjcf: Element, light_attrib: Dict[str, str] = None) -> None:
    """_summary_

    Parameters
    ----------
    mjcf : Element
        _description_
    light_attrib : Dict[str, str]
        _description_
    """  # TODO: docstring
    worldbody = mjcf.find("./worldbody")
    worldbody = SubElement(mjcf, "worldbody") if worldbody is None else worldbody

    light_attrib = _update_with_defaults(DEFAULT_LIGHT, light_attrib)
    SubElement(worldbody, "light", light_attrib)
