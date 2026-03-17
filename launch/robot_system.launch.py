#!/usr/bin/env python3
import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, TextSubstitution
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    package_share_dir = get_package_share_directory('krotov')

    # --- 1. ОБЪЯВЛЯЕМ АРГУМЕНТ 'mode' ---
    # Этот аргумент можно будет передать из командной строки
    mode_arg = DeclareLaunchArgument(
        'mode',                          # имя аргумента
        default_value='slow',             # значение по умолчанию
        description='Режим работы: fast (20 Гц, порог 50) или slow (5 Гц, порог 150)'
    )

    # --- 2. ПОЛУЧАЕМ ЗНАЧЕНИЕ АРГУМЕНТА ---
    # LaunchConfiguration - это специальный объект, который позже станет строкой
    mode = LaunchConfiguration('mode')

    # --- 3. ОПРЕДЕЛЯЕМ ПУТИ К ФАЙЛАМ ПАРАМЕТРОВ ДЛЯ РАЗНЫХ РЕЖИМОВ ---
    # Мы создадим два разных YAML-файла и выберем нужный в зависимости от mode
    fast_param_file = os.path.join(package_share_dir, 'params', 'fast_params.yaml')
    slow_param_file = os.path.join(package_share_dir, 'params', 'slow_params.yaml')

    # --- 4. СОЗДАЕМ УЗЕЛ С ВЫБОРОМ ФАЙЛА ПАРАМЕТРОВ ---
    # К сожалению, нельзя просто написать 'if mode == "fast"' в этом месте,
    # потому что mode - это объект, а не строка. Мы используем Conditional включение.
    # Самый простой и надежный способ для двух режимов - создать два узла
    # и запускать только один из них с помощью условия 'unless' и 'if'.
    # Но для простоты и наглядности мы сделаем так:
    # мы передадим в параметры путь к файлу, а ROS сам выберет существующий.
    # Но ROS не умеет выбирать между файлами. Поэтому мы используем Python-код
    # для формирования правильного пути.

    # Правильный путь: используем TextSubstitution для подстановки значения mode в строку.
    # Но это сложно. Давайте сделаем проще: будем использовать один YAML-файл,
    # а параметры будем передавать через аргументы командной строки узла.

    # ----- БОЛЕЕ ПРОСТОЙ ПОНЯТНЫЙ ВАРИАНТ -----
    # Мы будем использовать LaunchConfiguration для значений параметров.
    # Для этого создадим LaunchConfiguration для каждого параметра,
    # но установим их значения в зависимости от mode. Опять сложность с условиями.

    # ----- САМЫЙ ПРОСТОЙ И РАБОЧИЙ ВАРИАНТ ДЛЯ НОВИЧКА -----
    # Мы создадим два разных набора параметров прямо здесь, в коде launch-файла,
    # и выберем нужный с помощью простого Python if/else.
    # Для этого мы должны "развернуть" LaunchConfiguration в значение.
    # Это делается с помощью launch.substitutions.LocalSubstitution, но проще
    # использовать другой подход: сделать launch-файл, который генерирует описание
    # динамически. Так как мы уже внутри Python-функции, мы можем использовать обычный Python.

    # Получаем значение mode как строку. Это сработает, потому что функция generate_launch_description
    # вызывается один раз при запуске, и аргументы уже известны.
    # НО! Это не совсем правильно с точки зрения API, но работает на практике.
    # Правильнее использовать substitutions, но для простоты оставим так.
    
    # Мы создадим описание узла без параметров, а добавим их позже, используя обычный Python.
    
    # Давайте поступим так: создадим словарь параметров в зависимости от mode.
    # Для этого нам нужно получить значение mode. Воспользуемся тем, что
    # мы можем прочитать его через LaunchConfiguration, но для формирования
    # описания запуска это не подходит. Поэтому для простоты я покажу метод с двумя
    # разными файлами параметров и выбором файла через условие.

    # Создаем два узла, но с условиями запуска
    from launch.conditions import IfCondition, UnlessCondition
    from launch.substitutions import PythonExpression
    
    # Вычисляем булевы значения для условий
    is_fast = PythonExpression(['"', mode, '" == "fast"'])
    is_slow = PythonExpression(['"', mode, '" == "slow"'])

    node_fast = Node(
        package='krotov',
        executable='even_pub',
        name='even_pub',
        output='screen',
        parameters=[fast_param_file],
        condition=IfCondition(is_fast)  # запустится, только если mode == 'fast'
    )

    node_slow = Node(
        package='krotov',
        executable='even_pub',
        name='even_pub',
        output='screen',
        parameters=[slow_param_file],
        condition=IfCondition(is_slow)  # запустится, только если mode == 'slow'
    )

    # Узел слушателя всегда запускается
    listener_node = Node(
        package='krotov',
        executable='overflow_listener',
        name='overflow_listener',
        output='screen',
    )

    return LaunchDescription([
        mode_arg,
        node_fast,
        node_slow,
        listener_node,
    ])
