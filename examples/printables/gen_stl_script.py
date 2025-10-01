"""
Simple script to load up a config file (a wing request on disk), create a wing model, and then
process it to generate an STL file that can be used for further processing or printing.

"""
import os

from wingwalker.build_params.wing_request import WingRequest
from wingwalker.generators.wing import get_airfoil_specs, get_lambdas, generate_wing
from wingwalker.io.exports import export_stl

config_file = 'elliptical_left_wing_256mm.json'

# Read the values from the file
wing_req: WingRequest
with open(config_file, 'r', encoding='utf-8') as fin:
    json_str = fin.read()
    wing_req = WingRequest.from_json(json_str)

# Retrieve the specs from the request path
af_specs = get_airfoil_specs(wing_req)

# Get lambdas (dimension functions for the given parameters)
c_func, t_func, z_func, area_func = get_lambdas(wing_req)

# Generate the actual wing model
model = generate_wing(wing_req, af_specs, c_func, t_func, z_func, area_func)

f_name = f'{wing_req.name}_geometric_wing.stl'
if os.path.exists(f_name):
    os.remove(f_name)

export_stl(model, f_name)

print('Aircraft wing STL file generated.')

print(model.__repr__())

