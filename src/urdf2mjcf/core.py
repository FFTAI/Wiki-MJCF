""" TODO: add module description """

# Copyright (c) 2022 Fraunhofer IPA; see bottom of this file for full license

from xml.etree.ElementTree import Element, tostring, SubElement
from pathlib import Path
from typing import Union, IO, AnyStr, Dict
from os import fdopen, unlink
from tempfile import mkstemp
from urllib.parse import urlparse

from defusedxml.ElementTree import parse
from mujoco import MjModel, mj_saveLastXML
from rospkg import RosPack


def _parse_element(source: Union[str, Path, IO[AnyStr], None], **kwargs) -> Element:
    """Parse source into a Python XML element object, safely"""
    return None if source is None else parse(source, **kwargs).getroot()  # type: ignore


def pass_through_mujoco(model_xml: Element) -> Element:
    """Load and export XML element object through MuJoCo"""
    parsed_model = MjModel.from_xml_string(tostring(model_xml, encoding="unicode"))

    tmp_file_descriptor, tmp_file_name = mkstemp(prefix="tmp_mjcf_", suffix=".xml")
    mj_saveLastXML(tmp_file_name, parsed_model)

    with fdopen(tmp_file_descriptor, "r") as tmp_file:
        backloaded_model_xml = _parse_element(tmp_file)

    unlink(tmp_file_name)

    return backloaded_model_xml


def add_mujoco_node(urdf: Element, mujoco_node: Element = None) -> None:
    """Add the mujoco node to a URDF object"""
    mujoco_node = Element("mujoco") if mujoco_node is None else mujoco_node
    present_mujoco_node = urdf.find("./mujoco")
    if present_mujoco_node is None:
        present_mujoco_node = Element("mujoco")
    else:
        urdf.remove(present_mujoco_node)

    compiler_attrib = {
        "strippath": "false",
        "fusestatic": "false",
        "discardvisual": "true",
    }
    lengthrange_attrib: Dict[str, str] = {}
    option_attrib: Dict[str, str] = {}
    flag_attrib: Dict[str, str] = {}
    size_attrib: Dict[str, str] = {}

    attribs = [
        compiler_attrib,
        lengthrange_attrib,
        option_attrib,
        flag_attrib,
        size_attrib,
    ]
    mujoco_node_scheme = [
        "./compiler",
        "./compiler/lengthrange",
        "./option",
        "./option/flag",
        "./size",
    ]

    for node_attrib, xpath in zip(attribs, mujoco_node_scheme):
        for node in present_mujoco_node.findall(xpath):
            node_attrib.update(node.attrib)
        for node in mujoco_node.findall(xpath):
            node_attrib.update(node.attrib)

    new_mujoco_node = SubElement(urdf, "mujoco")

    compiler_node = SubElement(new_mujoco_node, "compiler", compiler_attrib)
    lengthrange_node = SubElement(compiler_node, "lengthrange", lengthrange_attrib)

    option_node = SubElement(new_mujoco_node, "option", option_attrib)
    flag_node = SubElement(option_node, "flag", flag_attrib)

    size_node = SubElement(new_mujoco_node, "size", size_attrib)


def abspath_from_ros_uri(uri: str, rospack: RosPack = None) -> str:
    """Parse a ROS package URI into an absolute path"""
    rospack = RosPack() if rospack is None else rospack

    scheme, netloc, path, *_ = urlparse(uri)

    assert scheme == "package", f"Got URI that is not of scheme 'package': {scheme}"

    package = Path(rospack.get_path(netloc))
    relative_path = Path(path if path[0] != "/" else path[1:])

    assert (
        not relative_path.is_absolute()
    ), f"Asset path is not relative: {relative_path}"

    assert (
            package / relative_path
    ).is_absolute(), f"Resolved path is not absolute: {package / relative_path}"

    return str(package / relative_path)


def resolve_ros_uris(urdf: Element, rospack: RosPack = None) -> None:
    """Resolve all collision mesh ROS package URIs to absolute paths"""
    for mesh_node in urdf.findall(".//collision/*/mesh[@filename]"):
        ros_uri = mesh_node.get("filename", None)
        assert (
                ros_uri is not None
        ), f"Mesh node without filename: '{mesh_node.tag}' : {mesh_node.attrib}"

        absolute_path = abspath_from_ros_uri(ros_uri, rospack)

        mesh_node.set("filename", absolute_path)


def resolve_uris(urdf: Element, base_path: str = None) -> None:
    """Resolve all collision mesh URIs to absolute paths"""
    for mesh_node in urdf.findall(".//collision/*/mesh[@filename]"):
        uri = mesh_node.get("filename", None)
        assert (
                uri is not None
        ), f"Mesh node without filename: '{mesh_node.tag}' : {mesh_node.attrib}"

        absolute_path = base_path + uri if base_path is not None else uri

        mesh_node.set("filename", str(absolute_path))


def populate_sensors(mjcf: Element, sensor_config: Element) -> None:
    """Add sites and sensors to an MJCF object"""
    for body_node in sensor_config.findall("./body"):
        body_name = body_node.get("name", None)
        assert (
                body_name is not None
        ), f"Bad sensor configuration; body node has no name ({body_node.attrib})"

        body_in_mjcf = mjcf.find(f".//body[@name='{body_name}']")
        assert body_in_mjcf is not None, f"No body in MJCF with name '{body_name}'"

        body_in_mjcf.extend(body_node.findall("./site"))

    mjcf.extend(sensor_config.findall("./sensor"))

# Copyright (c) 2022 Fraunhofer IPA
#
# Redistribution and use in source and binary forms, with or without modification, are permitted
# provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this list of conditions
#    and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions
#    and the following disclaimer in the documentation and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse
#    or promote products derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED
# WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
# PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR
# TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
# ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
