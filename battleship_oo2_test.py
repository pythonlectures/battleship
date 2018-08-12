from typing import NamedTuple


class Game:
    """
    This class controls the game.
    It declares the winner and who takes turn
    """

    def __init__(self, player1, player2):
        self._player1 = player1
        self._player2 = player2
        self._winner = None
        self.shooter = player1
        self.receiver = player2

    @classmethod
    def default(cls):
        board_len = 9
        player1 = Player("Jack")
        player1.set_ships([Ship([(1, 1), (1, 2)]), Ship([(4, 5), (4, 6)])])
        player1.set_board(Board(board_len))
        player2 = Player("Jill")
        player2.set_board(Board(board_len))
        player2.set_ships([Ship([(6, 5), (6, 6)]), Ship([(7, 7), (8, 7)])])
        return cls(player1, player2)

    def play_game(self):
        while self._winner is None:
            self.take_shot()
            self.update_winner()
            self.alternate_turns()
        self.declare_winner()

    def alternate_turns(self):
        self.shooter, self.receiver = self.receiver, self.shooter

    def declare_winner(self):
        print('{}, you won the game!'.format(self._winner.name))

    def take_shot(self):
        shot = self.shooter.call_your_shot()
        self.receiver.take_shot(shot)

    def update_winner(self):
        if self._player1.has_lost():
            self._winner = self._player2
        elif self._player2.has_lost():
            self._winner = self._player1


class Player:
    """
    This class contains the details of the player, the list of ships and the board seen by the player
    """

    def __init__(self, name):
        self.name = name
        self._ships = None
        self._board = None

    def set_ships(self, ships):
        self._ships = list(ships)

    def set_board(self, board):
        self._board = board

    def call_your_shot(self):
        coordinates = Coordinates(*(int(x.strip()) for x in
                                    input('{}, call your shot using comma separated coordinates x, y: '.format(
                                        self.name)).split(',')))
        shot = Shot(coordinates=coordinates, shooter_name=self.name)
        self._board.shots_taken.add(shot)
        return shot

    def take_shot(self, shot):
        for ship in self._ships:
            if ship.take_shot(shot):
                return
        print('{}, you missed your shot!'.format(shot.shooter_name))

    def has_lost(self):
        return all(ship.is_sunk for ship in self._ships)


class Ship:
    """This class represents a ship, it keeps track if it is_sunk"""
    id_counter = 0

    def __init__(self, list_tuples):
        Ship.id_counter += 1
        self.name = "Ship{}".format(Ship.id_counter)
        self.cells = [Cell(Coordinates(*tuple_)) for tuple_ in list_tuples]

    @property
    def is_sunk(self):
        return all(cell.is_hit for cell in self.cells)

    def take_shot(self, shot):
        for cell in self.cells:
            if cell.coordinates == shot.coordinates:
                cell.is_hit = True
                print('{}, your shot hit {}!'.format(shot.shooter_name, self.name))
                if self.is_sunk:
                    print('{} sunk!'.format(self.name))
                return True
        return False


class Board:
    """This class keeps track of the shots taken by a Player """
    def __init__(self, board_len):
        self.coordinates = [Coordinates(x=x, y=y) for x in range(1, board_len) for y in range(1, board_len)]
        self.shots_taken = set()

    def take_shot(self, shot):
        self.shots_taken.add(shot)


Coordinates = NamedTuple('Coordinates', x=int, y=int)


class Cell:
    """ This class contains the coordinates of a single cell, and keeps track if it has been hit """
    def __init__(self, coordinates):
        self.coordinates = coordinates
        self.is_hit = False


Shot = NamedTuple('Shot', coordinates=Coordinates, shooter_name=str)

if __name__ == "__main__":
    Game.default().play_game()
    #encoding change test