RESULT_PRINT_FORMAT = "Day {day_number}, partOne: {solution[0]}\nDay {day_number}, partTwo: {solution[1]}"

# Run day01
from day01 import day01
print(RESULT_PRINT_FORMAT.format(day_number="01", solution=day01.solve()))

# Run day02
from day02 import day02
print(RESULT_PRINT_FORMAT.format(day_number="02", solution=day02.solve()))

# Run day03
from day03 import day03
print(RESULT_PRINT_FORMAT.format(day_number="03", solution=day03.solve()))

# Run day04
from day04 import day04
print(RESULT_PRINT_FORMAT.format(day_number="04", solution=day04.solve()))

# Run day05
from day05 import day05
print(RESULT_PRINT_FORMAT.format(day_number="05", solution=day05.solve()))

# Run day06
from day06 import day06
print(RESULT_PRINT_FORMAT.format(day_number="06", solution=day06.solve()))