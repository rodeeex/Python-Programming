"""
TODO: последовательный юзерский ввод из параметров, которые добавляются в кортеж и потом, в распакованном виде, передаются в аргументы конструктора BinTree. Отлавливаю ValueError.
Функции для левого и правого листьев определяю отдельно в этом файле. И спрашиваю юзера - использовать предложенные функции отсюда или взять те, что по умолчанию?
"""

import json

from tree import BinTree

tree = BinTree()

tree_dict = tree.convert("dict")
print("Дерево в виде словаря:")
print(json.dumps(tree_dict, indent=4))

tree_list = tree.convert("list")
print("\nДерево в виде списка:")
print(*tree_list)
