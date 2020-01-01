from unittest import TestCase

from sudoku import Cell, Sudoku


class TestCell(TestCase):

    def test_solved_cell_initializes_properly(self):
        solved_cell = Cell(4)
        self.assertTrue(solved_cell.is_solved(),
                        "Solved cell is not marked as solved")
        self.assertEqual(solved_cell.value(), 4,
                         "Value of solved cell is incorrect")

    def test_unsolved_cell_initializes_properly(self):
        unsolved_cell = Cell()
        self.assertFalse(unsolved_cell.is_solved(),
                         "Unsolved cell is marked as solved")
        self.assertEqual(unsolved_cell.candidates, list(range(1, 10)),
                         "Unsolved cell does not list all candidates.")


class TestSudoku(TestCase):
    def test_easy(self):
        input_string = """   . 5 2 | 4 7 . | . . . 
                             . 6 . | . . . | . . . 
                             . . . | . . 8 | . 1 . 
                            -------+-------+-------
                             4 . . | . . . | . . 9 
                             7 . . | 9 5 . | . . . 
                             . 2 . | . 4 . | . 3 . 
                            -------+-------+-------
                             . . . | 8 . . | . 9 . 
                             . . . | . . 3 | 7 . 6 
                             . . . | . 9 1 | . . . """
        sudoku = Sudoku(input_string)
        sudoku.solve()
        self.assertTrue(sudoku.is_solved())
        self.assertEqual(" 1 5 2 | 4 7 9 | 6 8 3 \n"
                         " 3 6 8 | 2 1 5 | 9 7 4 \n"
                         " 9 7 4 | 6 3 8 | 5 1 2 \n"
                         "-------+-------+-------\n"
                         " 4 1 6 | 3 8 7 | 2 5 9 \n"
                         " 7 8 3 | 9 5 2 | 4 6 1 \n"
                         " 5 2 9 | 1 4 6 | 8 3 7 \n"
                         "-------+-------+-------\n"
                         " 2 3 7 | 8 6 4 | 1 9 5 \n"
                         " 8 9 1 | 5 2 3 | 7 4 6 \n"
                         " 6 4 5 | 7 9 1 | 3 2 8 ",
                         str(sudoku),
                         "Solutions do not match.")
