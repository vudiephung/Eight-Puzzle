class Node(object):
    childrens = []
    parent = None
    puzzle = []
    blank_index = 0
    col = 3

    def __init__(self, puzzle):
        self.puzzle = []
        for el in puzzle:
            self.puzzle.append(el)

    # Copy from a to b
    def copy_puzzle(self, old, new):
        for el in old:
            new.append(el)

    def goal_test(self):
        isGoal = True
        temp = self.puzzle[0]
        for i in range(1, len(self.puzzle)):
            if (temp > self.puzzle[i]):
                isGoal = False
                break
            temp = self.puzzle[i]
        return isGoal

    def move_up(self, index):
        if index - self.col >= 0:
            newPuzzle = []
            self.copy_puzzle(self.puzzle, newPuzzle)
            newPuzzle[index], newPuzzle[index - 3] = newPuzzle[index - 3], newPuzzle[index]
            child = Node(newPuzzle)
            self.childrens.append(child)
            child.parent = self

    def move_down(self, index):
        if index + self.col < len(self.puzzle):
            newPuzzle = []
            self.copy_puzzle(self.puzzle, newPuzzle)
            newPuzzle[index], newPuzzle[index + 3] = newPuzzle[index + 3], newPuzzle[index]
            child = Node(newPuzzle)
            self.childrens.append(child)
            child.parent = self

    # Move 0 to the left
    def move_left(self, index):
        if index % self.col > 0:
            newPuzzle = []
            self.copy_puzzle(self.puzzle, newPuzzle)
            newPuzzle[index], newPuzzle[index - 1] = newPuzzle[index - 1], newPuzzle[index]
            child = Node(newPuzzle)
            self.childrens.append(child)
            child.parent = self

    # Move 0 to the right
    def move_right(self, index):
        if index % self.col < 2:
            newPuzzle = []
            self.copy_puzzle(self.puzzle, newPuzzle)
            newPuzzle[index], newPuzzle[index + 1] = newPuzzle[index + 1], newPuzzle[index]
            child = Node(newPuzzle)
            self.childrens.append(child)
            child.parent = self

    def print_puzzle(self):
        print()
        for i in range(len(self.puzzle)):
            print(self.puzzle[i], "", end='')
            if (i + 1) % self.col == 0 and not (i + 1) == len(self.puzzle):
                print()

    def is_same_puzzle(self, puzzle):
        return self.puzzle == puzzle

    def expand_move(self):
        self.childrens = []
        self.blank_index = self.puzzle.index(0)

        if self.blank_index % self.col == 1:
            self.move_left(self.blank_index)
            self.move_right(self.blank_index)
        elif self.blank_index % self.col == 0:
            self.move_right(self.blank_index)
        elif self.blank_index % self.col == self.col - 1:
            self.move_left(self.blank_index)

        if self.blank_index // self.col == 0:
            self.move_down(self.blank_index)
        elif self.blank_index // self.col == self.col - 1:
            self.move_up(self.blank_index)
        else:
            self.move_up(self.blank_index)
            self.move_down(self.blank_index)


class UniformSearch:
    def BFS(self, root):
        pathToSolution = []
        openList = []
        closedList = []

        openList.append(root)
        foundGoal = False

        print("Searching for the solution ... ")
        while openList and not foundGoal:
            currentNode = openList[0]
            closedList.append(currentNode)
            openList.pop(0)

            currentNode.expand_move()

            for childNode in currentNode.childrens:
                if childNode.goal_test():
                    print("Result found!")
                    foundGoal = True
                    self.path_trace(pathToSolution, childNode)
                    break
                if not self.existed_puzzle(childNode, openList) and not self.existed_puzzle(childNode, closedList):
                    openList.append(childNode)

        return pathToSolution

    def path_trace(self, path, child):
        print("Tracing path...")
        current = child
        path.append(current)
        while current.parent:
            current = current.parent
            path.append(current)

    def existed_puzzle(self, myNode, nodeList):
        isContain = False
        for node in nodeList:
            if node.is_same_puzzle(myNode.puzzle):
                isContain = True
                break
        return isContain

if __name__ == "__main__":
    puzzle = [
        1, 2, 4,
        3, 0, 5,
        7, 6, 8
    ]

    goal = [
        1, 0, 4, 3, 2, 5, 6, 7, 8
    ]

    root = Node(puzzle)

    ui = UniformSearch()
    solution = ui.BFS(root)

    if solution:
        solution.reverse()
        for node in solution:
            node.print_puzzle()
            if solution.index(node) < len(solution) - 1:
                print();