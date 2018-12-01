RESULT_PRINT_FORMAT = "Day {day_number}, partOne: {solution[0]}\nDay {day_number}, partTwo: {solution[1]}"

# Run day01
from day01 import day01
print(RESULT_PRINT_FORMAT.format(day_number="01", solution=day01.solve()))
