from commons.commons import read_puzzle_input
import os, re
from collections import deque

def solve():
    """
    Advent Of Code 2018 - Day09 Solution.
    :return: tuple(partOneResult[int], partTwoResult[int])
    """

    puzzle_input = read_puzzle_input(os.path.dirname(os.path.abspath(__file__)), "day09_input.txt")

    INSTRUCTION_PATTERN = r"(\d+).*?(\d+)"
    '''
    Regexp explanation:
    (\d+) - number
    ?:.* - as few any characters as possible
    (\d+) - number
    '''
    puzzle_instruction = re.search(INSTRUCTION_PATTERN, puzzle_input[0])

    player_count, max_move_number = int(puzzle_instruction.group(1)), int(puzzle_instruction.group(2))

    def marble_game(player_count, max_marble_value):
        """
        Plays the marble game with number of players and max_marble_value defined.
        :param player_count: Number of players in the game.
        :param max_marble_value: Maximum value of marble. Game ends, when marble of this value has been placed into the circle.
        :return: (int) maximum score got by player in the game.
        """
        marbles = deque([0])                        # Marble circle
        players = [0 for i in range(player_count)]  # Scores of players
        move_number = 1                             # Current move number (equals to value of marble which is about to be placed into circle)

        while move_number < max_marble_value:
            if move_number % 23 == 0:
                # Rotates 7 steps right (marble 7 steps to the left becomes first in circle)
                marbles.rotate(7)
                # Remove first marble and add it to score of player whose move is
                players[move_number%player_count] = players[move_number%player_count] + marbles.popleft()
                # Add value of marble about to be placed to the circle to player's score, without actually placing it
                players[move_number%player_count] = players[move_number%player_count] + move_number
            else:
                # Rotate 2 steps left (marble 2 steps to the right becomes first in circle)
                marbles.rotate(-2)
                # Prepend marble to the beginning of the circle (this way it gets between formerly 1st and 2nd)
                marbles.appendleft(move_number)

            move_number = move_number + 1

        # Return maximum score of player
        return max(players)

    return (marble_game(player_count, max_move_number), marble_game(player_count, max_move_number*100))