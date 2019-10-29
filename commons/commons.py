def read_puzzle_input(path, file_name):
    import os
    os.chdir(path)

    input_file = open(file_name, "r")
    input_lines = input_file.readlines()
    input_file.close()
    return input_lines

def read_puzzle_input_as_string(path, file_name):
    import os
    os.chdir(path)

    input_file = open(file_name, "r")
    input_string = input_file.read()
    input_file.close()
    return input_string

def circular_buffer_position(length, offset, order):
    return (offset + order) % length
