import os


def cls():
    """
    Очистить содержимое консоли.
    """
    os.system('cls' if os.name == 'nt' else 'clear')
