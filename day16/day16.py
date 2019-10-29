from commons.commons import read_puzzle_input_as_string
import os, re


class VirtualMachine():
    def __init__(self):
        self.registers = []
        for reg_idx in range(4):
            self.registers.append(0)

    def setRegisters(self, registers):
        for register_idx in range(len(registers)):
            self.registers[register_idx] = registers[register_idx]

    def getRegisters(self):
        return self.registers

    def processInstruction(self, instruction, a, b, c):
        if instruction == "addr":
            self.registers[c] = self.registers[a] + self.registers[b]
        elif instruction == "addi":
            self.registers[c] = self.registers[a] + b
        elif instruction == "mulr":
            self.registers[c] = self.registers[a] * self.registers[b]
        elif instruction == "muli":
            self.registers[c] = self.registers[a] * b
        elif instruction == "banr":
            self.registers[c] = self.registers[a] & self.registers[b]
        elif instruction == "bani":
            self.registers[c] = self.registers[a] & b
        elif instruction == "borr":
            self.registers[c] = self.registers[a] | self.registers[b]
        elif instruction == "bori":
            self.registers[c] = self.registers[a] | b
        elif instruction == "setr":
            self.registers[c] = self.registers[a]
        elif instruction == "seti":
            self.registers[c] = a
        elif instruction == "gtir":
            self.registers[c] = 1 if a > self.registers[b] else 0
        elif instruction == "gtri":
            self.registers[c] = 1 if self.registers[a] > b else 0
        elif instruction == "gtrr":
            self.registers[c] = 1 if self.registers[a] > self.registers[b] else 0
        elif instruction == "eqir":
            self.registers[c] = 1 if a == self.registers[b] else 0
        elif instruction == "eqri":
            self.registers[c] = 1 if self.registers[a] == b else 0
        elif instruction == "eqrr":
            self.registers[c] = 1 if self.registers[a] == self.registers[b] else 0


