import typer
from typing_extensions import Annotated

import wingwalker as ww
from wingwalker import utils
from wingwalker.models.enums import SpecFormat
from wingwalker.svg import SvgWriter


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
        output_base: Annotated[
            str,
            typer.Option(
                help="Base path and name for the SVG output file(s)"
            ),
        ] = "airfoil_svg",
        chord:  Annotated[
            float,
            typer.Option(
                help="Length of the airfoil chord in the SVG image"
            ),
        ]  = 128.0,
        units:  Annotated[
            str,
            typer.Option(
                help="Units of the SVG"
            ),
        ]  = 'mm',
        trace:  Annotated[
            bool,
            typer.Option(
                help="Flag indicating whether to generate trace images"
            ),
        ] = False,
        fill: Annotated[
            bool,
            typer.Option(
                help="Flag indicating whether to generate filled images"
            ),
        ] = False,
        poly: Annotated[
            bool,
            typer.Option(
                help="Flag indicating whether to generate polygon images"
            ),
        ] = False,
        mirrored: Annotated[
            bool,
            typer.Option(
                help="Flag indicating whether to generate mirrors of each image type"
            ),
        ] = False
    )->None:
    """
    Example function to generate SVGs of according to the inputs
    """
    x = []
    y = []
    img_count = 0
    print()
    with open(specfile, 'rb') as f:
        spec_name = utils.parse_specs(f, x, y, chord, spec_format)
        print(spec_name)
        print('\tFormat:  %s' % spec_format)
        print('\tChord length:  %f %s' % (chord, units))
        print('\tTotal Coordinates:  %i' % len(x))
        print('\tTrace:  %s' % str(trace))
        print('\tFill:  %s' % str(fill))
        print('\tPoly:  %s' % str(poly))
        print('\tMirror:  %s' % str(mirrored))
        if trace or fill or poly:
            svg_writer = SvgWriter(x, y, chord, units)
            if trace:
                svg_writer.generate_trace(output_base + '_shape', mirror=mirrored, filled=False, l_width=1.0)
                img_count += (1 if not mirrored else 2)
            if fill:
                svg_writer.generate_trace(output_base + '_filled', mirror=mirrored, filled=True, l_width=0.75)
                img_count += (1 if not mirrored else 2)
            if poly:
                svg_writer.generate_poly(output_base + '_poly', mirror=mirrored)
                img_count += (1 if not mirrored else 2)
    print()
    print(f' {img_count} image{"s" if img_count > 1 else ""} generated')


if __name__ == "__main__":
    typer.run(main)