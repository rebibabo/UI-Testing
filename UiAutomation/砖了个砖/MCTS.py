from __future__ import annotations
from uiautomation import PaneControl
from matplotlib.colors import to_rgb, to_hex
from graphviz import Digraph
from Table import NewTable
from math import sqrt, log
from copy import deepcopy
import random

Action = tuple[int]

class TreeNode:
    N: int = 0          # number of visits
    T: int = 0          # total value
    c: float = 2.0      # exploration parameter
    action: Action = [] # the previous action leading to this node
    parent: TreeNode = None
    children: dict[Action, TreeNode] = {}   # children of this node, {action: TreeNode}
    table: NewTable = None   # the game table(state) at this node
    select: bool = False

    def __init__(self,
        table: NewTable,
        parent: TreeNode,
        action: Action
    ) -> None:
        self.table = table
        self.parent = parent
        self.action = action

    @ property
    def UCBscore(self) -> float:        # Upper Confidence Bound (UCB) score
        if self.N == 0:     # avoid divide by zero error
            return float('inf')
        parent = self
        if parent.parent is not None:   # if not root node
            parent = parent.parent
        return (self.T / self.N) + self.c * sqrt(log(parent.N) / self.N)  # T/N + c * sqrt(log(parent.N) / N)

    def detach_parent(self) -> None:    # detach this node from its parent
        del self.parent
        self.parent = None

    def _create_children(self):         # spread operation, create children of this node
        if self.table.done:
            return
        children = {}
        for action in self.table.actions:
            new_table = deepcopy(self.table)
            succ = new_table.step(*action)     # apply action to the table
            if succ:
                child = TreeNode(new_table, self, action)
                children[action] = child
        self.children = children

    def explore(self) -> None:      # select the root's best child node to explore
        current = self
        current.select = True
        while current.children:
            children = current.children
            scores = [child.UCBscore for child in children.values()]
            max_score = max(scores)
            actions = [action for action, score in zip(children.keys(), scores) if score == max_score]  # get all actions with max score
            action = random.choice(actions)     # randomly select one action with max score
            current = children[action]
            current.select = True
        
        if current.N > 0:    # if current node has been visited before
            current._create_children()   # create children of current node
            if current.children:
                current = random.choice(list(current.children.values()))
                current.select = True
        current.T += current.rollout()  # simulate the game from current node to the end
        current.N += 1                # update visit count and total value of current node
        parent = current
        while parent.parent is not None:        # update visit count and total value of all ancestors
            parent = parent.parent
            parent.N += 1
            parent.T += current.T

    def rollout(self) -> int:       # simulate the game from current node to the end
        if self.table.done:
            return 0
        v = 0
        table = deepcopy(self.table)
        while not table.done:       # simulate random step until the game is done
            actions = table.actions
            action = random.choice(actions)
            succ = table.step(*action)
            if not succ:
                break
            v += 1
        return v

    def next(self) -> TreeNode:     # select the best child node to play next
        max_N = max(child.N for child in self.children.values())
        max_children = [child for child in self.children.values() if child.N == max_N]
        random_child = random.choice(max_children)
        return random_child

    def _color(self, color: str, node: TreeNode) -> str:
        if node.N == 0:
            return "#ffffff"
        rgb = to_rgb(color)
        UCB = node.UCBscore
        parent = node
        if node.parent:
            parent = node.parent
        ratio = UCB / (node.table.max_grade + node.c * sqrt(log(parent.N) / node.N))
        diff = [1 - x for x in rgb]
        new_rgb = [x + y * ratio for x, y in zip(rgb, diff)]
        return to_hex(new_rgb)

    def show(self, color='red'):
        dot: Digraph = Digraph(comment='MCTS')   # for visualization
        self._show(self, dot, color)
        dot = dot.unflatten(stagger=6)
        dot.render('MCTS.gv', view=True)

    def _show(self, node: TreeNode, dot: Digraph, color: str, is_max: bool=False) -> None:
        dot.node(str(id(node)), 
            label=f"N={node.N}\nT={node.T}\nUCB={node.UCBscore:.2f}", 
            shape='box', 
            style='filled', 
            fillcolor=self._color(color, node),
            color=color if is_max else 'black',
            penwidth="2" if is_max else "1")
        node.select = False
        max_val = max([0] + [child.UCBscore for child in node.children.values()])
        for child in node.children.values():
            dot.edge(str(id(node)), str(id(child)), 
                label=str(child.action), 
                color=color if child.select else 'black',
                penwidth="2" if child.select else "1")
            is_max = child.UCBscore == max_val
            self._show(child, dot, color, is_max)

def MCTS(root: TreeNode, n_iters: int) -> TreeNode: # Monte Carlo Tree Search
    for _ in range(n_iters):
        root.explore()
    next_node = root.next()
    next_node.detach_parent()
    return next_node

if __name__ == '__main__':
    iters = 10
    child_iters = 10
    total_grade = 0
    for i in range(iters):
        grade = 0
        table = NewTable(load_from_pic=True)
        new_table = deepcopy(table)
        root = TreeNode(new_table, None, None)
        root_copy = deepcopy(root)
        print(f"Iteration {i+1}/{iters}")
        while not table.done:
            root = MCTS(root, child_iters)
            table.step(*root.action)
            grade += 1
            print(f"iter {i+1}: {grade}")
        print(f"Grade: {grade}")
        total_grade += grade
    print(f"Average Grade: {total_grade/iters}")
