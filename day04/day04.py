from commons.commons import read_puzzle_input
import os, re


def getTotalTimeAsleep(sleep_intervals):
    """
    Returns total time, the guard was sleeping
    :param sleep_intervals: Intervals (start_minute, end_minute) guard was sleeping
    :return: int: total minutes guard was asleep
    """
    sleep_total = 0

    # Loop through intervals
    for sleep_interval in sleep_intervals:
        # For each minute in sleep interval increase counter, how many times it has been slept
        for i in range(sleep_interval[0], sleep_interval[1]):
            sleep_total += 1

    return sleep_total


def getMostFrequentMinute(sleep_intervals):
    """
    Returns most slept minute and times it was slept
    :param sleep_intervals: Intervals (start_minute, end_minute) guard was sleeping
    :return: (int: most_slept_minute, int:times_the_minute_has_been_slept)
    """
    minutes = {}
    maxTimes = None
    minuteSleptMaxTimes = None

    # Loop through intervals
    for sleep_interval in sleep_intervals:
        # For each minute in sleep interval increase counter, how many times it has been slept
        for i in range(sleep_interval[0], sleep_interval[1]):
            try:
                times = minutes[i]
            except KeyError:
                times = 0

            times += 1
            minutes[i] = times

            # If the minute has been slept more times, than the so far, remember it
            if maxTimes is None or times > maxTimes:
                maxTimes = times
                minuteSleptMaxTimes = i

    return (minuteSleptMaxTimes, times)


def solve():
    """
    Advent Of Code 2018 - Day04 Solution.
    :return: tuple(partOneResult[int], partTwoResult[int])
    """

    # Read puzzle input from file
    puzzle_input = read_puzzle_input(os.path.dirname(os.path.abspath(__file__)), "day04_input.txt")

    INSTRUCTION_PATTERN = r"(?<=:)(\d+)(?:.*)((?<=#)\d+|falls|wakes)"
    '''
    Regexp explanation:
    (?<=:)(\d+) - number prefixed with :, i.e. minute
    (?:.*) - as few any characters as possible
    (?<=#)\d+|falls|wakes) - number prefixed with #/falls/wakes
    '''

    guard_id = None  # ID of current guard
    start_time = None  # Shift start of current guard
    guards_records = {}  # Dictionary of guards and list of times, when they are asleep, e.g. {1:[(5,10), [15,20]}
    puzzle_input.sort()  # Sort instructions alphabetically (sort by date)

    # Loop through instructions
    for puzzle_input_line in puzzle_input:
        puzzle_instruction = re.search(INSTRUCTION_PATTERN, puzzle_input_line)

        # Check whether input is valid instruction
        if puzzle_instruction is not None:
            # Get time and instruction, which can either be: guardID, falls or wakes
            time, instruction = puzzle_instruction.group(1), puzzle_instruction.group(2)

            # When the guard wakes up, write down sleep slot (time read is end of sleep slot)
            if instruction == "wakes":
                end_time = int(time)

                guard = guards_records.get(guard_id, [])
                guard.append((start_time, end_time))
                guards_records[guard_id] = guard
            # When the guard falls asleep, remember sleep slot start, but don't write it yet
            elif instruction == "falls":
                start_time = int(time)
            # Otherwise we just got info about new guard starting shift
            else:
                guard_id = int(instruction)

    def solvePartOne():
        guardID_max_asleep = None  # ID of Guard, who slept the most time
        max_minutes_asleep = 0

        # Loop through all guards and find who has slept the most minutes total
        for guard in guards_records:
            minutes_asleep = getTotalTimeAsleep(guards_records[guard])
            if minutes_asleep > max_minutes_asleep:
                max_minutes_asleep = minutes_asleep
                guardID_max_asleep = guard

        # Find the minute, during which the guard slept most time
        most_frequent_minute = getMostFrequentMinute(guards_records[guardID_max_asleep])[0]  # Most slept minute

        return guardID_max_asleep * most_frequent_minute

    def solvePartTwo():
        max_slept_times = 0  # Maximum times the guard spent sleeping at given minute
        guard_max_at_minute = None  # ID of Guard who slept most times at given minute
        most_slept_minute = None  # Minute, which the guard spent most asleep

        for guard in guards_records:
            slept = getMostFrequentMinute(guards_records[guard])
            if slept[1] > max_slept_times:
                max_slept_times = slept[1]
                guard_max_at_minute = guard
                most_slept_minute = slept[0]

        return guard_max_at_minute * most_slept_minute

    return (solvePartOne(), solvePartTwo())
