from commons.commons import read_puzzle_input
import os, re


def solve():
    """
    Advent Of Code 2018 - Day03 Solution.
    :return: tuple(partOneResult[int], partTwoResult[int])
    """

    # Read puzzle input from file
    puzzle_input = read_puzzle_input(os.path.dirname(os.path.abspath(__file__)), "day03_input.txt")

    # Map of fabric usage, which piece is used by which claimIds, e.g: (x,y) -> [claim1, claim2]
    fabric_usage = {}

    INSTRUCTION_PATTERN = r"(\d+)"  # Sequences of digits
    for puzzle_instruction in puzzle_input:
        # There are five numbers in input - claim_id, distance from left, distance from top, horizontal size and vertical size
        claimid, offset_x, offset_y, size_x, size_y = [int(val) for val in
                                                       re.findall(INSTRUCTION_PATTERN, puzzle_instruction)]

        # For each requested fabric, write which claim asks for it
        for x in range(offset_x, offset_x + size_x):
            for y in range(offset_y, offset_y + size_y):
                coordinations = (x, y)
                piece_usage = fabric_usage.get(coordinations, [])
                piece_usage.append(claimid)

                fabric_usage[coordinations] = piece_usage

    def solvePartOne():
        """Advent Of Code 2018 - Day03 - Part One Solution.
        :return: int
        """

        # Count pieces of fabric which are asked for more than once (more than 1 claim)
        used_more_than_once = 0
        for piece_usage in fabric_usage.values():
            if len(piece_usage) > 1:
                used_more_than_once += 1

        return used_more_than_once

    def solvePartTwo():
        """Advent Of Code 2018 - Day03 - Part Two Solution.
        :return: set() of non-overlapping claim IDs
        """
        non_overlapping_claimids = set()

        all_claim_ids = set(claim_id for claim_ids in fabric_usage.values() for claim_id in claim_ids)

        claimid_conflicts = False

        # For each claimid, check whether it doesn't ask for same piece of fabric as any other piece
        for claimid in all_claim_ids:
            # Check all requested pieces
            for piece_usage in fabric_usage.values():
                # If more than one claimid asks for this piece of fabric, and currently checked is amongst them, this is overlap
                if len(piece_usage) > 1 and claimid in piece_usage:
                    claimid_conflicts = True
                    break

            if claimid_conflicts:
                claimid_conflicts = False
                continue

            non_overlapping_claimids.add(claimid)

        return non_overlapping_claimids

    return solvePartOne(), solvePartTwo()
