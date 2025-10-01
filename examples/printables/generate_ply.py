from enum import Enum

import typer
from typing_extensions import Annotated

from wingwalker.build_params.wing_request import WingRequest
from wingwalker.generators.wing import get_airfoil_specs, get_lambdas, generate_wing, generate_point_cloud_polydata, \
    generate_wing_model
from wingwalker.io.exports import export_ply
from wingwalker.models.enums import SpecFormat, Planform, WingType
from wingwalker.models.wing_model import WingModel

class StructType(str, Enum):
    WING = "wing"
    ELEVATOR = "elevator"
    RUDDER = "rudder"

class StructPosition(str, Enum):
    LEFT = "left"
    RIGHT = "right"

class StructOrientation(str, Enum):
    UNDEFINED = "undefined"
    VERTICAL = "vertical"
    HORIZONTAL = "horizontal"

def main(
        specfile: Annotated[
            str,
            typer.Option(
                help= "Path to the spec file to generate the SVG"
            ),
        ],
        spec_format: Annotated[
            SpecFormat,
            typer.Option(
                help= "Spec format to use"
            )
        ],
        planform: Annotated[
            Planform,
            typer.Option(
                help= "Wing shape to generate"
            )
        ] = Planform.ELLIPSE,
        structure_type: Annotated[
            StructType,
            typer.Option(
                help= "Structure type (wing, elevator, stabilizer)"
            )
        ] = StructType.WING,
        structure_position: Annotated[
            StructPosition,
            typer.Option(
                help= "Position (left or right) of the structure to be generated"
            )
        ] = StructPosition.RIGHT,
        structure_orientation: Annotated[
            StructOrientation,
            typer.Option(
                help= "Orientation for tracking; this does not effect the generation"
            )
        ] = StructOrientation.UNDEFINED,
        twist: Annotated[
            float,
            typer.Option(
                help= "Twist (aerodynamic washout) from root to tip."
            )
        ] = 0.0,
        span: Annotated[
            float,
            typer.Option(
                help= "Span of the structure from root to tip"
            )
        ] = 256.0,
        base: Annotated[
            float,
            typer.Option(
                help= "chord length at the root"
            )
        ] = 96.0,
        end: Annotated[
            float,
            typer.Option(
                help= "Chord length at the tip. Ignored for ELLIPSE and RECTANGULAR planforms"
            )
        ] = 48.0,
        iterations: Annotated[
            int,
            typer.Option(
                help= "Number of iterations to run from the root to the tip."
            )
        ] = 100
    ):
    """
    Generates a wing model and exports it as a PLY file, fit to be processed by MeshLab (or equivalent).  From that process,
     a printable STL file should be exported and either printed directly or further manipulated  by a 3rd party tool like Blender
    """
    wing_type: WingType = WingType.UNDEFINED

    match structure_type:
        case WingType.WING:
            wing_type |= WingType.WING
        case WingType.ELEVATOR:
            wing_type |= WingType.ELEVATOR
        case WingType.RUDDER:
            wing_type |= WingType.RUDDER

    match structure_position:
        case StructPosition.LEFT:
            wing_type |= WingType.LEFT
        case StructPosition.RIGHT:
            wing_type |= WingType.RIGHT

    match structure_orientation:
        case StructOrientation.VERTICAL:
            wing_type |= WingType.VERTICAL
        case StructOrientation.HORIZONTAL:
            wing_type |= WingType.HORIZONTAL

    req: WingRequest = WingRequest()
    req.planform = planform
    req.wing_type = wing_type
    req.span = span
    req.base_chord = base
    req.end_chord = end
    req.twist = twist
    req.spec_file = specfile
    req.spec_format = spec_format
    req.iterations = iterations

    print()

    model: WingModel = generate_wing_model(wing_req=req)
    export_name = f'wing_pointcloud_{structure_type}_{structure_position}_{structure_orientation}.ply'
    export_ply(model, export_name)


if __name__ == "__main__":
    typer.run(main)