def solve():
    """
    Advent Of Code 2018 - Day16 Solution.
    :return: tuple(partOneResult[int], partTwoResult[int])
    """
    # Read puzzle input - split it for tests (used in part_one and training in part_two) and program (used in part_two)
    LINE_SEPARATOR = '\n'
    INPUT_SEPARATOR = LINE_SEPARATOR + LINE_SEPARATOR + LINE_SEPARATOR
    NUMBER_RE_PATTERN = r"\d+"

    input_part_one, input_part_two = read_puzzle_input_as_string(os.path.dirname(os.path.abspath(__file__)),
                                                                 "day16_input.txt").strip().split(INPUT_SEPARATOR)

    # 3) List of valid virtual machine instructions
    MACHINE_INSTRUCTIONS = ["addr", "addi",
                            "mulr", "muli",
                            "banr", "bani",
                            "borr", "bori",
                            "setr", "seti",
                            "gtir", "gtri", "gtrr",
                            "eqir", "eqri", "eqrr"]

    def solvePartOne():
        # Number of op codes which behave as more than one instruction (each tested input, output and instruction are independent)
        # For example for sample a, 0 might behave like 'addi', 'addr', 'mulr'
        # For another sample a 0 might behave like 'muli', 'banr', 'bani'
        # We don't make an intersection of these results. Correct answer in this case would be two.
        total_op_behaving_as_more_than_three_instr = 0

        # Convert input_part_one string into list of lines
        input_part_one_lines = input_part_one.strip().split(LINE_SEPARATOR)

        # Create single VirtualMachine, which we use to initialize registers, run tested instruction and test the result
        vm_one = VirtualMachine()

        # Loop through testing instructions and test one by one
        # Jump by 4 lines (1st - initial state, 2nd - instruction to run, 3rd - expected result, 4th - blank)
        for line_idx in range(0, len(input_part_one_lines), 4):
            state_init = [int(x) for x in re.findall(NUMBER_RE_PATTERN, input_part_one_lines[line_idx])]
            instr_op, instr_a, instr_b, instr_c = [int(x) for x in
                                                   re.findall(NUMBER_RE_PATTERN, input_part_one_lines[line_idx + 1])]
            state_expected = [int(x) for x in re.findall(NUMBER_RE_PATTERN, input_part_one_lines[line_idx + 2])]

            instr_valid_for_input_output = 0  # Counter of instructions, which are applicable to given input and output

            # Test each instruction (regardless of op code - instr_test[0]) to produce expected result
            for tested_instruction in MACHINE_INSTRUCTIONS:
                vm_one.setRegisters(state_init)  # Set registers of machine to initial state
                vm_one.processInstruction(tested_instruction, instr_a, instr_b,
                                          instr_c)  # Process the instruction (ignoring op_code) and inputs a, b, c

                # If result matches to expected result, increase counter of applicable for this input, output
                if vm_one.getRegisters() == state_expected:
                    instr_valid_for_input_output += 1

            if instr_valid_for_input_output >= 3:
                total_op_behaving_as_more_than_three_instr += 1

        return total_op_behaving_as_more_than_three_instr

    def solvePartTwo():
        op_code_instructions = []  # List of instructions valid for numbers 0-15

        # Before testing, each instruction is valid for each instruction_id
        for instruction_id in range(len(MACHINE_INSTRUCTIONS)):
            op_code_instructions.append(MACHINE_INSTRUCTIONS[:])

        # Convert input_part_one string into list of lines - used to "train" the virtual machine
        input_part_two_training = input_part_one.strip().split(LINE_SEPARATOR)
        # Convert input_part_two string into list of lines - contains  the program itself
        input_part_two_program = input_part_two.strip().split(LINE_SEPARATOR)

        # Create single VirtualMachine, which we use to initialize registers, run tested instruction and test the result
        vm_two = VirtualMachine()

        # Loop through testing instructions and test one by one
        # Jump by 4 lines (1st - initial state, 2nd - instruction to run, 3rd - expected result, 4th - blank)
        for line_idx in range(0, len(input_part_two_training), 4):
            state_init = [int(x) for x in re.findall(NUMBER_RE_PATTERN, input_part_two_training[line_idx])]
            instr_op, instr_a, instr_b, instr_c = [int(x) for x in
                                                   re.findall(NUMBER_RE_PATTERN, input_part_two_training[line_idx + 1])]
            state_expected = [int(x) for x in re.findall(NUMBER_RE_PATTERN, input_part_two_training[line_idx + 2])]

            # For each opcode, test all instructions, which have not been invalidated (e.g: in previous run, 0 was proven not to be the addr. in this run we are not testing 0 to be the addr)
            # Contrary to first puzzle, we use op_code - instr_op to pick list of available instructions
            for tested_instruction in op_code_instructions[instr_op]:
                vm_two.setRegisters(state_init)  # Set registers of machine to initial state
                vm_two.processInstruction(tested_instruction, instr_a, instr_b,
                                          instr_c)  # Process the instruction

                # If result doesn't match expected result, we remove this instruction (mapping) from currently tested op code
                if vm_two.getRegisters() != state_expected:
                    op_code_instructions[instr_op].remove(tested_instruction)

        # At this stage, for each op code we have one (or more) instructions which are applicable for whole input
        # If there is an op code, with 1:1 mapping to an instruction, no other op code can map to this instruction
        # We find instructions which are 1:1 mapped to op code. Then we remove these instructions from all other op codes. We loop until all of opcodes have only 1 possible op code.

        # len(x) represents number of op code to instruction mapping per op code
        # As long as there is more mappings than instructions, we need to clean mappings by removing what is known as described above.
        while sum([len(x) for x in op_code_instructions]) > len(MACHINE_INSTRUCTIONS):
            mapped_one_to_one = [x[0] for x in op_code_instructions if
                                 len(x) == 1]  # Find instruction names mapped to exactly one op code

            # Loop through all instructions
            for i in range(len(op_code_instructions)):
                # Remove all already mapped as one to one ( len(op_code_instructions[i]) > 1 ensures we don't remove mapping from single identified op code)
                if len(op_code_instructions[i]) > 1:
                    op_code_instructions[i] = [x for x in op_code_instructions[i] if x not in mapped_one_to_one]

        # We have 1:1 mapping of op code to instruction. All that's left to do is run program (second part of puzzle input) with this mapping.

        # Reset registers of virtual machine
        vm_two.setRegisters([0, 0, 0, 0])

        for program_instruction in input_part_two_program:
            instr_op, instr_a, instr_b, instr_c = [int(x) for x in
                                                   re.findall(NUMBER_RE_PATTERN, program_instruction)]

            # op_code_instructions[instr_op][0] - look for "all" instructions mapped to op code instr_op, and take "first" (only one)
            vm_two.processInstruction(op_code_instructions[instr_op][0], instr_a, instr_b, instr_c)

        # Return register 0
        return vm_two.getRegisters()[0]

    return solvePartOne(), solvePartTwo()
