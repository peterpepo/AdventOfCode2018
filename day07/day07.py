from commons.commons import read_puzzle_input
import os


class Node:
    def __init__(self):
        self.preconditions = []  # List of nodes, which must be processed before this one
        self.state = 0  # State of the node (1-done, 0-not done yet)

    def addPreconditionNode(self, newPreconditionNode):
        """
        Adds new node as a precondition for this node.
        :param newPreconditionNode: node to be added to preconditions
        :return:
        """
        self.preconditions.append(newPreconditionNode)

    def getState(self):
        """
        Returns state of the node.
        :return:
        """
        return self.state

    def activate(self):
        """
        Sets the state to 1 (done)
        :return:
        """
        self.state = 1

    def canBeActivated(self):
        """
        Checks, whether node can be activated(executed),
        based on state of previous nodes. I.e., node can be executed, when all
        its preconditions has been done.
        :return: boolean
        """
        preconditions_met = True

        for preconditionNode in self.preconditions:
            if preconditionNode.getState() == 0:
                preconditions_met = False
                break

        return preconditions_met


def solve():
    """
    Advent Of Code 2018 - Day07 Solution.
    :return: tuple(partOneResult[str], partTwoResult[int])
    """

    def solvePart(workers_count, difficulty_offset, fixed_difficulty):
        """
        Universal solver for both partOne and partTwo of Advent Of Code 2018 - Day07.
        :param workers_count: Number of workers processing the task.
        :param difficulty_offset: Additional time required for each node to complete.
        :return: (str: order in which nodes have been completed, int: time required to complete all nodes)
        """
        # Dict of all nodes
        nodes = {}
        '''
        Worker list description:
        workers[worker][0] -> Node assigned
        workers[worker][1] -> Processing time left on node
        '''
        workers = {idx: [None, 0] for idx in range(workers_count)}

        def getCharPositionInAlpha(char):
            """
            Returns position of a character in alphabet(abcdefghijklmnopqrstuvwxyz), regardless of case.
            :param char: Character to be found
            :return: int, position starting from 1
            """
            ALPHABET = "abcdefghijklmnopqrstuvwxyz"
            return ALPHABET.find(char.lower()) + 1

        def getOrCreateNode(node_name):
            """
            Gets or creates new Node and stores it in nodes dictionary as node_name : Node()
            :param node_name: Name of the node to be created/retrieved in nodes list.
            :return: Node
            """
            try:
                node = nodes[node_name]
            except KeyError:
                node = Node()
                nodes[node_name] = node

            return node

        def workLeft():
            """
            Checks, whether there is any work to do for any worker.
            :return: boolean
            """
            for worker in workers.values():
                if worker[1] > 0:
                    return True
            return False

        # Read puzzle input from file
        puzzle_input = read_puzzle_input(os.path.dirname(os.path.abspath(__file__)), "day07_input.txt")

        # Loop through instructions
        for puzzle_input_line in puzzle_input:
            # Get names of precondition and current node name from puzzle input starting at positions 5 and 36
            node_precondition_name, node_name = puzzle_input_line[5], puzzle_input_line[36]

            # Get or create current and precondition nodes
            current_node = getOrCreateNode(node_name)
            precondition_node = getOrCreateNode(node_precondition_name)

            # Add precondition_node to current_node
            current_node.addPreconditionNode(precondition_node)

        # Sort nodes to assign them in alphabetical order
        sorted_node_names = sorted(nodes.keys())

        # Order in which nodes have been finished
        nodes_execution_order = ""
        '''
        Time passed since start of the job (starts at -1, because the puzzle expects, that work is delivered
        immediatelly after touching it. I.e., worker picks node and has been working on it for second immediately.
        '''
        time_passed = -1

        # Run while there are untouched nodes, or if there are no more untouched, until all workers finish their work
        while len(sorted_node_names) > 0 or workLeft():

            time_passed += 1

            # Decrease timer of each task by one, and mark it finished if applicable

            solved_in_this_tick = ""  # List of nodes, which have been solved in this tick

            for worker in workers:
                # Decrease remaining time on task
                workers[worker][1] -= 1

                # If the task has finished (time remaining is <= 0 and task was assigned before)
                if workers[worker][1] <= 0 and workers[worker][0] is not None:
                    solved_in_this_tick += workers[worker][0]

                    nodes[workers[worker][0]].activate()  # Mark node complete
                    workers[worker][0] = None  # Empty out workers hands

            '''
            In case of multiple nodes have been solved in single tick of game, add the to result in alphabetical order.
            Note: this isn't the case for my puzzle input, but I leave it here, just in case.
            '''
            nodes_execution_order += ''.join(sorted(solved_in_this_tick))

            # Find new job for each worker
            for worker in workers:
                # Remaining time on task <= 0
                if workers[worker][1] <= 0:
                    # Loop through list of nodes and first, which can be activated (preconditions met), assign ot worker
                    for node_name in sorted_node_names:
                        if nodes[node_name].canBeActivated():
                            workers[worker][0] = node_name

                            '''
                            Check partOne or partTwo is solved.
                            In partOne, node is solved immediately after starting work on it (next tick), thus the required time -> 1.
                            In partTwo, difficulty is given by sum of difficulty offset + order of character in alphabet.
                            '''
                            if fixed_difficulty:
                                workers[worker][1] = 1
                            else:
                                workers[worker][1] = getCharPositionInAlpha(node_name) + difficulty_offset

                            sorted_node_names.remove(node_name)
                            break

        return (nodes_execution_order, time_passed)

    def solvePartOne():
        """Advent Of Code 2018 - Day07 - Part One Solution.
        :return: int
        """
        # Solve with 1 worker, 0 difficulty offset, fixed difficulty (Node is solved immediately) + we are interested in execution order only.
        return solvePart(1, 0, True)[0]

    def solvePartTwo():
        """Advent Of Code 2018 - Day07 - Part Two Solution.
        :return: int
        """
        # Solve with 5 workers, 60 difficulty offset, non-fixed difficulty + we are interested in execution time only.
        return solvePart(5, 60, False)[1]

    return (solvePartOne(), solvePartTwo())
