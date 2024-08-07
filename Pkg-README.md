# Wingwalker Python Module

This Python module provides core functions and scripts to create useful airfoil models
and files from engineering specifications.  These base models can then be used to 
create useful designs and implementations (VR and 3D models, 3D printer components, etc).

## Philosophy

Wing selection and design can be very complex.  From the choice of starting
airfoil specs (custom or existing), to cost analysis, and finally to construction, the spectrum of
both choices and pitfalls at each stage can become overwhelming pretty quickly, especially to 
someone whose primary interest is what comes _after_ the wings are bolted on. 

The goal behind this software is very straightforward:  To give everyone, from 
the basic hobbyist to the serious (semi)professional, the ability to go quickly from theory and
specs to design to real- or virtual-world production of airfoils and wings.

## Installation

```bash
$ pip install wingwalker
```

## Usage

The wingwalker modules can be used directly and help cut back on multiple custom steps.

For example, to read in an airfoil data file, start with the follwoing code snippet:

```python
import wingwalker as ww

# Arrays to hold coordinates
xs, ys = []
# File format
dat_format="selig"
# Chord (x-axis) length (in mm, in this case)
c_len=128.0 
# Input file
infile='/path/to/selig/file'
with open(infile, 'rb') as stream:
        spec_name = ww.utils.parse_specs(stream, xs, ys, c_len, dat_format)
        # spec_name, xs, and ys now have the info from the input file

```

## License

This software is distributed freely under the MIT license.  You are free to use, abuse, modify, 
or ridicule the software, its products, and its processes in any way you see fit.

Output generated by the original software is published under the Create Commons license, and may
also be used for any purpose, commercial or not.  Users of this software may freely apply or replace the CC 
license with their own license or restrictions, as they desire.

## Credits

`wingwalker` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
