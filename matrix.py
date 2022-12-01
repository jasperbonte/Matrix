"a matrix library"

from copy import deepcopy
from typing import Union


class Matrix:
    """Matrix Class"""

    def __init__(self, elements: list[list[float]]):
        """Creates a matrix

        Args:
            elements (list[list[float]]): elements grouped by row
        """
        self.elements = elements

    def __getitem__(self, place: tuple[int, int]) -> float:
        row, column = place
        return self.elements[row][column]

    def __setitem__(self, place: tuple[int, int], val: float) -> None:
        self.elements[place[0]][place[1]] = val

    def __str__(self) -> str:
        return str(self.elements).replace("[[", "[").replace("[", "\n[")

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Matrix):
            return self.elements == other.elements
        return False

    def copy(self) -> "Matrix":
        """Copys the matrix

        Returns:
            Matrix: the copyed matrix
        """
        return Matrix(deepcopy(self.elements))

    def get_dimension(self) -> tuple[int, int]:
        """Get dimensions of matrix

        Returns:
            tuple[int, int]: rows, columns
        """
        return self.get_rows(), self.get_columns()

    def get_rows(self) -> int:
        """Get amount of rows

        Returns:
            int: amount rows
        """
        return len(self.elements)

    def get_columns(self) -> int:
        """Get amount of columns

        Returns:
            int: amount columns
        """
        return len(self.elements[0])

    def __add__(self, other: "Matrix") -> "Matrix":
        return Matrix(
            [
                [self[r, c] + other[r, c] for c in range(self.get_columns())]
                for r in range(self.get_rows())
            ]
        )

    def __sub__(self, other: "Matrix") -> "Matrix":
        return Matrix(
            [
                [self[r, c] - other[r, c] for c in range(self.get_columns())]
                for r in range(self.get_rows())
            ]
        )

    def __mul__(self, other: Union["Matrix", float]) -> "Matrix":
        if isinstance(other, Matrix):
            return Matrix(
                [
                    [
                        sum(
                            [
                                self[r, i] * other[i, c]
                                for i in range(self.get_columns())
                            ]
                        )
                        for c in range(other.get_columns())
                    ]
                    for r in range(self.get_rows())
                ]
            )
        return Matrix(
            [
                [other * self[r, c] for c in range(self.get_columns())]
                for r in range(self.get_rows())
            ]
        )

    def __pow__(self, exp: int) -> "Matrix":
        res = IdentityMatrix(self.get_rows())
        for _ in range(exp):
            res *= self
        return res

    def transpose(self) -> "Matrix":
        """Transpose a matrix

        Returns:
            Matrix: the transposed matrix
        """
        res = Matrix(
            [[0 for _ in range(self.get_rows())] for _ in range(self.get_columns())]
        )
        for r in range(self.get_rows()):
            for c in range(self.get_columns()):
                res[c, r] = self[r, c]

        return res

    def rowswap(self, a: int, b: int) -> None:
        """Swap two rows

        Args:
            a (int): a th row
            b (int): b th row
        """
        r_a = self.elements[a]
        self.elements[a] = self.elements[b]
        self.elements[b] = r_a

    def rowmult(self, r: int, n: float) -> None:
        """Multiply a row with a float

        Args:
            r (int): row number
            n (float): what to multiply the row with
        """
        self.elements[r] = [a * n for a in self.elements[r]]

    def rowadd(self, r1: int, r2: int) -> None:
        """Add two rows together and stores it in the second row

        Args:
            r1 (int): the first row
            r2 (int): the second row
        """
        self.elements[r1] = [
            self.elements[r1][n] + self.elements[r2][n] for n in range(r1)
        ]

    def spill(self) -> None:
        """Spill the matrix"""
        for i in range(self.get_rows()):
            print(self)
            spil = self[i, i]
            if spil == 0:
                for j in range(self.get_rows())[1:]:
                    if self[j, j] != 0:
                        self.rowswap(i, j)
                        self.spill()
                    return

            # add zeros
            pr_matrix = self.copy()
            for j in range(self.get_rows()):
                if j != i:
                    self[j, i] = 0

            # kruisproducten
            for r in range(self.get_rows()):
                for c in range(self.get_columns()):
                    if r == i or c <= i:
                        continue
                    else:
                        self[r, c] = (spil * pr_matrix[r, c]) - (
                            pr_matrix[i, c] * pr_matrix[r, i]
                        )

    def inverse(self) -> None:
        """Inverse the matrix"""
        l: list[list[float]] = []
        for i in range(self.get_rows()):
            l.append([])
            l[-1].extend(self.elements[i])
            l[-1].extend([1 if i == j else 0 for j in range(self.get_rows())])
        self.elements = l
        self.spill()


class IdentityMatrix(Matrix):
    def __init__(self, rows: int):
        res: list[list[float]] = [
            [1 if i == j else 0 for i in range(rows)] for j in range(rows)
        ]
        super().__init__(res)
