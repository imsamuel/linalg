#!/usr/bin/env python3
"""
Module Docstring
"""

__author__ = "Samuel Yap Woon Pin"
__version__ = "0.1.0"
__license__ = "MIT"

from fractions import Fraction
from tabulate import tabulate


def sumRows(r1, r2):
    """Sums the elements of two rows from a matrix.

    Args:
        r1 (List[Fraction]): A matrix row.
        r2 (List[Fraction]): Another matrix row.

    Returns:
    List[Fraction]: The resulting row from the sum of the two given rows.
    """
    return [sum(i) for i in zip(r1, r2)]


def multiplyRowBy(r, m):
    """Multiplies the elements of a matrix row by a multiplier `m`.

    Args:
        r (List[int]): A matrix row.
        m (int): The multiplier to be used on the elements of `r`.

    Returns:
        List[int]: The resulting row from the given row multipled by `m`.
    """
    return [m * x for x in r]


def divideRow(r, d):
    """Divides the elements of a matrix row by a divisor `d`.

    Args:
        r (List[int]): A matrix row.
        d (int): The divisor to be used on the elements of `r`.

    Returns:
        List[int]: The resulting row from the given row divided by `d`.
    """
    return [Fraction(x, d) for x in r]


def reduceDown(m, xPivot, yPivot):
    """Reduces the elements below a given pivot (in the same column) to 0.

    Args:
        m (List[List[int]]): An augmented matrix.
        xPivot (int): The 'x'-position of the pivot.
        yPivot (int): The 'y'-position of the pivot.

    Returns:
        List[List[int]]: The resulting matrix after the column is 
                         downwards-reduced.
    """
    if m[xPivot][yPivot] != 1:
        raise ValueError('pivot should have a value of 1')

    xNextRow = xPivot + 1
    while xNextRow < len(m):
        lead = m[xNextRow][yPivot]
        m[xNextRow] = sumRows(multiplyRowBy(m[xPivot], -lead), m[xNextRow])
        print("R{0} = R{1} - {2}R{3}".format(xNextRow +
              1, xNextRow + 1, lead, xPivot + 1))
        xNextRow += 1

    return m


def reduceUp(m, xPivot, yPivot):
    """Reduces the elements above a given pivot (in the same column) to 0.

    Args:
        m (List[List[int]]): An augmented matrix.
        xPivot (int): The 'x'-position of the pivot.
        yPivot (int): The 'y'-position of the pivot.

    Returns:
        List[List[int]]: The resulting matrix after the column is 
                         upwards-reduced.
    """
    if m[xPivot][yPivot] != 1:
        raise ValueError('pivot should have a value of 1')

    xNextRow = xPivot - 1
    while xNextRow >= 0:
        lead = m[xNextRow][yPivot]
        m[xNextRow] = sumRows(multiplyRowBy(m[xPivot], -lead), m[xNextRow])
        print("R{0} = R{1} - {2}R{3}".format(xNextRow +
              1, xNextRow + 1, lead, xPivot + 1))
        xNextRow -= 1

    return m


def ref(m):
    """Converts an augmented matrix into row-echelon form.

    Args:
        m (List[List[int]]): An augmented matrix.

    Returns:
        List[List[int]]: The given matrix in row-echelon form.
    """
    xPivot = yPivot = 0
    while (xPivot < len(m)):
        pivot = m[xPivot][yPivot]

        if (pivot != 1):
            m[xPivot] = divideRow(m[xPivot], pivot)

        reduceDown(m, xPivot, yPivot)
        xPivot += 1
        yPivot += 1

    return m


def prettyPrintMatrix(m):
    print(tabulate([[str(x) for x in row] for row in m]))


def swapRows(m, xRowA, xRowB):
    """Swaps the positions of two rows from an augmented matrix.

    Args:
        m (List[List[int]]): An augmented matrix.
        xRowA (int): The 'x'-position of one of the rows.
        xRowB (int): The 'x'-position of the other row.

    Returns:
        List[List[int]]: The resulting matrix after the rows are swapped.
    """
    m[xRowA], m[xRowB] = m[xRowB], m[xRowA]
    return m


def findNonZeroPivot(m, xPivot, yPivot):
    """Attempts to find a nonzero element below given pivot to swap.

    Args:
        m (List[List[int]]): An augmented matrix.
        xPivot (int): The 'x'-position of the zero-pivot.
        yPivot (int): The 'y'-position of the zero-pivot.

    Returns:
        bool: True if managed to swap to a nonzero pivot, False otherwise.
    """
    xNextRow = xPivot + 1
    while xNextRow < len(m):
        if m[xNextRow][yPivot] != 0:
            swapRows(m, xPivot, xNextRow)
            return True

    return False


def main():
    # Insert your matrix here!
    m = []

    xPivot = yPivot = 0
    while xPivot < len(m):
        pivot = m[xPivot][yPivot]
        # 1st case: if pivot = 1, start reduction,
        # 2nd case: if pivot != 1, but not equal to 0, divide to 1 and start reduction
        # 3rd case: if pivot == 0, find nonzero. if find non zero, swap. if don't find nonzero, move to next col same row.
        if pivot == 0:
            isNonZeroPivot = False
            xNextRow = xPivot + 1
            while xNextRow < len(m):
                if (m[xNextRow][yPivot] != 0):
                    m[xPivot], m[xNextRow] = m[xNextRow], m[xPivot]
                    print("R{0} <-> R{1}".format(xPivot, xNextRow))
                    isNonZeroPivot = True
                    break

                xNextRow += 1

            if not isNonZeroPivot:
                yPivot += 1
                if yPivot > len(m) - 1:
                    break
                continue

        # Scale pivot down to 1.
        if pivot != 1:
            m[xPivot] = divideRow(m[xPivot], pivot)
            print("R{0} = R{1}/{2}".format(xPivot + 1, xPivot + 1, pivot))
            prettyPrintMatrix(m)

        reduceDown(m, xPivot, yPivot)
        prettyPrintMatrix(m)
        reduceUp(m, xPivot, yPivot)
        prettyPrintMatrix(m)
        xPivot += 1
        yPivot += 1


if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
