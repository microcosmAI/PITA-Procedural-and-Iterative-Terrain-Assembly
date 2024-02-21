import logging
import matplotlib.pyplot as plt
from typing import Any, Union
from matplotlib import patches
from math import sqrt, ceil, trunc


class LayoutManager:
    """Sets a layout for Area-sites if multiple areas are present."""

    def __init__(self, length: float, height: float, number: float, plot: bool):
        """Constructor of the LayoutManager class.

        Parameters:
            length (float): Length of the environment
            height (float): Height of the environment
            number (float): Number of areas to split the environment into
            plot (bool): Whether to plot the created layout as bird view 2D map
        """
        self.length: float = length
        self.height: float = height
        self.number: float = number
        self.plot: bool = plot

    def tiling(self, length: float, height: float, number: float) -> dict:
        """Calculate the tiling layout based on environment dimensions and number of areas.

        Parameters:
            length (float): Length of the environment
            height (float): Height of the environment
            number (float): Number of areas to split the environment into

        Returns:
            (dict): A dictionary containing information about the tiling layout
        """
        area = length * height

        # How many tiles would fit along both dimensions if they were perfectly square?
        real_num_tiles_length = sqrt(number * length / height)
        real_num_tiles_height = sqrt(number * height / length)

        # What's the area of the area of each tile?
        square_area = area / number

        # What are the upper and lower bound of the number of columns and rows?
        n_rows_trunc = trunc(real_num_tiles_height)
        n_rows_ceil = ceil(real_num_tiles_height)
        n_cols_trunc = trunc(real_num_tiles_length)
        n_cols_ceil = ceil(real_num_tiles_length)

        # What are the maximum divergences for the resulting tiling dimensions from a square?
        # The first half assumes longer and shorter rows
        rows_trunc = self._max_div(length, height, number, square_area, n_rows_trunc)
        rows_ceil = self._max_div(length, height, number, square_area, n_rows_ceil)
        # The second half assumes longer and shorter columns. To efficiently reuse the self._max_div function
        # the height and length arguments are swapped on call.
        cols_trunc = self._max_div(height, length, number, square_area, n_cols_trunc)
        cols_ceil = self._max_div(height, length, number, square_area, n_cols_ceil)

        # What is the minimum divergence possible?
        min_max_div = min(rows_trunc, rows_ceil, cols_trunc, cols_ceil)

        # What are the resulting tilings for the mode (rows or cols) and the number of tiles that
        # resulted in the lowest divergence from square tiles?

        # First half assumes that the tiling is fitted with longer and shorter rows
        if rows_trunc == min_max_div:
            tiling = self._solve(length, height, number, square_area, n_rows_trunc)
            tiling["mode"] = "rows"
        elif rows_ceil == min_max_div:
            tiling = self._solve(length, height, number, square_area, n_rows_ceil)
            tiling["mode"] = "rows"
        # The second half assumes that the tiling is fitted with longer and shorter collumns.
        # To reuse the self._solve function we swap length and height arguments in the call and swap
        # the resulting tiling back using the _swap function.
        elif cols_trunc == min_max_div:
            tiling = self._solve(height, length, number, square_area, n_cols_trunc)
            tiling["mode"] = "cols"
            tiling = self._swap(tiling)
        elif cols_ceil == min_max_div:
            tiling = self._solve(height, length, number, square_area, n_cols_ceil)
            tiling["mode"] = "cols"
            tiling = self._swap(tiling)
        else:
            logger = logging.getLogger()
            logger.error("Arithmetic error while trying to solve layout.")
            raise ArithmeticError
        return tiling

    def _max_div(
        self,
        length: float,
        height: float,
        number: float,
        square_area: float,
        n_rows: int,
    ) -> float:
        """Calculate the maximal divergence from a square tiling.

        Parameters:
            length (float): Length of the environment
            height (float): Height of the environment
            number (float): Number of areas to split the environment into
            square_area (float): Area of each tile in a perfectly square tiling
            n_rows (int): Number of rows to be constructed in the tiling

        Returns:
            (float): The maximal divergence from a square tiling
        """
        # What is the maximal divergence from a square given the area dimensions, the number of tiles
        # and the number of rows to be constructed.
        if n_rows < 1 or n_rows > number:
            return float("inf")

        # How many cols are to be placed in the longer and shorter rows?
        n_cols_long = ceil(number / n_rows)
        n_cols_short = trunc(number / n_rows)

        # How long are the tiles in the short and long rows?
        length_long = length / n_cols_long
        length_short = length / n_cols_short

        # How high are the tiles in the short and long rows?
        height_long = square_area / length_long
        height_short = square_area / length_short

        # What is the difference between the heights and lengths in the short and long rows? Ideally this should be zero, as in a perfect square.
        delta_long = length_long - height_long
        delta_short = length_short - height_short

        # What is the maximum difference between the heights and lengths?
        return max(abs(delta_long), abs(delta_short))

    def _solve(
        self,
        length: float,
        height: float,
        number: float,
        square_area: float,
        n_rows: int,
    ) -> dict:
        """Solve the tiling layout based on given parameters.

        Parameters:
            length (float): Length of the environment
            height (float): Height of the environment
            number (float): Number of areas to split the environment into
            square_area (float): Area of each tile in a perfectly square tiling
            n_rows (int): Number of rows to be constructed in the tiling

        Returns:
            (dict): A dictionary containing information about the solved tiling layout
        """
        # What are the number of cols in the short and long rows?
        n_cols_long = ceil(number / n_rows)
        n_cols_short = trunc(number / n_rows)

        # What are the number of long and short rows such that all tiles fit?
        n_rows_long = number % n_rows
        n_rows_short = n_rows - n_rows_long

        # What are the lengths and heights of the short and long rows?
        long_length = length / n_cols_long
        long_height = square_area / long_length
        short_length = length / n_cols_short
        short_height = square_area / short_length

        # Collect all the parameters for the tiling in one dictionary
        tiling = {
            "short": {
                "n_rows": n_rows_short,
                "n_cols": n_cols_short,
                "tile_length": short_length,
                "tile_height": short_height,
            },
            "long": {
                "n_rows": n_rows_long,
                "n_cols": n_cols_long,
                "tile_length": long_length,
                "tile_height": long_height,
            },
        }
        # Sanity check
        assert number == n_cols_long * n_rows_long + n_cols_short * n_rows_short
        return tiling

    @staticmethod
    def _swap(tiling: dict) -> dict:
        """Swap the rows and columns of the tiling layout.

        Parameters:
            tiling (dict): A dictionary containing information about the tiling layout.

        Returns:
            (dict): A dictionary with swapped rows and columns
        """
        # Swap rows and cols length and height
        tiling_short = tiling["short"]
        tiling_long = tiling["long"]

        # Should be pretty self explainatory
        tiling["short"] = {
            "n_rows": tiling_short["n_cols"],
            "n_cols": tiling_short["n_rows"],
            "tile_length": tiling_short["tile_height"],
            "tile_height": tiling_short["tile_length"],
        }
        tiling["long"] = {
            "n_rows": tiling_long["n_cols"],
            "n_cols": tiling_long["n_rows"],
            "tile_length": tiling_long["tile_height"],
            "tile_height": tiling_long["tile_length"],
        }
        return tiling

    def generate_layout_boundaries(
        self,
    ) -> list[
        tuple[
            tuple[Union[int, Any], Union[int, Any]],
            tuple[Union[int, Any], Union[int, Any]],
        ]
    ]:
        """Generate boundaries for the layout based on the tiling.

        Returns:
            list: A list of tuples containing boundaries for the layout tiles.
        """
        # Get the tiling
        tilingVar_result = self.tiling(self.length, self.height, self.number)

        # Store the boundaries of the tiles in the form of top-left and bottom-right corners
        boundaries = []

        # Initialize the shift
        shift = 0
        for tiling_key in ["short", "long"]:
            tilingVar = tilingVar_result[tiling_key]
            for row in range(tilingVar["n_rows"]):
                for col in range(tilingVar["n_cols"]):
                    if tilingVar_result["mode"] == "rows":
                        top_left = (
                            col * tilingVar["tile_length"],
                            row * tilingVar["tile_height"] + shift,
                        )
                        bottom_right = (
                            (col + 1) * tilingVar["tile_length"],
                            (row + 1) * tilingVar["tile_height"] + shift,
                        )
                    else:
                        top_left = (
                            col * tilingVar["tile_length"] + shift,
                            row * tilingVar["tile_height"],
                        )
                        bottom_right = (
                            (col + 1) * tilingVar["tile_length"] + shift,
                            (row + 1) * tilingVar["tile_height"],
                        )
                    boundaries.append((top_left, bottom_right))

            # Update the shift for the next tiling key
            if tilingVar_result["mode"] == "rows":
                shift += tilingVar["n_rows"] * tilingVar["tile_height"]
            else:
                shift += tilingVar["n_cols"] * tilingVar["tile_length"]

        return boundaries

    def plot_tiling_boundaries(self) -> None:
        """Plot the boundaries of the layout tiles."""
        boundaries = self.generate_layout_boundaries()
        self.plot_boundaries(boundaries)

    def plot_boundaries(self, boundaries: list) -> None:
        """Plot the boundaries of the layout tiles.

        Parameters:
            boundaries (list): List of tuples containing boundaries for the layout tiles.
        """
        fig, ax = plt.subplots()
        for boundary in boundaries:
            top_left, bottom_right = boundary
            width = bottom_right[0] - top_left[0]
            height = bottom_right[1] - top_left[1]
            rect = patches.Rectangle(
                top_left, width, height, linewidth=1, edgecolor="r", facecolor="none"
            )
            ax.add_patch(rect)
        plt.xlim(0, max([b[1][0] for b in boundaries]))
        plt.ylim(0, max([b[1][1] for b in boundaries]))
        plt.gca().set_aspect("equal", adjustable="box")
        if self.plot:
            plt.show()

    def plot_tiling(self, length: float, height: float, number: int) -> None:
        """Plot the tiling layout.

        Parameters:
            length (float): Length of the environment
            height (float): Height of the environment
            number (int): Number of areas to split the environment into
        """
        tiles = self.tiling(length, height, number)
        plt.figure(figsize=(length, height))
        if tiles["mode"] == "rows":
            row_height = 0
            # Short rows
            tile_height = tiles["short"]["tile_height"]
            tile_length = tiles["short"]["tile_length"]
            for i in range(tiles["short"]["n_rows"]):
                # Horizontal line
                plt.plot((0, length), (row_height, row_height))
                for j in range(tiles["short"]["n_cols"] + 1):
                    # Vertical lines
                    plt.plot(
                        (j * tile_length, j * tile_length),
                        (row_height, row_height + tile_height),
                    )
                row_height += tile_height
            # Long rows
            tile_height = tiles["long"]["tile_height"]
            tile_length = tiles["long"]["tile_length"]
            for i in range(tiles["long"]["n_rows"]):
                # Horizontal line
                plt.plot((0, length), (row_height, row_height))
                for j in range(tiles["long"]["n_cols"] + 1):
                    # Vertical lines
                    plt.plot(
                        (j * tile_length, j * tile_length),
                        (row_height, row_height + tile_height),
                    )
                row_height += tile_height
            # Final horizontal line
            plt.plot((0, length), (row_height, row_height))
        elif tiles["mode"] == "cols":
            col_length = 0
            # Short cols
            tile_height = tiles["short"]["tile_height"]
            tile_length = tiles["short"]["tile_length"]
            for i in range(tiles["short"]["n_cols"]):
                # Horizontal line
                plt.plot((col_length, col_length), (0, height))
                for j in range(tiles["short"]["n_rows"] + 1):
                    # Vertical lines
                    plt.plot(
                        (col_length, col_length + tile_length),
                        (j * tile_height, j * tile_height),
                    )
                col_length += tile_length
            # Long cols
            tile_height = tiles["long"]["tile_height"]
            tile_length = tiles["long"]["tile_length"]
            for i in range(tiles["long"]["n_cols"]):
                # Horizontal line
                plt.plot((col_length, col_length), (0, height))
                for j in range(tiles["long"]["n_rows"] + 1):
                    # Vertical lines
                    plt.plot(
                        (col_length, col_length + tile_length),
                        (j * tile_height, j * tile_height),
                    )
                col_length += tile_length
            # Final vertical line
            if self.plot:
                plt.plot((col_length, col_length), (0, height))
                plt.show()
