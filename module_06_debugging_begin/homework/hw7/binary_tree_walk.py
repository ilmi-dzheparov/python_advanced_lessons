"""
Помимо того чтобы логи писать, нужно их ещё и уметь читать,
иначе мы будем как в известном анекдоте, писателями, а не читателями.

Для вас мы написали простую функцию обхода binary tree по уровням.
Также в репозитории есть файл с логами, написанными этой программой.

Напишите функцию restore_tree, которая принимает на вход путь до файла с логами
    и восстанавливать исходное BinaryTree.

Функция должна возвращать корень восстановленного дерева

def restore_tree(path_to_log_file: str) -> BinaryTreeNode:
    pass

Примечание: гарантируется, что все значения, хранящиеся в бинарном дереве уникальны
"""
import itertools
import logging
import random
from collections import deque
from dataclasses import dataclass
from typing import Optional, List
import re

logger = logging.getLogger("tree_walk")


@dataclass
class BinaryTreeNode:
    val: int
    left: Optional["BinaryTreeNode"] = None
    right: Optional["BinaryTreeNode"] = None

    def __repr__(self):
        return f"<BinaryTreeNode[{self.val}]>"


def walk(root: BinaryTreeNode):
    queue = deque([root])

    while queue:
        node = queue.popleft()

        logger.info(f"Visiting {node!r}")

        if node.left:
            logger.debug(
                f"{node!r} left is not empty. Adding {node.left!r} to the queue"
            )
            queue.append(node.left)

        if node.right:
            logger.debug(
                f"{node!r} right is not empty. Adding {node.right!r} to the queue"
            )
            queue.append(node.right)


counter = itertools.count(random.randint(1, 10 ** 6))


def get_tree(max_depth: int, level: int = 1) -> Optional[BinaryTreeNode]:
    if max_depth == 0:
        return None

    node_left = get_tree(max_depth - 1, level=level + 1)
    node_right = get_tree(max_depth - 1, level=level + 1)
    node = BinaryTreeNode(val=next(counter), left=node_left, right=node_right)

    return node


def restore_tree(path_to_log_file: str) -> BinaryTreeNode:
    def find_node(line: str) -> List[str]:
        rule = r'\[([^\]]+)\]'
        pattern = re.compile(rule)
        return pattern.findall(line)

    nodes_dict = dict()
    with open(path_to_log_file, 'r') as file:
        lines = file.readlines()

    for i in range(len(lines) - 1 , -1, -1):

        if lines[i].split(":")[0] == "DEBUG":
            nodes_in_line = find_node(lines[i])
            node_father = int(nodes_in_line[0])
            node_child: int = int(nodes_in_line[1])
            if node_father not in nodes_dict:
                nodes_dict[node_father] = {"value": None, "left": None, "right": None}
            if lines[i].split()[1] == 'left':
                nodes_dict[node_father]["left"] = nodes_dict[node_child]["value"]
            if lines[i].split()[1] == 'right':
                nodes_dict[node_father]["right"] = nodes_dict[node_child]["value"]
        if lines[i].split(":")[0] == "INFO":
            node = int(find_node(lines[i])[0])
            if node not in nodes_dict:
                nodes_dict[node] = {"value": BinaryTreeNode(val=node, left=None, right=None), "left": None, "right": None}
            else:
                nodes_dict[node]["value"] = BinaryTreeNode(val=node, left=nodes_dict[node]["left"], right=nodes_dict[node]["right"])

    return nodes_dict[node]["value"]



if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(levelname)s:%(message)s",
        filename="walk_log_5.txt",
        filemode='w'
    )

    root = get_tree(3, 1)
    # walk(root)
    # restore_tree("walk_log_1.txt")
    root_2 = restore_tree("walk_log_3.txt")
    print(root_2)
    walk(root_2)