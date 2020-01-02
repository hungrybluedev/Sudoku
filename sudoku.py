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
        return len(self.candidates) == 1

    def is_invalid(self):
        return len(self.candidates) == 0

    def value(self):
        return self.candidates[0]

    def __contains__(self, item):
        return item in self.candidates

    def remove(self, item):
        self.candidates.remove(item)

    def set(self, value):
        if value not in self.candidates:
            return False
        self.candidates = [value]
        return True


class Sudoku(object):
    def __init__(self, input_string=""):
        # This simple use of replacement makes it easy to handle
        # pretty-printed board states.
        for char in " -|+\n":
            input_string = input_string.replace(char, "")

        if len(input_string) != 81:
            raise AttributeError("Input must have length 81")

        self.board = [
            Cell() if not char.isdigit() else Cell(int(char))
            for char in input_string
        ]

    def is_solved(self):
        return all([cell.is_solved() for cell in self.board]) \
               and self.is_valid()

    def is_valid(self):
        for area in CHUNKS:
            found = []
            for index in area:
                location = self.board[index]
                if location.is_invalid():
                    return False
                if location.is_solved():
                    value = location.value()
                    if value in found:
                        return False
                    else:
                        found.append(value)
        return True

    def _simplify(self):
        counter = self._remove_duplicates()
        counter += self._solve_singles()
        return counter

    def _remove_duplicates(self):
        counter = 0
        for location in RANGE81:
            if not self.board[location].is_solved():
                continue
            value = self.board[location].value()
            for area in CHUNK_MAP[location]:
                for neighbour in area:
                    if neighbour == location:
                        # We skip the solved cell
                        continue
                    if value in self.board[neighbour]:
                        self.board[neighbour].remove(value)
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
                for candidate in self.board[location].candidates:
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
                cell = self.board[location]
                if cell.is_solved():
                    continue

                if target in cell:
                    cell.set(target)
                    counter += 1

        return counter

    def _next_empty_slot(self):
        for location in RANGE81:
            if not self.board[location].is_solved():
                return location
        return None

    def solve(self):
        while self._simplify() > 0:
            pass
        return self._recursive_solve()

    def _recursive_solve(self):
        if not self.is_valid():
            return False

        location = self._next_empty_slot()
        if location is None:
            return self.is_valid()

        candidates = self.board[location].candidates

        for candidate in candidates:
            self.board[location].candidates = [candidate]
            if self._recursive_solve():
                return True
        self.board[location].candidates = candidates
        return False

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
                    if not self.board[location].is_solved():
                        value = "."
                    else:
                        value = str(self.board[location].value())
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
