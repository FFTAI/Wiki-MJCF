from .core import Element, RosPack
from .core import (
    resolve_ros_uris,
    add_mujoco_node,
    pass_through_mujoco,
    populate_sensors,
)
from .default_elements.ground import add_ground
from .default_elements.lighting import add_lighting


def full_pipeline(
    urdf: Element,
    rospack: RosPack = None,
    sensor_config: Element = None,
    mujoco_node: Element = None,
    default_ground: bool = False,
    default_lighting: bool = False,
) -> Element:
    """Convert URDF object to MJCF"""
    resolve_ros_uris(urdf, rospack)
    add_mujoco_node(urdf, mujoco_node)

    mjcf = pass_through_mujoco(urdf)

    if sensor_config is not None:
        populate_sensors(mjcf, sensor_config)
        mjcf = pass_through_mujoco(mjcf)

    if default_ground:
        add_ground(mjcf)
    if default_lighting:
        add_lighting(mjcf)

    return mjcf
