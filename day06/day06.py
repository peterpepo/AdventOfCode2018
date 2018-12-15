from commons.commons import read_puzzle_input
import os, re


def solve():
    """
    Advent Of Code 2018 - Day06 Solution.
    :return: tuple(partOneResult[int], partTwoResult[int])
    """

    def getManhattanDistance(point_one, point_two):
        return abs(point_one[0] - point_two[0]) + abs(point_one[1] - point_two[1])

    # Read puzzle input from file
    puzzle_input = read_puzzle_input(os.path.dirname(os.path.abspath(__file__)), "day06_input.txt")

    points_affected_area = {}

    x_min = x_max = y_min = y_max = None
    for instruction in puzzle_input:

        # Store points from puzzle_input
        point = instruction.strip().split(", ")
        x, y = int(point[0]), int(point[1])
        point = (x, y)

        points_affected_area[point] = 0

        # Define universe of points outside of "infinity"
        if x_min is None or x < x_min:
            x_min = x
        elif x_max is None or x > x_max:
            x_max = x

        if y_min is None or y < y_min:
            y_min = y
        elif y_max is None or y > y_max:
            y_max = y

    def solvePartOne():
        """Advent Of Code 2018 - Day06 - Part One Solution.
        :return: int
        """
        # Loop through universe and for each POSITION find which POINT is closed based on Manhattan distance
        for x in range(x_min, x_max + 1):
            for y in range(y_min, y_max + 1):
                current_position = (x, y)
                closest_distance, closest_point = None, None

                for point in points_affected_area:
                    point_to_position_distance = getManhattanDistance(current_position, point)

                    if closest_distance is None or point_to_position_distance < closest_distance:
                        closest_distance = point_to_position_distance
                        closest_point = point

                # Increase the count of controlled area for closest POINT to the POSITION
                point_area = points_affected_area[closest_point]
                point_area += 1
                points_affected_area[closest_point] = point_area

        # Loop through points and find which affects the largest area
        largest_area = None
        for point in points_affected_area:
            current_area = points_affected_area[point]
            if largest_area is None or current_area > largest_area:
                largest_area = current_area

        return largest_area

    def solvePartTwo():
        """Advent Of Code 2018 - Day06 - Part Two Solution.
        :return: int
        """
        total_area = 0
        MAX_DISTANCE = 10000

        # Loop through universe and for each POSITION find which POINT is closed based on Manhattan distance
        # for x in range(x_min-universe_offset, x_max + 1+universe_offset):
        #     for y in range(y_min-universe_offset, y_max + 1+universe_offset):
        for x in range(x_max + 1):
            for y in range(y_max + 1):
                current_position = (x, y)

                distance_to_all_points = 0
                for point in points_affected_area:
                    distance_to_all_points += getManhattanDistance(current_position, point)

                if distance_to_all_points < MAX_DISTANCE:
                    total_area += 1

        return total_area

    return solvePartOne(), solvePartTwo()
