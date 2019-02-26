from commons.commons import read_puzzle_input
import os


class TreeNode():
    def __init__(self):
        self.childNodes = []  # List of children
        self.metaData = []  # List of metadata

    def addChild(self, childNode):
        """
        Adds another TreeNode as a child
        :param childNode[TreeNode]: TreeNode to be added as a child
        :return:
        """
        self.childNodes.append(childNode)

    def addMeta(self, metaDataInfo):
        """
        Adds metaInformation to list of metadata
        :param metaDataInfo[int]: MetaInformation to be added to list of metadata
        :return:
        """
        self.metaData.append(metaDataInfo)

    def getMetaDataSumIncludingChildren(self):
        """
        Calculates "value" of TreeNode according to PartOne - as sum of metaData + value of all children
        :return: [int] value of TreeNode
        """
        metaSum = sum(self.metaData)

        for child in self.childNodes:
            metaSum = metaSum + child.getMetaDataSumIncludingChildren()

        return metaSum

    def getMetaDataReferencingChildrenSum(self):
        """
        Calculates "value" of TreeNode according to PartTwo.
        In case TreeNode has no children, it's value is given by sum of its metaData.
        In case TreeNode has children, it's value is calculated as sum of children referenced by metadata
            (e.g.: metaData of value 3 says : "Include value of third child in value")
            * first child is referenced as 1
            * reference to non-existing (e.g.: fifth child in case node has only three) is considered 0 value
        :return: [int] value of TreeNode
        """
        metaSum = 0
        if len(self.childNodes) == 0:
            metaSum = sum(self.metaData)
        else:

            for metaReference in self.metaData:
                metaReference = metaReference - 1

                if metaReference >= len(self.childNodes) or metaReference < 0:
                    continue

                metaSum = metaSum + self.childNodes[metaReference].getMetaDataReferencingChildrenSum()

        return metaSum


def solve():
    """
    Advent Of Code 2018 - Day08 Solution.
    :return: tuple(partOneResult[str], partTwoResult[int])
    """

    puzzle_input = read_puzzle_input(os.path.dirname(os.path.abspath(__file__)), "day08_input.txt")

    # Converts input to list of integers
    puzzle_input_iter = iter([int(x) for x in puzzle_input[0].split(" ")])

    def deserialize():
        """
        Constructs tree representation of tree defined as text in following format:
        (children_count, metadata_count, [children], [metadata]))
        :return: [TreeNode] - object representation of a Tree
        """

        child_count = next(puzzle_input_iter)  # Read number of children
        meta_count = next(puzzle_input_iter)  # Read number of metadata

        currentNode = TreeNode()  # Construct new TreeNode - current node

        # Deserialize children nodes
        # In case, a node contains children, these precede metadata information
        for i in range(child_count):
            currentNode.addChild(deserialize())

        # Once all children have ben processed, continue reading medatada
        for j in range(meta_count):
            currentNode.addMeta(next(puzzle_input_iter))

        return currentNode

    # Get object representation of a Tree described in puzzle input
    rootNode = deserialize()

    def solvePartOne():
        """Advent Of Code 2018 - Day08 - Part One Solution.
        :return: [int] "value" of tree described in puzzle input as defined in partOne of Day08
        """
        return rootNode.getMetaDataSumIncludingChildren()

    def solvePartTwo():
        """Advent Of Code 2018 - Day08 - Part Two Solution.
        :return: [int] "value" of tree described in puzzle input as defined in partTwo of Day08
        """
        return rootNode.getMetaDataReferencingChildrenSum()

    return (solvePartOne(), solvePartTwo())
