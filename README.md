# Wiki-MJCF

This repository provides a tool to transfer from URDF file to MJCF.

## User Guide

1. Install the package using pip:

```shell
pip install mujoco
pip install -e .
```

2. Test the package:

```shell
urdf2mjcf --help
```

```
usage: urdf2mjcf [-h] [-s SENSOR_CONFIG] [-m MUJOCO_NODE] [--ground] [--lighting] [--version] [-l] [urdf] [mjcf]

Copyright (c) 2022 Fraunhofer IPA; use option '-l' to print license.

Parse a URDF model into MJCF format

positional arguments:
  urdf              the URDF file to convert (default: <_io.TextIOWrapper name='<stdin>' mode='r' encoding='utf-8'>)
  mjcf              the converted MJCF file (default: <_io.TextIOWrapper name='<stdout>' mode='w' encoding='utf-8'>)

optional arguments:
  -h, --help        show this help message and exit
  -s SENSOR_CONFIG  the XML file of the sensor configuration (default: None)
  -m MUJOCO_NODE    the XML file defining the global MuJoCo configuration (default: None)
  --ground          whether to add the default ground plane to the MuJoCo model (default: False)
  --lighting        whether to add the default lighting to the MuJoCo model (default: False)
  --version         show program's version number and exit
  -l                print license information (default: False)
```

3. Convert a URDF file to MJCF:

```shell
urdf2mjcf /path/to/urdf /path/to/mjcf
```

4. Example: convert GR1T1 robot to MJCF:

```shell
urdf2mjcf /path/to/urdf/gr1t1.urdf /path/to/mjcf/gr1t1.mjcf
```

5. Add the ground plane and lighting to the MJCF file:

```shell
urdf2mjcf /path/to/urdf/gr1t1.urdf /path/to/mjcf/gr1t1.mjcf --ground --lighting
```

6. Change base height of the robot:
    - Edit `<body name="base">` in the MJCF file.
    ```
    <body name="base" pos="0 0 0.95">
    ```


## Thanks

- https://github.com/balandbal/urdf2mjcf