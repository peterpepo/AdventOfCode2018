from commons.commons import read_puzzle_input
from collections import Counter
import os


def solve():
    """
    Advent Of Code 2018 - Day02 Solution.
    :return: tuple(partOneResult[int], partTwoResult[int])
    """

    # Read puzzle input from file
    puzzle_input = read_puzzle_input(os.path.dirname(os.path.abspath(__file__)), "day02_input.txt")

    def containsCharacterExactlyTimes(word, times):
        """
        Checks, whether word contains any character exactly times times.
        :param word: Word to look for repeating characters in.
        :param times: Number of times, a word must contain any character.
        :return: True or False based on condition in description.
        """
        letter_counts = Counter(word)

        for letter_count in letter_counts.values():
            if letter_count == times:
                return True

        return False

    def differByOneCharAtSamePosition(wordOne, wordTwo):
        """
        Checks, whether two words of same length differ in exactly one character at same position.
        :param wordOne: First word to compare.
        :param wordTwo: Second word to compare.
        :return: True or False based on condition in description.
        """
        differences_count = 0

        for i in range(len(wordOne)):
            if (wordOne[i] != wordTwo[i]):
                differences_count += 1

            if differences_count > 1:
                return False

        return True

    def getSameCharacters(wordOne, wordTwo):
        """
        Returns string of same characters at same positions in two words.
        :param wordOne: First word to compare. 
        :param wordTwo: Second word to compare.
        :return: String of same characters at same positions in words - wordOne and wordTwo
        """
        same_characters = ""

        for i in range(len(wordOne)):
            if (wordOne[i] == wordTwo[i]):
                same_characters += wordOne[i]

        return same_characters

    def solvePartOne():
        """Advent Of Code 2018 - Day02 - Part One Solution.
        :return: int
        """
        count_of_words_containing_character_twice = 0
        count_of_words_containing_character_three_times = 0

        for word in puzzle_input:
            if (containsCharacterExactlyTimes(word, 2)):
                count_of_words_containing_character_twice += 1

            if (containsCharacterExactlyTimes(word, 3)):
                count_of_words_containing_character_three_times += 1

        return count_of_words_containing_character_twice * count_of_words_containing_character_three_times

    def solvePartTwo():
        """Advent Of Code 2018 - Day02 - Part Two Solution.
        :return: string
        """
        for i in range(len(puzzle_input)):
            for j in range(i + 1, len(puzzle_input)):
                if (differByOneCharAtSamePosition(puzzle_input[i], puzzle_input[j])):
                    same_characters = getSameCharacters(puzzle_input[i], puzzle_input[j])
                    return same_characters.rstrip() #Strip off end of line coming from puzzle input

    return solvePartOne(), solvePartTwo()