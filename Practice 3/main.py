"""
Раз функции - это объекты первого класса и их можно хранить в словарях, я решил возвращать в helper() именованные параметры.
Это позволит избирательно передавать исходные параметры в дерево.

TODO: написать документацию к функциям
"""
import json
from tree import BinTree


def left_leaf(value: float) -> float:
    return value * 2


def right_leaf(value: float) -> float:
    return value * 2 + 1


def helper():
    root_val_input = input('Введите значение корня дерева (пропустите, чтобы использовать 10): ')
    if root_val_input != '':
        try:
            root_val = float(root_val_input)
        except ValueError:
            raise ValueError('Неверное значение! Корень дерева - это вещественное число.')
    else:
        root_val = ''

    height_input = input('Введите высоту дерева (пропустите, чтобы использовать 5): ')
    if height_input != '':
        try:
            height = int(height_input)
        except ValueError:
            raise ValueError('Неверное значение! Высота дерева - это целое положительное число.')
        if int(height_input) < 0:
            raise ValueError('Неверное значение! Высота дерева не может быть меньше 1.')
    else:
        height = ''

    print(' -> Стандартные функции для листьев: left_leaf = 3 * root + 1, right_leaf = 3 * root - 1')
    use_custom_leaf_functions = input(
        'Использовать определённые в файле функции (y) или оставить стандартные (n)? ')
    if use_custom_leaf_functions == 'y':
        count_left_leaf_function, count_right_leaf_function = left_leaf, right_leaf
    elif use_custom_leaf_functions == 'n':
        count_left_leaf_function, count_right_leaf_function = None, None
    else:
        raise ValueError(
            'Неверное значение! Использовать определённые в файле функции - y, оставить стандартные - n.')

    recursive_input = input('Использовать рекурсию при построении дерева? (y [по умолчанию]/n) ')
    if recursive_input == 'y':
        is_recursive = True
    elif recursive_input == 'n':
        is_recursive = False
    else:
        raise ValueError(
            'Неверное значение! Использовать рекурсию при построении дерева - y, не использовать - n.')

    use_recursive_dict_input = input('Использовать рекурсию при ВЫВОДЕ дерева? (y/n) ')
    if use_recursive_dict_input == 'y':
        use_recursive_dict = True
    elif use_recursive_dict_input == 'n':
        use_recursive_dict = False
    else:
        raise ValueError('Неверное значение! Использовать рекурсию при ВЫВОДЕ дерева - y, не использовать - n.')

    params = dict()

    if root_val != '':
        params['root_val'] = root_val
    if height_input != '':
        params['height'] = height
    if use_custom_leaf_functions == 'y':
        params['count_left_leaf_function'] = count_left_leaf_function
        params['count_right_leaf_function'] = count_right_leaf_function
    if not is_recursive:
        params['is_recursive'] = is_recursive

    return params, use_recursive_dict


def main():
    params = helper()
    tree = BinTree(**params[0])

    tree_dict = tree.convert('dict_recursive') if params[1] else tree.convert('dict')
    print('Дерево в виде словаря:')
    print(json.dumps(tree_dict, indent=4))

    tree_list = tree.convert('list')
    print('\nДерево в виде списка:')
    print(*tree_list)


if __name__ == '__main__':
    main()
