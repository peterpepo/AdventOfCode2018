from commons.commons import read_puzzle_input, circular_buffer_position
import os


def solve():
    """
    Advent Of Code 2018 - Day01 Solution.
    :return: tuple(partOneResult[int], partTwoResult[int])
    """

    # Read puzzle input from file
    puzzle_input = read_puzzle_input(os.path.dirname(os.path.abspath(__file__)), "day01_input.txt")

    def solvePartOne():
        """Advent Of Code 2018 - Day01 - Part One Solution.
        :return: int
        """
        frequency_current = 0  # Current frequency

        for frequency_adjustment_string in puzzle_input:
            frequency_current += int(frequency_adjustment_string)

        return frequency_current

    def solvePartTwo():
        """Advent Of Code 2018 - Day01 - Part Two Solution.
        :return: int
        """
        frequencies_seen = set()  # Set of frequencies already seen
        frequency_current = 0  # Current frequency
        i = 0  # Iterator over circular buffer of frequency adjustments

        while True:
            # Return, when the frequency is seen second time or remember if seen for the first time
            if frequency_current in frequencies_seen:
                return frequency_current
            else:
                frequencies_seen.add(frequency_current)

            # Adjust current frequency
            frequency_current += int(puzzle_input[circular_buffer_position(len(puzzle_input), 0, i)])
            i += 1

    return solvePartOne(), solvePartTwo()
