# Sudoku

A self-contained Python program that can solve Sudoku puzzles using traditional techniques as well as backtracking.

Coming Soon:

1. Playable game loop where the user can play Sudoku in the terminal.
2. A GUI for the app.

## Status

This is currently a work in progress and needs a lot of polish in terms of its API as well as unit tests. Currently it does indeed solve _all_ possible valid Sudoku states. However, it relies heavily on backtracking and is very slow. I am in the process of implementing the traditional Sudoku solving algorithms in the code.

Expect lots of refactoring and breaking changes by the time this is stable.

## Usage

```python
from sudoku import Sudoku

# The input string can be prettified or simply
# an 81-character long string with digits for
# given values and dots for unknowns
input_string = """   . . . | . . . | . . . 
                     . . . | . 2 9 | . 8 . 
                     . 7 4 | . . 5 | . . 2 
                    -------+-------+-------
                     . . . | . . . | . 1 . 
                     9 . 3 | . . 7 | . . . 
                     6 . 7 | . 3 . | . 4 8 
                    -------+-------+-------
                     . . . | . 9 . | . . 3 
                     . 6 5 | . . . | . . . 
                     . 4 . | 2 . . | 6 . ."""

sudoku = Sudoku(input_string)
print(sudoku)
sudoku.solve()
print(sudoku)
```

## License

[MIT License](/LICENSE)