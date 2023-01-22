# Matrix Class 

This is a Python implementation of a Matrix class. It supports basic matrix operations such as addition, subtraction, multiplication, and exponentiation. It also has additional methods such as `transpose`, `rowswap`, and `rowmult` that can be used to perform additional matrix operations.

## Usage

- Create a matrix by passing a 2-dimensional list of numbers as the argument to the `Matrix` class
- Use the `+`, `-`, `*` and `**` operators to perform addition, subtraction, multiplication and exponentiation respectively.
- Use the `transpose`, `rowswap`, and `rowmult` methods for additional matrix operations.
- The matrix elements are accessible using the `[row, col]` notation

## Note

- The `__getitem__` and `__setitem__` methods are used to access and set the matrix elements respectively.
- The `__str__` method returns a string representation of the matrix in the form of a list of lists.
- The `__eq__` method checks if two matrices are equal by comparing their elements.
- The `copy` method returns a new instance of the matrix with the same elements.
- The `__pow__` method raises the matrix to the given power and returns the result.
- The `inverse` method returns the inverse of the matrix.

## Dependencies

The script uses the following libraries:
- fractions
- typing

Make sure to have them installed before running the script
