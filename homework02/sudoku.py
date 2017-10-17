import random
from pprint import pprint as pp
from collections import Counter


def read_sudoku(filename):
    """ Прочитать Судоку из указанного файла """
    digits = [c for c in open(filename).read() if c in '123456789.']
    grid = group(digits, 9)
    return grid


def display(values):
    """Вывод Судоку """
    width = 2
    line = '+'.join(['-' * (width * 3)] * 3)
    for row in range(9):
        print(''.join(values[row][col].center(width) +
                      ('|' if str(col) in '25' else '') for col in range(9)))
        if str(row) in '25':
            print(line)
    print()


def group(values, n):
    """
    Сгруппировать значения values в список, состоящий из списков по n элементов
    >>> group([1,2,3,4], 2)
    [[1, 2], [3, 4]]
    >>> group([1,2,3,4,5,6,7,8,9], 3)
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    """
    return [values[i * n: i * n + n] for i in range(n)]


def get_row(values, pos):
    """ Возвращает все значения для номера строки, указанной в pos
    >>> get_row([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '2', '.']
    >>> get_row([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (1, 0))
    ['4', '.', '6']
    >>> get_row([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (2, 0))
    ['.', '8', '9']
    """
    return values[pos[0]]


def get_col(values, pos):
    """ Возвращает все значения для номера столбца, указанного в pos
    >>> get_col([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '4', '7']
    >>> get_col([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (0, 1))
    ['2', '.', '8']
    >>> get_col([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (0, 2))
    ['3', '6', '9']
    """
    return [values[i][pos[1]] for i in range(len(values))]


def get_block(values, pos):

    """ Возвращает все значения из того квадрата, в который попадает
    позиция pos """
    """ Счет pos ведется с нуля!!! (pos = x,y в сетке) """

    """ --------------------- """
    """ цикл для группировки эл-ов по 3 внутри сетки (при условии,
    если эл-ты не сгруппированы) """
    r = 3 * (pos[0] // 3)
    c = 3 * (pos[1] // 3)
    return [values[r+i][c+j] for i in range(3) for j in range(3)]


def find_empty_positions(grid):
    """ Найти первую свободную позицию в пазле
    >>> find_empty_positions([['1', '2', '.'], +\
    ['4', '5', '6'], ['7', '8', '9']])
    (0, 2)
    >>> find_empty_positions([['1', '2', '3'], +\
    ['4', '.', '6'], ['7', '8', '9']])
    (1, 1)
    >>> find_empty_positions([['1', '2', '3'], +\
    ['4', '5', '6'], ['.', '8', '9']])
    (2, 0)
    """
    for i in range(len(grid)):
        for j in range(len(grid)):
            if grid[i][j] == '.':
                return (i, j)
    return -1


def find_possible_values(grid, pos):
    """ Вернуть все возможные значения для указанной позиции """
    return set('123456789') - set(get_row(grid, pos)) - set(get_col(grid, pos)) - set(get_block(grid, pos))    


def solve(grid):
    """ Решение пазла, заданного в grid """
    """ Как решать Судоку?
        1. Найти свободную позицию
        2. Найти все возможные значения, которые могут
        находиться на этой позиции
        3. Для каждого возможного значения:
            3.1. Поместить это значение на эту позицию
            3.2. Продолжить решать оставшуюся часть пазла
    """
    pos = find_empty_positions(grid)
    if pos == -1:
        return grid
    values = find_possible_values(grid, pos)
    if not values:
        return None
    for i in values:
        grid[pos[0]][pos[1]] = i
        ans = solve(grid)
        if ans is not None:
            return ans
    grid[pos[0]][pos[1]] = '.'
    return None


def check_solution(solution):
    """ Если решение solution верно, то вернуть True,
    в противном случае False """
    for i in range(9):
        row_values = set('123456789')
        col_values = set('123456789')
        block_values = set('123456789')
        row_solution_values = set(get_row(solution, (i, 0)))
        col_solution_values = set(get_col(solution, (0, i)))
        row_values -= row_solution_values
        col_values -= col_solution_values
        if row_values or col_values:
            return False
    for i in range(3):
        for j in range(3):
            block_solution_values = set(get_block(solution, (i, j)))
            block_values -= block_solution_values
            if block_values != set():
                return False
    return True


def generate_sudoku(N):
    """ Генерация судоку заполненного на N элементов
        >>> grid = generate_sudoku(40)
        >>> sum(1 for row in grid for e in row if e == '.')
        41
        >>> solution = solve(grid)
        >>> check_solution(solution)
        True
        >>> grid = generate_sudoku(1000)
        >>> sum(1 for row in grid for e in row if e == '.')
        0
        >>> solution = solve(grid)
        >>> check_solution(solution)
        True
        >>> grid = generate_sudoku(0)
        >>> sum(1 for row in grid for e in row if e == '.')
        81
        >>> solution = solve(grid)
        >>> check_solution(solution)
        True
    """
    N = 81 - N
    grid = [['.' for i in range(9)] for j in range(9)]
    grid = solve(grid)
    for elem in range(N):
        row = random.randrange(0, 9)
        col = random.randrange(0, 9)
        while grid[row][col] == '.':
            row = random.randrange(0, 9)
            col = random.randrange(0, 9)
        grid[row][col] = '.'
    return grid

if __name__ == '__main__':
    for fname in ['puzzle1.txt', 'puzzle2.txt', 'puzzle3.txt']:
        grid = read_sudoku(fname)
        display(grid)
        solution = solve(grid)
        display(solution)
