"""
Module wingwalker.processing handles intermediate and final processing stages to apply cleanup, filtering, and other
post point cloud operations.

The focus of these operators is to produce a final digital model of the airfoils, parts, and connectors that will ultimately be
sent to a design library (such as Blender) and then/or directly to a 3D printer.

The goal is a quality model that requires little to no adjustment before the final and print stages.
"""