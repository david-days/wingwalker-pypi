from wingwalker.models.enums import Planform, WingType, SpecFormat
from wingwalker.models.wing_model import WingRequest

"""
Simple script demonstrating how to write out a wing request as a configuration file.

This is useful in several ways.  First, it allows you to save the initial request, in case it needs to be referenced at a later time
or reran.

Secondly, it can provide a baseline configuration for other requests; the saved file can be copied, edited, and made into an 
assembly of airfoils and control surfaces, to be called later for actual generation.
"""

# Set up request
wing_req: WingRequest = WingRequest()
wing_req.name = 'Test write wing request'
wing_req.planform = Planform.GEOMETRIC
wing_req.wing_type = WingType.LEFT | WingType.ELEVATOR
wing_req.span = 96.0
wing_req.base_chord = 64.0
wing_req.end_chord = 64.0
wing_req.twist = 0.0
wing_req.spec_file = '../../data/selig_symmetrical_n0011sc-il.dat'
wing_req.spec_format = SpecFormat.SELIG
wing_req.iterations = 200
wing_req.notes = '''
- This is an example of multiline notes
- These can be stored in the config and retrieved later 
'''
outfile = f'left_horizontal_stabilizer_.json'

req_settings = wing_req.to_json()

with open(outfile, 'w', encoding='utf-8') as fout:
    fout.write(req_settings)


