class Array:
    def __init__(self, rows, cols, init = None):
        self.rows = rows
        self.cols = cols
        self.data = rows * cols * [init]
    
    def coord_to_index(self, row, col):
        assert row >= 0 and row < self.rows, "Array row out of bounds"
        assert col >= 0 and col < self.cols, "Array col out of bounds"
        return row * self.cols + col
    
    def get(self, row, col):
        return self.data[self.coord_to_index(row, col)]
    
    def set(self, row, col, val):
        self.data[self.coord_to_index(row, col)] = val

    def view(self, drow, dcol):
        return View(self, drow, dcol)

class View:
    def __init__(self, array, drow, dcol):
        self.array = array
        self.drow = drow
        self.dcol = dcol
    
    def get(self, row, col):
        return self.array.get(self.drow + row, self.dcol + col)
    
    def set(self, row, col, val):
        self.array.set(self.drow + row, self.dcol + col, val)
    
    def view(self, drow, dcol):
        return View(self.array, self.drow + drow, self.dcol + dcol)
