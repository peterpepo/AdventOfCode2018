from commons.commons import read_puzzle_input, write_lines_list_to_file
import os, re, sys


def solve():
    """
    Advent Of Code 2018 - Day17 Solution.
    :return: tuple(partOneResult[int], partTwoResult[int])
    """
    NUMBER_RE_PATTERN = r"\d+"

    puzzle_input = puzzle_input = read_puzzle_input(os.path.dirname(os.path.abspath(__file__)), "day17_input.txt")

    # Constants for clay, send, water, spring position
    SPRING_POSITION = (500, 0)
    CLAY = "#"
    SAND = "."
    WATER_RUNNING = "|"
    WATER_STILL = "~"

    clay = set()  # Set of (x,y) positions of CLAY
    water_running = set()  # Set of (x,y) positions of running water
    water_still = set()  # Set of (x,y) positions of still water

    def isSand(position):
        """
        Since we don't store list of SAND tiles, we have a function which checks, whether tile isn't clay or water
        :param position: (x, y) position
        :return: (bool) True / False
        """
        return position not in clay and position not in water_running and position not in water_still

    # Loop through puzzle input lines
    for puzzle_input_line in puzzle_input:
        # Find all numbers in single puzzle input row
        puzzle_input_line_ints = [int(x) for x in re.findall(NUMBER_RE_PATTERN, puzzle_input_line)]

        # If it starts with x, first number is static x position, two and third defines y range of clay
        if puzzle_input_line.startswith("x"):
            for y in range(puzzle_input_line_ints[1], puzzle_input_line_ints[2] + 1):
                clay.add((puzzle_input_line_ints[0], y))
        # If it starts with y, first number is static y position, two and third defines x range of clay
        elif puzzle_input_line.startswith("y"):
            for x in range(puzzle_input_line_ints[1], puzzle_input_line_ints[2] + 1):
                clay.add((x, puzzle_input_line_ints[0]))

    # Find minimum and maximum x and y values
    #
    # Y limits vertical range to tiles "..in your scan?", as defined by puzzle (e.g. if spring is at (500, 0)
    # and our first clay at (500, 150), we don't want those 150 vertical tiles to be counted towards result
    y_min = min(pos_x_y[1] for pos_x_y in clay)
    y_max = max(pos_x_y[1] for pos_x_y in clay)
    #
    # X theoretically doesn't limit our space, since water falls down. It only shifts to the side, when there is clay
    # right underneath. That would increase x_max though.
    x_min = min(pos_x_y[0] for pos_x_y in clay)
    x_max = max(pos_x_y[0] for pos_x_y in clay)

    def saveStateToFile():
        """
        Writes output - current state of a grid to file.
        """
        lines_to_write = []
        lines_to_write.append("Top-left corner: [{},{}]\n".format(x_min - 1, y_min))
        lines_to_write.append("Bottom-right corner: [{},{}]\n".format(x_max + 1, y_max + 1))

        # We are interested only in rows in range of our input (+1 since range excludes end value)
        for y in range(y_min, y_max + 1):
            line_to_write = ""
            # We start one column to the left and one to the right compared to x_min, x_max - water can run down
            # off the edge of the pool to the side (puzzle question limits y range only, id doesn't limit x range).
            for x in range(x_min - 1, x_max + 2):
                if (x, y) in clay:
                    line_to_write += CLAY
                elif (x, y) in water_running:
                    line_to_write += WATER_RUNNING
                elif (x, y) in water_still:
                    line_to_write += WATER_STILL
                else:
                    line_to_write += SAND
            line_to_write += "\n"
            lines_to_write.append(line_to_write)

        # Save as new file
        write_lines_list_to_file(os.path.dirname(os.path.abspath(__file__)), "day17_output.txt", lines_to_write, "w")

    def hasWall(position, side):
        """
        Checks, whether tile at position has wall to the side
        :param position: (x,y) position
        :param side: +1 - to the right, -1 to the left
        :return: (bool) True / False
        """
        current_x, static_y = position

        while (True):
            # If we hit the clay, we found the wall
            if (current_x, static_y) in clay:
                return True
            # If we hit sand, there's no wall
            elif isSand((current_x, static_y)):
                return False

            # If we didn't hit clay, nor sand, it's water (running/still) and we move to the side and check again
            current_x += side

    def hasBothWalls(position):
        """
        Checks whether tile at position (x,y) has walls to both sides
        :param position: (x,y) position to check
        :return: (bool) True/False
        """
        return hasWall(position, 1) & hasWall(position, -1)

    def fillSide(position, side):
        """
        Fills tiles from position (x,y) to the side with still water and removes running water.
        :param position: (x,y) starting position
        :param side: +1 - to the right, -1 to the left
        """
        current_x, fixed_y = position

        while (True):
            # When we hit clay, we can't fill anymore
            if (current_x, fixed_y) in clay:
                return
            try:
                # Remove water from set of running
                water_running.remove((current_x, fixed_y))
            except KeyError:
                # We may encounter KeyError, when we fill both sides LEFT and RIGHT and we try to remove "center" tile twice
                pass
            # Add water to set of still
            water_still.add((current_x, fixed_y))

            # Move to the side
            current_x += side

    def fillBothSides(position):
        """
        Fills both sides to the (x,y) position with still water.
        """
        fillSide(position, 1)
        fillSide(position, -1)

    def fill(starting_position):
        """
        Fills the grid with water. This is core function of this puzzle.
            It pours running water from top to bottom.
            When it reaches clay, the water pours to the sides.
            When whole line fills with running water, it is converted to still water.
            We stop filling, once the y position gets outside of range given by our puzzle input.
        """
        x, y = starting_position

        # Stop pouring, once we get out of y range.
        if (y >= y_max):
            return

        # If there is space below, pour water
        if isSand((x, y + 1)):
            water_running.add((x, y + 1))
            fill((x, y + 1))
        # If tile below is clay, or running water, pour to the right
        if ((x, y + 1) in clay or (x, y + 1) in water_still) and isSand((x + 1, y)):
            water_running.add((x + 1, y))
            fill((x + 1, y))
        # If tile below is clay, or running water, pour to the left
        if ((x, y + 1) in clay or (x, y + 1) in water_still) and isSand((x - 1, y)):
            water_running.add((x - 1, y))
            fill((x - 1, y))
        # Convert row of running water to still water
        if hasBothWalls((x, y)):
            fillBothSides((x, y))

    # Solutions uses recursion - tile which is poured tries to pour again, and those new again
    # python default setting (1000) is pretty limiting and we hit maximum recursion limit easily:
    #   RecursionError: maximum recursion depth exceeded in comparison
    # I found the recursion depth of my puzzle to be 2784, thus I left some room left for other puzzle inputs.
    #   If you still run into RecursionError exception, please raise this value.
    sys.setrecursionlimit(3000)

    # Fill the grid with water starting at SPRING_POSITION
    fill(SPRING_POSITION)

    # Count running water tiles between y_min and y_max
    count_water_running = len([position for position in water_running if position[1] >= y_min and position[1] <= y_max])

    # Count still water tiles between y_min and y_max
    count_water_still = len([position for position in water_still if position[1] >= y_min and position[1] <= y_max])

    # We are summing up all wet tiles - either with running or still water
    part_one_answer = count_water_running + count_water_still

    # If the spring dries out, all water which is running will run down - path defined by running water
    # Therefore only the still water (which has walls to both sides) remains and won't drain
    part_two_answer = count_water_still

    # Writes final state of the grid to the output file
    saveStateToFile()

    return (part_one_answer, part_two_answer)
