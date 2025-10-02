"""
Вариант 10 (Root = 10; height = 5, left_leaf = root * 3 + 1, right_leaf = 3 * root - 1)

Дерево хранится в виде объектов, ссылающихся на дочерние. Параметры по умолчанию вывел на самый верхний уровень,
т.е. в BinTree. При этом, и создание бинарного дерева, и его вывод в виде словаря можно выполнить
рекурсивным или нерекурсивным путём (через очередь). Также возможен вывод в виде списка.

TODO: написать документацию к функциям
"""

from typing import Callable, Literal, Optional
from collections import deque


class TreeNode:
    def __init__(self, value: float, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


class BinTree:
    type OutputStruct = Literal['dict', 'dict_recursive', 'list']

    def __init__(self, root_val: float = 10, height: int = 5,
                 count_left_leaf_function: Callable[[float], float] = lambda value: value * 3 + 1,
                 count_right_leaf_function: Callable[[float], float] = lambda value: 3 * value - 1,
                 is_recursive: bool = False):
        self.height = height

        generator = TreeGenerator(count_left_leaf_function, count_right_leaf_function)
        self.root = generator.generate(root_val, height, is_recursive)

    def to_dict(self, root: TreeNode = None) -> dict:
        if root is None:
            return None

        tree = dict()
        queue = deque([(root, tree)])

        while queue:
            current_node, current_dict = queue.popleft()
            if current_node is None:
                continue

            current_dict['value'] = current_node.value
            current_dict['left'] = dict() if current_node.left else None
            current_dict['right'] = dict() if current_node.right else None

            if current_node.left:
                queue.append((current_node.left, current_dict['left']))
            if current_node.right:
                queue.append((current_node.right, current_dict['right']))

        return tree

    def to_dict_recursive(self, node: TreeNode = None) -> dict:
        if node is None:
            return None
        return {
            'value': node.value,
            'left': self.to_dict_recursive(node.left),
            'right': self.to_dict_recursive(node.right)
        }

    def to_list(self, node: TreeNode = None) -> list:
        if node is None:
            node = self.root
            if node is None:
                return list()
        tree = list()
        queue = deque([node])
        while queue:
            current_node = queue.popleft()
            tree.append(current_node.value)
            if current_node.left:
                queue.append(current_node.left)
            if current_node.right:
                queue.append(current_node.right)
        return tree

    def convert(self, data_struct: OutputStruct = 'dict') -> dict | list:
        if data_struct == 'dict':
            return self.to_dict(self.root)
        elif data_struct == 'dict_recursive':
            return self.to_dict_recursive(self.root)
        elif data_struct == 'list':
            return self.to_list()
        else:
            raise ValueError('Неправильная структура данных для вывода. Поддерживаются dict (по умолчанию) / dict_recursive / list.')


class TreeGenerator:
    def __init__(self, count_left_leaf_function: Callable, count_right_leaf_function: Callable):
        self.count_left_leaf = self.validate_function(count_left_leaf_function)
        self.count_right_leaf = self.validate_function(count_right_leaf_function)

    @staticmethod
    def validate_function(func: Callable[[float], float]) -> Callable[[float], float]:
        try:
            result = func(2.77)
        except Exception as e:
            raise TypeError(f'Функции для вычисления листьев должны принимать один аргумент float')

        if not isinstance(result, (int, float)):
            raise TypeError(f'Функции для вычисления листьев должны возвращать float, возвращено {type(result).__name__}')
        return func

    def generate(self, root_val: float, height: int, is_recursive: bool) -> TreeNode:
        root = TreeNode(root_val)
        if is_recursive:
            self.generate_recursive(root, height)
        else:
            self.generate_non_recursive(root, height)
        return root

    def generate_recursive(self, current_node: TreeNode, height: int):
        if height <= 1:
            return
        current_node.left = TreeNode(value=self.count_left_leaf(current_node.value))
        current_node.right = TreeNode(value=self.count_right_leaf(current_node.value))
        self.generate_recursive(current_node.left, height - 1)
        self.generate_recursive(current_node.right, height - 1)

    def generate_non_recursive(self, root: TreeNode, height: int):
        tree_queue = deque([(root, 1)])
        while tree_queue:
            node, level = tree_queue.popleft()
            if level >= height:
                continue
            node.left = TreeNode(value=self.count_left_leaf(node.value))
            node.right = TreeNode(value=self.count_right_leaf(node.value))
            tree_queue.append((node.left, level + 1))
            tree_queue.append((node.right, level + 1))