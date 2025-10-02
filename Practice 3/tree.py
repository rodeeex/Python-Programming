"""
Вариант 10 (Root = 10; height = 5, left_leaf = root * 3 + 1, right_leaf = 3 * root - 1)

Дерево хранится в виде объектов, ссылающихся на дочерние. Параметры по умолчанию вывел на самый верхний уровень,
т.е. в BinTree. При этом, и создание бинарного дерева, и его вывод в виде словаря можно выполнить
рекурсивным или нерекурсивным путём (через очередь). Также возможен вывод в виде списка.
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

    def to_dict(self) -> dict:
        """
        Преобразовать дерево в словарь (нерекурсивно), используя для этого очередь.

        :return tree: дерево в виде словаря
        """
        if self.root is None:
            return dict()

        tree = {}  # Словарь для представления дерева
        tree_queue = deque([(self.root, tree)])  # Очередь узлов и соответствующих словарей

        while tree_queue:
            current_node, current_dict = tree_queue.popleft()

            if current_node is None:
                continue

            current_dict['value'] = current_node.value
            current_dict['left'] = {} if current_node.left else None
            current_dict['right'] = {} if current_node.right else None

            if current_node.left:
                tree_queue.append((current_node.left, current_dict['left']))
            if current_node.right:
                tree_queue.append((current_node.right, current_dict['right']))

        return tree

    def to_dict_recursive(self, node: TreeNode = None) -> dict:
        """
        Преобразовать дерево в словарь, используя рекурсию.

        :param node: текущий элемент, от которого строится дерево
        :return: дерево в виде словаря
        """
        if node is None:
            return None
        return {
            'value': node.value,
            'left': self.to_dict_recursive(node.left),
            'right': self.to_dict_recursive(node.right)
        }

    def to_list(self) -> list:
        """
        Преобразовать дерево в список (нерекурсивно) путём обхода в ширину.

        :return tree: список значений элементов дерева
        """
        if self.root is None:
            return list()

        tree = list()
        tree_queue = deque([self.root])

        while tree_queue:
            current_node = tree_queue.popleft()
            tree.append(current_node.value)
            if current_node.left:
                tree_queue.append(current_node.left)
            if current_node.right:
                tree_queue.append(current_node.right)
        return tree

    def convert(self, data_struct: OutputStruct = 'dict') -> dict | list:
        """
        Конвертировать дерево в разные структуры данных.

        :param data_struct: структура данных, в которую нужно преобразовать дерево.
        Поддерживаемые преобразования: "dict" (нерекурсивно в словарь), "dict_recursive" (рекурсивно в словарь), "list" (нерекурсивно в список)
        :return: список или словарь
        """
        if data_struct == 'dict':
            return self.to_dict()
        elif data_struct == 'dict_recursive':
            return self.to_dict_recursive(self.root)
        elif data_struct == 'list':
            return self.to_list()
        else:
            raise ValueError(
                'Неправильная структура данных для вывода. Поддерживаются dict (по умолчанию) / dict_recursive / list.')


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
        self.count_left_leaf = self.validate_function(count_left_leaf_function)
        self.count_right_leaf = self.validate_function(count_right_leaf_function)

    @staticmethod
    def validate_function(func: Callable[[float], float]) -> Callable[[float], float]:
        """
        Валидировать функцию для вычисления значения листа на предмет неправильной сигнатуры и возвращаемого значения.

        Примечание: функции могут принимать на вход одно число и возвращать также одно число.

        :param func: функция, которую нужно проверить
        :return: эта же функция, если проверка не выбросила исключение
        :raise: TypeError: неправильная сигнатура или возвращаемое значение
        """
        try:
            result = func(2.77)
        except Exception as e:
            raise TypeError(f'Функции для вычисления листьев должны принимать один аргумент float')

        if not isinstance(result, (int, float)):
            raise TypeError(
                f'Функции для вычисления листьев должны возвращать float, возвращено {type(result).__name__}')
        return func

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