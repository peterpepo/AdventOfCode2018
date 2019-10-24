from commons.commons import read_puzzle_input
import os


def solve():
    """
    Advent Of Code 2018 - Day11 Solution.
    :return: tuple(partOneResult[int], partTwoResult[int])
    Uses summed-area table to calculate sum of square on a rack.
    More information about summed-area table can be found on: https://en.wikipedia.org/wiki/Summed-area_table
    """

    puzzle_input = int(read_puzzle_input(os.path.dirname(os.path.abspath(__file__)), "day11_input.txt")[0])

    RACK_DIMENSION = 300

    def getCellPower(pos_x, pos_y, grid_serial):
        """
        Calculates power level of a cell based on its position and serial number of a grid.
        :param pos_x: (int) Position on x-axis.
        :param pos_y: (int) Position on y-axis.
        :param grid_serial: (int) Serial number of a grid.
        :return:
        """
        RACK_ID = pos_x + 10
        return (RACK_ID * pos_y + grid_serial) * RACK_ID % 1000 // 100 - 5

    # Summed Area Table for rack
    rack_summed_area_table = {}

    def getSummedAreaAtPosition(pos_x, pos_y):
        summed_value = None

        # Grid starts at [1,1], if asked for value outside, return 0.
        if pos_x < 1 or pos_y < 1:
            return 0
        else:
            # Calculate value, if asked inside rack.
            try:
                # Get the cached value in case it exists.
                summed_value = rack_summed_area_table[(pos_x, pos_y)]
            except KeyError:
                # In case value is not in cache yet, calculate and cache it.
                summed_value = getCellPower(pos_x, pos_y, puzzle_input)\
                               + getSummedAreaAtPosition(pos_x, pos_y - 1)\
                               + getSummedAreaAtPosition(pos_x - 1, pos_y)\
                               - getSummedAreaAtPosition(pos_x - 1, pos_y - 1)
                rack_summed_area_table[(pos_x, pos_y)] = summed_value
            return summed_value

    def getSumOfRectangle(start_x, start_y, end_x, end_y):
        """
        Get sum of a rectangle with top-left and bottom-right corners specified.
        :param start_x: (int) top-left x
        :param start_y: (int) top-left y
        :param end_x: (int) bottom-right x
        :param end_y: (int) bottom-right y
        :return: (int) sum of a rectangle
        """
        return getSummedAreaAtPosition(end_x, end_y)\
                - getSummedAreaAtPosition(start_x - 1, end_y)\
                - getSummedAreaAtPosition(end_x, start_y - 1)\
                + getSummedAreaAtPosition(start_x - 1, start_y - 1)

    def getMaxSumOfSizeBetween(size_min, size_max):
        """
        Returns maximum sum of a square with side length between size_min and size_max on a rack.
        :param size_min: (int) minimum square side length
        :param size_max: (int) maximum square side length
        :return: (int, int, int, int) top-left corner x, y position of a square, side length, sum of a maximum square
        """
        max_square_side = None
        max_square_pos_x = None
        max_square_pos_y = None
        max_square_sum = None

        # Check for each square side length in specified interval.
        for current_size in range(size_min, size_max + 1):
            # Let the square side length to be the bottom-right corner of a square
            # Move the x to the right one-by-one in loop
            for end_x in range(current_size, RACK_DIMENSION + 1):
                # Move the y down one-by-one in loop
                for end_y in range(current_size, RACK_DIMENSION + 1):
                    # Get sum for current square
                    start_x = end_x - current_size + 1
                    start_y = end_y - current_size + 1
                    square_sum = getSumOfRectangle(start_x, start_y, end_x, end_y)

                    # In case new sum is greater than known maximum, remember its position, side length and sum
                    if max_square_sum is None or square_sum > max_square_sum:
                        max_square_sum = square_sum
                        max_square_pos_x = start_x
                        max_square_pos_y = start_y
                        max_square_side = current_size

        return (max_square_pos_x, max_square_pos_y, max_square_side, max_square_sum)

    # Get result of part one of the puzzle - square with side exactly 3 units long and slice the of the square side length and sum off, since it's not required for puzzle
    partOneResult = getMaxSumOfSizeBetween(3, 3)[0:2]

    # Get result for part two- square of any size
    partTwoResult = getMaxSumOfSizeBetween(1, RACK_DIMENSION)[0:3]

    return (partOneResult, partTwoResult)
