import click
import matplotlib.collections
import matplotlib.pyplot as plt

from .decorators import global_processor
from .model import VectorData, as_vector
from .vpype import cli

COLORS = [
    (0, 0, 1),
    (0, 0.5, 0),
    (1, 0, 0),
    (0, 0.75, 0.75),
    (0, 1, 0),
    (0.75, 0, 0.75),
    (0.75, 0.75, 0),
    (0, 0, 0),
]


@cli.command(group="Output")
@click.option("-a", "--show-axes", is_flag=True, help="Display axes.")
@click.option("-g", "--show-grid", is_flag=True, help="Display grid (implies -a).")
@click.option(
    "-c", "--colorful", is_flag=True, help="Display each segment in a different color."
)
@global_processor
def show(vector_data: VectorData, show_axes: bool, show_grid: bool, colorful: bool):
    """
    Display the geometry using matplotlib.

    By default, only the geometries are displayed without the axis. All geometries are
    displayed with black. When using the `--colorful` flag, each segment will have a different
    color (default matplotlib behaviour). This can be useful for debugging purposes.
    """

    plt.figure()
    color_idx = 0
    for lc in vector_data.layers.values():
        if colorful:
            color = COLORS[color_idx:] + COLORS[:color_idx]
            color_idx += len(lc)
        else:
            color = COLORS[color_idx]
            color_idx += 1
        if color_idx >= len(COLORS):
            color_idx = color_idx % len(COLORS)

        plt.gca().add_collection(
            matplotlib.collections.LineCollection(
                (as_vector(line) for line in lc), color=color, lw=0.5,
            )
        )

    plt.gca().invert_yaxis()
    plt.axis("equal")
    if show_axes or show_grid:
        plt.axis("on")
    else:
        plt.axis("off")
    if show_grid:
        plt.grid("on")
    plt.show()

    return vector_data
