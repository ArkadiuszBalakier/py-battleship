class Deck:
    def __init__(self, row, column, is_alive=True):
        pass


class Ship:
    def __init__(self, start: tuple, end: tuple, is_drowned=False):
        ship_cords = set()
        r1, c1 = start
        r2, c2 = end

        if r1 == r2:
            ship_cords = {(r1, c) for c in range(min(c1, c2), max(c1, c2) + 1)}
        elif c1 == c2:
            ship_cords = {(r, c1) for r in range(min(r1, r2), max(r1, r2) + 1)}
        if not ship_cords:
            raise ValueError("Ship must be horizontal or vertical")

        self.cords = ship_cords
        self.hits = set()
        self.is_drowned = is_drowned
        self.size = len(self.cords)

    def is_sunk(self) -> str:
        self.is_drowned = True
        return "Sunk!"


    def get_deck(self, row, column) -> bool:
        if (row, column) in self.cords:
            return True
        return False

    def fire(self, row, column) -> str:
        if self.get_deck(row, column):
            self.hits.add((row, column))
            if self.hits == self.cords:
                return self.is_sunk()
            else:
                return "Hit!"
        return "Miss!"


class Battleship:
    def __init__(self, ships):
        self.ships = []
        self.field = {}
        for start, end in ships:
            cords = (start, end)
            if cords in self.field:
                raise ValueError("Overlapping ships")
            ship = Ship(start, end)
            self.ships.append(ship)

            for r, c in ship.cords:
                if not (0 <= r < 10 and 0 <= c < 10):
                    raise ValueError("ship out of board")
                coord = (r, c)
                if coord in self.field:
                    raise ValueError(f"Overlapping ships at {coord}")
                self.field[coord] = ship
        self._validate_field()

    def fire(self, location: tuple):
        if not isinstance(location, tuple) or not len(location) == 2:
            return "Miss!"

        if location not in self.field:
            return "Miss!"

        ship = self.field[location]
        result = ship.fire(*location)
        return result

    def _validate_field(self) -> None:
        expected_ship_count = {
            4:1,
            3:2,
            2:3,
            1:4
        }

        for ship in self.ships:
            if ship.size not in expected_ship_count:
                raise ValueError("Invalid ship size")
        actual_ship_counts = {}
        for ship in self.ships:
            size = ship.size
            actual_ship_counts[size] = actual_ship_counts.get(size, 0) + 1

        if actual_ship_counts != expected_ship_count:
            raise ValueError("Invalid ship count")