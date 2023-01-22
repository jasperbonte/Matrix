from fractions import Fraction


class Matrix:
    """Matrix Class"""

    def __init__(self, elements: list[list[float | Fraction]]):
        """Creates a matrix

        Args:
            elements (list[list[float | Fraction]]): elements grouped by row
        """
        self.elements = elements
        self.rows = len(self.elements)
        self.columns = len(self.elements[0])
        self.dimension = self.rows, self.columns

    def __getitem__(self, place: tuple[int, int]) -> float | Fraction:
        return self.elements[place[0]][place[1]]

    def __setitem__(self, place: tuple[int, int], val: float | Fraction) -> None:
        self.elements[place[0]][place[1]] = val

    def __str__(self) -> str:
        return "[{}]".format(
            "\n ".join(" ".join(str(j) for j in i) for i in self.elements)
        )

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Matrix):
            return self.elements == other.elements
        raise ValueError(f"can't compare matrix to {type(other)}")

    def copy(self) -> "Matrix":
        """Copys the matrix

        Returns:
            Matrix: the copyed matrix
        """
        return Matrix([[val for val in row] for row in self.elements])

    def __add__(self, other: "Matrix") -> "Matrix":
        return Matrix(
            [
                [a + b for a, b in zip(row1, row2)]
                for row1, row2 in zip(self.elements, other.elements)
            ]
        )

    def __sub__(self, other: "Matrix") -> "Matrix":
        return Matrix(
            [
                [a - b for a, b in zip(row1, row2)]
                for row1, row2 in zip(self.elements, other.elements)
            ]
        )

    def __mul__(self, other: "Matrix | float | Fraction") -> "Matrix":
        if isinstance(other, Matrix):
            return Matrix(
                [
                    [
                        sum(a * b for a, b in zip(row1, col2))
                        for col2 in zip(*other.elements)
                    ]
                    for row1 in self.elements
                ]
            )
        return Matrix([[val * other for val in row] for row in self.elements])

    def __pow__(self, exp: int) -> "Matrix":
        if exp == -1:
            return self.invers()
        res = IdentityMatrix(self.rows)
        for _ in range(exp):
            res *= self
        return res

    def transpose(self) -> "Matrix":
        """Transpose a matrix
        does not change the original matrix

        Returns:
            Matrix: the transposed matrix
        """
        return Matrix(list(map(list, zip(*self.elements))))

    def rowswap(self, a: int, b: int) -> None:
        """Swap two rows

        Args:
            a (int): a th row
            b (int): b th row
        """
        r_a = self.elements[a]
        self.elements[a] = self.elements[b]
        self.elements[b] = r_a

    def rowmult(self, r: int, n: float | Fraction) -> None:
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

    def rref(self) -> None:
        """Spill the matrix
        Original matrix gets affected"""
        for i in range(self.rows):
            spil = self[i, i]  # set spill
            if spil == 0:  # spill can't be zero
                for j in range(self.rows)[1:]:
                    if self[j, j] != 0:
                        self.rowswap(i, j)
                        spil = self[i, i]  # change the spill
                        break
                    else:
                        return

            # add zeros
            pr_matrix = self.copy()
            for j in range(self.rows):
                if j != i:
                    self[j, i] = 0

            # kruisproducten
            for r in range(self.rows):
                if r != i:
                    for c in range(self.columns):
                        self[r, c] = (spil * pr_matrix[r, c]) - (
                            pr_matrix[i, c] * pr_matrix[r, i]
                        )
            for i in range(self.rows):
                a = self[i, i]
                f = 10 ** (len(str(a)) - str(a).count("."))
                b = self[i, i] * f

                for j in range(self.columns):
                    self[i, j] = Fraction(self[i, j] * f, b)

    def invers(self) -> "Matrix":
        """Inverses a Matrix
        original matrix does not change

        Raises:
            ValueError: can't inverse matrix

        Returns:
            Matrix: the inversed matrix
        """
        if self.det() == 0 or self.rows != self.columns:
            raise ValueError("Can't inverse matrix")

        l: list[list[float | Fraction]] = []
        for i in range(self.rows):
            l.append([])
            l[-1].extend(self.elements[i])
            l[-1].extend([1 if i == j else 0 for j in range(self.rows)])
        a = Matrix(l)
        a.rref()
        b: list[list[float | Fraction]] = []
        for r in range(a.rows):
            b.append([])
            for c in range(a.columns)[self.rows :]:
                b[-1].append(a[r, c])
        return Matrix(b)

    def det(self) -> float | Fraction:
        if self.rows != self.columns:
            raise ValueError(f"Cant find det of {self.rows} x {self.columns} matrix")
        if self.rows == 1:
            return self[0, 0]
        elif self.rows == 2:
            return self[0, 0] * self[1, 1] - self[1, 0] * self[0, 1]
        else:
            # ontwikkelen naar rij 1
            s = 0
            for i in range(self.columns):
                l: list[list[float | Fraction]] = []
                for r in range(self.rows):
                    if r != 1:
                        l.append([])
                        for c in range(self.columns):
                            if c != i:
                                l[-1].append(self[r, c])
                s += (1 if i % 2 == 1 else -1) * self[1, i] * Matrix(l).det()
            return s


class IdentityMatrix(Matrix):
    def __init__(self, rows: int):
        res: list[list[float | Fraction]] = [
            [1 if i == j else 0 for i in range(rows)] for j in range(rows)
        ]
        super().__init__(res)
