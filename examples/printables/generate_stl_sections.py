"""
Simple script to load up a config file (a wing request on disk), create wing sections, and then
process these sections to generate STL files that can be used for further processing or printing.

"""
import os

from wingwalker.build_params.wing_request import WingRequest
from wingwalker.generators.wing import get_airfoil_specs, get_lambdas, generate_wing, get_section_lambdas, \
    generate_wing_subsection
from wingwalker.io.exports import export_stl

config_file = 'elliptical_left_wing_256mm.json'

# Read the values from the file
wing_req: WingRequest
with open(config_file, 'r', encoding='utf-8') as fin:
    json_str = fin.read()
    wing_req = WingRequest.from_json(json_str)

# Retrieve the specs from the request path
af_specs = get_airfoil_specs(wing_req)

for i in range(0, len(wing_req.sections)):
    # Generate the actual wing model
    model = generate_wing_subsection(wing_req, i)

    f_name = f'{wing_req.name}_section-{i}.stl'
    if os.path.exists(f_name):
        os.remove(f_name)

    export_stl(model, f_name)
    print('Aircraft wing STL file generated.')
    print(model.__repr__())

print()
print('Done.')

