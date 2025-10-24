"""
Вариант 10 (Root = 10; height = 5, left_leaf = root * 3 + 1, right_leaf = 3 * root - 1)

Дерево хранится в виде объектов, ссылающихся на дочерние. Параметры по умолчанию вывел на самый верхний уровень,
т.е. в BinTree.
"""

from typing import Callable, Literal
from collections import deque


class TreeNode:
    """
    Класс для хранения информации об одном элементе дерева
    """

    def __init__(self, value: float, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


class BinTree:
    """
    Класс для хранения бинарного дерева. При создании вызывает метод из TreeGenerator.
    Значения по умолчанию написаны в конструкторе. Для использования разных структур вывода определён тип OutputStruct.
    """
    type OutputStruct = Literal['dict', 'dict_recursive', 'list']

    def __init__(self, root_val: float = 10, height: int = 5,
                 count_left_leaf_function: Callable[[float], float] = lambda value: value * 3 + 1,
                 count_right_leaf_function: Callable[[float], float] = lambda value: 3 * value - 1,
                 is_recursive: bool = False):
        self.height = height

        generator = TreeGenerator(count_left_leaf_function, count_right_leaf_function)
        self.root = generator.generate(root_val, height, is_recursive)


class TreeGenerator:
    """
    Класс для создания дерева. Поддерживает рекурсивную и нерекурсивную генерацию.
    """

    def __init__(self, count_left_leaf_function: Callable, count_right_leaf_function: Callable):
        """
        Конструктор генератора дерева. Позволяет передать функции для вычисления значений листьев.

        :param count_left_leaf_function: функция для вычисления значения левого листа
        :param count_right_leaf_function: функция для вычисления значения правого листа
        """
        self.count_left_leaf = count_left_leaf_function
        self.count_right_leaf = count_right_leaf_function

    def generate(self, root_val: float, height: int, is_recursive: bool) -> TreeNode:
        """
        Общая функция для генерации дерева. Создаёт корень и генерирует на его основе потомков всех уровней.

        :param root_val: значение корня дерева
        :param height: высота дерева
        :param is_recursive: рекурсивное (True) или нерекурсивное (False) создание
        :return:
        """
        root = TreeNode(root_val)
        if is_recursive:
            self.generate_recursive(root, height)
        else:
            self.generate_non_recursive(root, height)
        return root

    def generate_recursive(self, current_node: TreeNode, height: int):
        """
        Создать дерево рекурсивно.

        :param current_node: текущий узел, от которого строится дерево
        :param height: высота дерева
        """
        if height <= 1:
            return
        current_node.left = TreeNode(value=self.count_left_leaf(current_node.value))
        current_node.right = TreeNode(value=self.count_right_leaf(current_node.value))
        self.generate_recursive(current_node.left, height - 1)
        self.generate_recursive(current_node.right, height - 1)

    def generate_non_recursive(self, root: TreeNode, height: int):
        """
        Создать дерево нерекурсивно, используя очередь.

        :param root: корень дерева (объект)
        :param height: высота дерева
        """
        tree_queue = deque([(root, 1)])
        while tree_queue:
            node, level = tree_queue.popleft()
            if level >= height:
                continue
            node.left = TreeNode(value=self.count_left_leaf(node.value))
            node.right = TreeNode(value=self.count_right_leaf(node.value))
            tree_queue.append((node.left, level + 1))
            tree_queue.append((node.right, level + 1))
