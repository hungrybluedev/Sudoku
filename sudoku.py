# The frequently used ranges
RANGE3 = range(3)
RANGE9 = range(9)
RANGE81 = range(81)
CANDIDATES_RANGE = range(1, 10)

# This divider is printed to separate the parts
DIVIDER = "-------+-------+-------"

# These are the constants used to group "chunks" or areas in Sudoku
# These areas are the ones where the constraints need to be applied
TRIPLES = [[offset * 3 + i for i in RANGE3] for offset in RANGE3]
ROWS = [[i * 9 + j for j in RANGE9] for i in RANGE9]
COLS = [[i * 9 + j for i in RANGE9] for j in RANGE9]
SUB_SQUARES = [
    [i * 9 + j for i in rows for j in cols]
    for rows in TRIPLES for cols in TRIPLES
]

CHUNKS = ROWS + COLS + SUB_SQUARES
CHUNK_MAP = {}

# Populating the map that relates the positions to the chunks they are in
for position in RANGE81:
    CHUNK_MAP[position] = []
for chunk in CHUNKS:
    for position in chunk:
        CHUNK_MAP[position].append(chunk)


class Cell(object):
    """A class to help encapsulate the operations performed on a single cell
    on the board.

    This class encapsulates a list of candidates and operations on them to
    help improve readability and simplicity of the codebase.
    """

    def __init__(self, value=None):
        """Initialize the cell with the given value.

        If no value is provided, all possible values are set as candidates.
        """
        self.candidates = list(CANDIDATES_RANGE) if value is None else [value]

    def is_solved(self):
        """A cell is marked as solved if it has only one candidate."""
        return len(self.candidates) == 1

    def is_invalid(self):
        """A cell is invalid if any of the simplification operations caused
        the cell to loose all candidates."""
        return len(self.candidates) == 0

    def value(self):
        """
        :returns  a non-null value only when it is solved. Otherwise None.
        """
        return self.candidates[0] if self.is_solved() else None

    def __contains__(self, item):
        """
        :returns True if the given candidate is a valid option for this Cell.
        """
        return item in self.candidates

    def remove(self, item):
        """Removes the given candidate from the Cell's list of candidates
        if present.
        """
        if item in self:
            self.candidates.remove(item)

    def set(self, value):
        """Marks the cell as solved and assigns it the given value."""
        self.candidates = [value]

    def reset(self, old_candidates):
        self.candidates = old_candidates


class Board(object):

    def __init__(self, clean_string):
        self.cells = [
            Cell() if not char.isdigit() else Cell(int(char))
            for char in clean_string
        ]

    def __iter__(self):
        for cell in self.cells:
            yield cell

    def get_cell_at(self, index):
        return self.cells[index]


