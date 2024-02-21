import random
import webcolors
import numpy as np
from typing import Union
from random import sample
from PIL import ImageColor


class ObjectPropertyRandomization:
    """Generates random colors, sizes and z-rotation depending on user input."""

    @staticmethod
    def sample_from_amount(amount: tuple[int, int]) -> int:
        """Sample the amount of objects to be placed if amount is a tuple of different values.

        Parameters:
           amount (tuple[int, int]): Range of objects for randomization

        Returns:
            amount_int (int): Sample drawn from amount range
        """
        amount_int = (
            amount[0]
            if (amount[0] == amount[1])
            else np.random.randint(
                int(amount[0]), int(amount[1]) + 1
            )  # Randint function is exclusive on high val
        )
        return amount_int

    @staticmethod
    def get_random_colors(
        amount: int, color_groups: Union[tuple[int, int], None]
    ) -> Union[list[list[float]], None]:
        """Returns a list of random rgba colors (with alpha=1).

        Parameters:
            amount (int): Number of objects
            color_groups (Union[tuple[int, int], None]): Range of members per distinctly colored group

        Returns:
            colors_for_placement (Union[list[list[float]], None]): List of randomized rgba colors
                                                (with duplicate entries for each group member, if color_groups > 1)
        """
        if color_groups is None:
            return None

        # Get list of available color names
        color_names = list(webcolors.CSS3_NAMES_TO_HEX.keys())

        # Get random int in range of colors
        colors_randint = (
            color_groups[0]
            if (color_groups[0] == color_groups[1])
            else np.random.randint(
                int(color_groups[0]), int(color_groups[1]) + 1
            )  # higher is excluding
        )

        # Get number of different colors needed by amount / color_groups
        colors_needed = int(
            amount / colors_randint
        )  # Int type cast automatically rounds down

        # Get random rgba for number of colors needed
        colors_rgba = list()

        # Shuffle color names
        random.shuffle(color_names)

        # Loop over the first 'colors_needed' colors and convert them to rgba
        # and normalize between 0 and 1
        for color in color_names[:colors_needed]:
            color_rgba = ObjectPropertyRandomization.get_rgba_from_color_name(color)
            color_rgba_normalized = [(float(val) / 255) for val in color_rgba]
            colors_rgba.append(color_rgba_normalized)

        # Generate list of colors depending on amount an
        colors_for_placement = list()
        for color in colors_rgba:
            for _ in range(colors_randint):
                colors_for_placement.append(color)

        # Fill colors_for_placement list if amount of objects is greater than colors in the list.
        # This happens if amount % color_groups != 0
        while amount > len(colors_for_placement):
            sampled_color = sample(colors_rgba, 1)[0]
            colors_for_placement.append(sampled_color)

        return colors_for_placement

    @staticmethod
    def get_random_sizes(
        amount: int,
        size_groups: Union[tuple[float, float], None],
        size_value_range: Union[tuple[float, float], None],
    ) -> Union[list[list[float]], None]:
        """Returns a list of random sizes.

        Parameters:
            amount (int): Number of objects
            size_groups (Union[tuple[float, float], None]): Range of members per distinctly sized group
            size_value_range (Union[tuple[float, float], None]): Defines the value size of the randomization process

        Returns:
            sizes_for_placement (Union[list(float, float, float), None]): List of randomized sizes
                    (with duplicate entries for each group member, if size_groups > 1)
        """
        if size_groups is None:
            return None

        # Get random int in range of sizes
        sizes_randint = (
            size_groups[0]
            if (size_groups[0] == size_groups[1])
            else np.random.randint(
                int(size_groups[0]), int(size_groups[1]) + 1
            )  # Higher is excluding
        )

        # Get number of different sizes needed by amount / size_groups
        sizes_needed = int(
            amount / sizes_randint
        )  # Int type cast automatically rounds down

        # Get random sizes for number of sizes needed
        sizes = list()
        sizes_used = list()
        for _ in range(sizes_needed):
            random_size = ObjectPropertyRandomization.get_size_array(
                size_value_range=size_value_range
            )
            while random_size in sizes_used:
                random_size = ObjectPropertyRandomization.get_size_array(
                    size_value_range=size_value_range
                )
            sizes_used.append(random_size)
            sizes.append(random_size)

        # Generate list of colors depending on amount an
        sizes_for_placement = list()
        for size in sizes:
            for _ in range(sizes_randint):
                sizes_for_placement.append(size)

        # Fill colors_for_placement list if amount of objects is greater than colors in the list.
        # This happens if amount % color_groups != 0
        while amount > len(sizes_for_placement):
            sampled_color = sample(sizes, 1)[0]
            sizes_for_placement.append(sampled_color)

        # Apply shuffling so that color and size is not synchronized
        random.shuffle(sizes_for_placement)

        return sizes_for_placement

    @staticmethod
    def get_rgba_from_color_name(
        color_name: str,
    ) -> Union[tuple[float, float, float, float], None]:
        """Takes color as argument and returns the corresponding rgba color code.

        Parameters:
            color_name (str): Name of color

        Returns:
            rgba (Union[tuple[float, float, float, float], None]): Rgba values for the corresponding color string
        """
        try:
            # Get hexadecimal color code
            hex_code = webcolors.name_to_hex(color_name)
            # Convert hexadecimal to RGBA
            rgba = ImageColor.getcolor(hex_code, "RGBA")
            return rgba
        except ValueError:
            raise ValueError(f"Invalid color name {color_name}.")

    @staticmethod
    def get_size_array(size_value_range: tuple[float, float]) -> list[float]:
        """Generates 3D random size in given range.

        Parameters:
            size_value_range (tuple[float, float]): Range of possible size values

        Returns:
            random_size (list[float]): Randomized size values in given range for 3D
        """
        x_rand_size_float = float(
            np.random.uniform(size_value_range[0], size_value_range[1])
        )  # Higher is excluding
        y_rand_size_float = float(
            np.random.uniform(size_value_range[0], size_value_range[1])
        )  # Higher is excluding
        z_rand_size_float = float(
            np.random.uniform(size_value_range[0], size_value_range[1])
        )  # Higher is excluding
        random_size = [x_rand_size_float, y_rand_size_float, z_rand_size_float]
        return random_size

    @staticmethod
    def get_random_rotation(
        amount: int, z_rotation_range: Union[tuple[int, int], None]
    ) -> Union[list[float], None]:
        """Generate random number in z_rotation_range.

        Parameters:
            amount (int): Number of objects
            z_rotation_range (Union[tuple[int, int], None]): Range of degrees for randomization of z-axis

        Returns:
            z_rotations_for_placement (Union[list[float], None]): Random numbers in given range for z-axis rotation
        """
        if z_rotation_range is None:
            return None

        z_rotations_for_placement = list()
        for _ in range(amount):
            z_rotation = np.random.uniform(
                z_rotation_range[0], z_rotation_range[1]
            )  # Higher is excluding
            z_rotations_for_placement.append(z_rotation)
        return z_rotations_for_placement
