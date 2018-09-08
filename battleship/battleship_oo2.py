from typing import NamedTuple, Iterator
from enum import Enum, auto


class Game:
    """
    This class controls the game.
    It declares the winner and who takes turn
    """

    def __init__(self, player1: 'Player', player2: 'Player'):
        self._player1 = player1
        self._player2 = player2
        self._winner = None
        self._shooter = self._player1
        self._receiver = self._player2

    def play_game(self):
        while self._winner is None:
            self._take_shot()
            self._update_winner()
            self._alternate_turns()
        self._declare_winner()

    def _alternate_turns(self):
        self._shooter, self._receiver = self._receiver, self._shooter

    def _declare_winner(self):
        print('{}, you won the game!'.format(self._winner.get_name()))

    def _take_shot(self):
        shot = self._shooter.call_your_shot()
        for ship in self._receiver.get_ships():
            if ship.is_hit(shot):
                print('{}, your shot hit {}!'.format(self._shooter.get_name(), ship.get_name()))
                if ship.get_is_sunk():
                    print('{} sunk!'.format(ship.get_name()))
                return
        print('{}, you missed your shot!'.format(self._shooter.get_name()))

    def _update_winner(self):
        if self._player1.has_lost():
            self._winner = self._player2
        elif self._player2.has_lost():
            self._winner = self._player1


class Player:
    """
    This class contains the details of the player, the list of ships and the board seen by the player
    """

    def __init__(self, name: str):
        self._name = name
        self._ships = None
        self._board = None

    def set_ships(self, iter_ships: 'Iterator[Ship]'):
        self._ships = list(iter_ships)

    def get_ships(self):
        return self._ships

    def set_board(self, board):
        self._board = board

    def get_name(self):
        return self._name

    def call_your_shot(self):
        print('{}, call your shot using comma separated coordinates x, y: '.format(self._name))
        while True:
            try:
                coordinates = Coordinates(*(int(x.strip()) for x in
                                            input().split(',')))
                break
            except (TypeError, ValueError):
                print("Please try again, you must input two integers separated by a comma")
        shot = Shot(coordinates=coordinates)
        return shot

    def has_lost(self):
        return all(ship.get_is_sunk() for ship in self._ships)


class Ship:
    """This class represents a ship, it keeps track if it is_sunk"""
    id_counter = 0

    def __init__(self, iter_coordinates: 'Iterator[Coordinates]'):
        Ship.id_counter += 1
        self._name = "Ship{}".format(Ship.id_counter)
        self._cells = [Cell(coordinates, CellStatus.UNDISCOVERED) for coordinates in iter_coordinates]
        self._is_sunk = False

    def _update_is_sunk(self):
        self._is_sunk = all(cell.get_status() is CellStatus.HIT for cell in self._cells)

    def get_is_sunk(self):
        return self._is_sunk

    def get_name(self):
        return self._name

    def is_hit(self, shot: 'Shot'):
        for cell in self._cells:
            if cell.get_coordinates() == shot.coordinates:
                if cell.get_status() is not CellStatus.HIT:
                    cell.set_status(CellStatus.HIT)
                    self._update_is_sunk()
                    return True
        return False


class Board:
    """This class keeps track of the shots taken by a Player """

    def __init__(self, board_len: int):
        self._cells = [Cell(Coordinates(x=x, y=y)) for x in range(1, board_len) for y in range(1, board_len)]


Coordinates = NamedTuple('Coordinates', x=int, y=int)

Shot = NamedTuple('Shot', coordinates=Coordinates)


class CellStatus(Enum):
    UNDISCOVERED = auto()
    HIT = auto()


class Cell:
    """ This class contains the coordinates of a single cell, and keeps track if it has been hit """

    def __init__(self, coordinates: 'Coordinates', status=CellStatus.UNDISCOVERED):
        self._coordinates = coordinates
        self._status = status

    def get_status(self):
        return self._status

    def set_status(self, status: CellStatus):
        if status in CellStatus:
            self._status = status
        else:
            raise ValueError(type(self).__name__ + " supports only CellStatus ")

    def get_coordinates(self):
        return self._coordinates


def mock_game():
    board_len = 9
    player1 = Player("Jack")
    player1.set_ships([Ship((Coordinates(1, 1), Coordinates(1, 2))), Ship([Coordinates(4, 5), Coordinates(4, 6)])])
    player1.set_board(Board(board_len))
    player2 = Player("Jill")
    player2.set_board(Board(board_len))
    player2.set_ships((Ship([Coordinates(6, 5), Coordinates(6, 6)]), Ship([Coordinates(7, 7), Coordinates(8, 7)])))
    Game(player1, player2).play_game()


if __name__ == "__main__":
    mock_game()
