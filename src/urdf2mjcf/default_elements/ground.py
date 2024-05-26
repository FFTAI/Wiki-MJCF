from typing import Dict

from ..core import Element, SubElement
from ..utils import _update_with_defaults


DEFAULT_GROUND_TEXTURE = {
    "name": "texplane",
    "builtin": "checker",
    "height": "512",
    "width": "512",
    "rgb1": ".2 .3 .4",
    "rgb2": ".1 .15 .2",
    "type": "2d",
}
"""TODO: docstring
"""

DEFAULT_GROUND_MATERIAL = {
    "name": "MatPlane",
    "reflectance": "0.5",
    "shininess": "0.01",
    "specular": "0.1",
    "texrepeat": "1 1",
    "texture": "texplane",
    "texuniform": "true",
}
"""TODO: docstring
"""

DEFAULT_GROUND_GEOM = {
    "name": "ground_plane",
    "type": "plane",
    "size": "5 5 10",
    "material": "MatPlane",
    "rgba": "1 1 1 1",
}
"""TODO: docstring
"""


def add_ground(
    mjcf: Element,
    texture_attrib: Dict[str, str] = None,
    material_attrib: Dict[str, str] = None,
    geom_attrib: Dict[str, str] = None,
) -> None:
    """_summary_

    Parameters
    ----------
    mjcf : Element
        _description_
    texture_attrib : Dict[str, str], optional
        _description_, by default None
    material_attrib : Dict[str, str], optional
        _description_, by default None
    geom_attrib : Dict[str, str], optional
        _description_, by default None
    """  # TODO: docstring
    asset = SubElement(mjcf, "asset")

    texture_attrib = _update_with_defaults(DEFAULT_GROUND_TEXTURE, texture_attrib)
    SubElement(asset, "texture", texture_attrib)

    material_attrib = _update_with_defaults(DEFAULT_GROUND_MATERIAL, material_attrib)
    SubElement(asset, "material", material_attrib)

    worldbody = mjcf.find("./worldbody")
    worldbody = SubElement(mjcf, "worldbody") if worldbody is None else worldbody

    geom_attrib = _update_with_defaults(DEFAULT_GROUND_GEOM, geom_attrib)
    SubElement(worldbody, "geom", geom_attrib)