class Sudoku(object):
    def __init__(self, input_string=""):
        # This simple use of replacement makes it easy to handle
        # pretty-printed board states.
        for char in " -|+\n":
            input_string = input_string.replace(char, "")

        if len(input_string) != 81:
            raise AttributeError("Input must have length 81")

        self.board = Board(input_string)

        # Stat tracking parameters
        self.duplicates_removed = []
        self.singles_solved = []
        self.last_cells_solved = []
        self.backtracks = 0

    def is_solved(self):
        """A board is solved when there are no unsolved cells and the board is
        valid."""
        return all(
            [cell.is_solved() for cell in self.board]
        ) and self.is_valid()

    def is_valid(self, location=None):
        """A board is valid if all the areas have all the possible values at
         most once and the no cell is invalid."""
        areas = CHUNKS if location is None else CHUNK_MAP[location]
        for area in areas:
            # We keep track of the unique values we find
            found = []
            for index in area:
                cell = self.board.get_cell_at(index)
                if cell.is_invalid():
                    return False
                if cell.is_solved():
                    value = cell.value()
                    if value in found:
                        return False
                    else:
                        found.append(value)
        return True

    def _simplify(self):
        counts = {"remove duplicates": self._remove_duplicates(),
                  "solve singles": self._solve_singles(),
                  "solve last cell": self._solve_last_cell()}

        self.duplicates_removed.append(counts["remove duplicates"])
        self.singles_solved.append(counts["solve singles"])
        self.last_cells_solved.append(counts["solve last cell"])

        return sum(counts.values())

    def _remove_duplicates(self):
        counter = 0
        for location in RANGE81:
            if not self.board.get_cell_at(location).is_solved():
                continue
            value = self.board.get_cell_at(location).value()
            for area in CHUNK_MAP[location]:
                for neighbour_index in area:
                    if neighbour_index == location:
                        # We skip the solved cell
                        continue
                    cell = self.board.get_cell_at(neighbour_index)
                    if value in cell:
                        cell.remove(value)
                        counter += 1

        return counter

    def _solve_singles(self):
        counter = 0
        for area in CHUNKS:
            # We are going to see if any of the cells have a candidate
            # that is only present in that location and nowhere else.

            # We keep track of the number of times a candidate has appeared
            candidate_counts = {}
            for candidate in CANDIDATES_RANGE:
                candidate_counts[candidate] = 0

            for location in area:
                for candidate in self.board.get_cell_at(location).candidates:
                    candidate_counts[candidate] += 1

            # We see if any candidate appears only once in the area
            target = None
            for candidate, count in candidate_counts.items():
                if count == 1:
                    target = candidate
                    break

            if target is None:
                # There is no candidate that appears only once in the area
                # We can proceed to search the next area/chunk.
                continue

            # Since the target candidate appears in only one cell,
            # we can go ahead and directly change it
            for location in area:
                cell = self.board.get_cell_at(location)
                if cell.is_solved():
                    continue

                if target in cell:
                    cell.set(target)
                    counter += 1

        return counter

    def _solve_last_cell(self):
        counter = 0
        for area in CHUNKS:
            # We need to see if any area has just one unsolved cell
            solved_count, unsolved = 0, None
            candidates = list(CANDIDATES_RANGE)
            for location in area:
                cell = self.board.get_cell_at(location)
                if cell.is_solved():
                    solved_count += 1
                    candidates.remove(cell.value())
                else:
                    unsolved = cell

            # We can continue only when all but one have been solved.
            if solved_count != 8:
                continue

            unsolved.set(candidates[0])
            counter += 1

        return counter

    def _next_empty_slot(self):
        for location in RANGE81:
            if not self.board.get_cell_at(location).is_solved():
                return location
        return None

    def solve(self):
        while self._simplify() > 0:
            pass
        return self._backtrack_and_solve()

    def _backtrack_and_solve(self):
        location = self._next_empty_slot()
        if location is None:
            return self.is_valid()

        cell = self.board.get_cell_at(location)
        candidates = cell.candidates

        for candidate in candidates:
            cell.set(candidate)
            if self.is_valid(location) and \
                    self._backtrack_and_solve():
                return True
            cell.reset(candidates)
            self.backtracks += 1

        return False

    def print_stats(self):
        print("Duplicates removed   :", self.duplicates_removed)
        print("Singles solved       :", self.singles_solved)
        print("Last cells solved    :", self.last_cells_solved)
        print("Backtracks performed :", self.backtracks)

    def __str__(self, pretty_print=True):
        if not self.is_valid():
            return "Invalid sudoku"
        if pretty_print:
            lines = []
            location = 0
            for i in RANGE9:
                line = " "
                for j in RANGE9:
                    if j % 3 == 0 and j != 0:
                        line += "| "
                    if not self.board.get_cell_at(location).is_solved():
                        value = "."
                    else:
                        value = str(self.board.get_cell_at(location).value())
                    line += value + " "
                    location += 1

                if i % 3 == 0 and i != 0:
                    lines.append(DIVIDER)
                lines.append(line)
            return '\n'.join(lines)
        else:
            return ''.join(
                str(cell.value()) if cell.is_solved() else '.' for cell in
                self.board)


def main():
    pass


if __name__ == '__main__':
    main()
