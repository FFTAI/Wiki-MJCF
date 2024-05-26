from sys import stdin, stdout
from argparse import (
    ArgumentParser,
    ArgumentDefaultsHelpFormatter,
    RawDescriptionHelpFormatter,
    FileType,
)


class ArgFormatter(ArgumentDefaultsHelpFormatter, RawDescriptionHelpFormatter):
    pass


def cli(parser: ArgumentParser = None):
    """CLI for URDF-2-MJCF conversion"""
    parser = (
        ArgumentParser(
            prog="urdf2mjcf",
            description="""Copyright (c) 2022 Fraunhofer IPA; use option '-l' to print license.

Parse a URDF model into MJCF format""",
            formatter_class=ArgFormatter,
        )
        if parser is None
        else parser
    )

    parser.add_argument(
        "urdf",
        nargs="?",
        type=FileType("r"),
        default=stdin,
        help="the URDF file to convert",
    )
    parser.add_argument(
        "mjcf",
        nargs="?",
        type=FileType("w"),
        default=stdout,
        help="the converted MJCF file",
    )
    parser.add_argument(
        "-s",
        dest="sensor_config",
        type=FileType("r"),
        default=None,
        help="the XML file of the sensor configuration",
    )
    parser.add_argument(
        "-m",
        dest="mujoco_node",
        type=FileType("r"),
        default=None,
        help="the XML file defining the global MuJoCo configuration",
    )
    parser.add_argument(
        "--ground",
        dest="default_ground",
        action="store_true",
        help="whether to add the default ground plane to the MuJoCo model",
    )
    parser.add_argument(
        "--lighting",
        dest="default_lighting",
        action="store_true",
        help="whether to add the default lighting to the MuJoCo model",
    )
    return parser
