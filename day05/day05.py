from commons.commons import read_puzzle_input
import os


def solve():
    """
    Advent Of Code 2018 - Day05 Solution.
    :return: tuple(partOneResult[int], partTwoResult[int])
    """

    def getReactedLength(polymerInput, ignoreElement):
        unmatched_char_positions = []  # List of character positions, which already have been looped through but not reacted yet
        matched_chars_count = 0  # Count of matched characters, i.e. count of reacted elements (not polymers)
        skipped_chars = 0  # Count of skipped elements (useful in partTwo, when certain elements are ignored)

        # Loop through whole polymer, element by element
        for i in range(len(polymerInput)):
            # Set the flag, that this element hasn't reacted
            element_reacted_flag = False

            # Read current element
            char_current = polymerInput[i]

            # In case, this element is to be ignored, just skip it
            if char_current.upper() == ignoreElement.upper():
                skipped_chars += 1  # Increase count of skipped elements (used when calculating length).
                continue

            # Check if there are any elements to the left of current, which hasn't reacted yet
            # This is list is empty, when reading first character (there is nothing to the left to react with)
            if unmatched_char_positions:

                # Read, what last unreacted element is
                char_previous = polymerInput[unmatched_char_positions[-1]]

                # Check, whether previous and current elements can react (They're lower and upper case of the same character)
                if char_current.upper() == char_previous.upper() and (
                        (char_previous.islower() and char_current.isupper()) or (
                        char_previous.isupper() and char_current.islower())):
                    # When the elements reacted, length of polymer reduces by two, thus increase the counter
                    matched_chars_count += 2

                    # Remove reference to unreacted element
                    unmatched_char_positions.pop()
                    element_reacted_flag = True

            # If current element hasn't reacted, add it to list of unreacted
            if not element_reacted_flag:
                unmatched_char_positions.append(i)

        return len(polymerInput) - skipped_chars - matched_chars_count

    # Get first line of puzzle input (as there's only one line supposed to be)
    puzzle_input = read_puzzle_input(os.path.dirname(os.path.abspath(__file__)), "day05_input.txt")[0]

    def solvePartOne():
        """Advent Of Code 2018 - Day05 - Part One Solution.
        :return: int
        """
        return getReactedLength(puzzle_input, "")

    def solvePartTwo():
        """Advent Of Code 2018 - Day05 - Part Two Solution.
        :return: int
        """
        # Get list of elements in puzzle input
        polymer_elements = set(puzzle_input.upper())

        min_polymer_length = None

        # Exclude (remove) each of elements and get length of reacted polymer
        for polymerElementToRemove in polymer_elements:
            current_length = getReactedLength(puzzle_input, polymerElementToRemove)
            if min_polymer_length is None or current_length < min_polymer_length:
                min_polymer_length = current_length

        return min_polymer_length

    return (solvePartOne(), solvePartTwo())
