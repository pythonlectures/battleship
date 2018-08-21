from typing import NamedTuple, Iterator


class Game:
    """
    This class controls the game.
    It declares the winner and who takes turn
    """

    def __init__(self, player1: 'Player', player2: 'Player'):
        self._player1 = player1
        self._player2 = player2
        self._winner = None
        self.shooter = self._player1
        self.receiver = self._player2

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

    def __init__(self, name: str):
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

    def take_shot(self, shot: 'Shot'):
        for ship in self._ships:
            if ship.is_hit(shot):
                print('{}, your shot hit {}!'.format(self.name, ship.get_name()))
                if ship.get_is_sunk():
                    print('{} sunk!'.format(ship.get_name))
            else:
                print('{}, you missed your shot!'.format(self.name))

    def has_lost(self):
        return all(ship.get_is_sunk() for ship in self._ships)


class Ship:
    """This class represents a ship, it keeps track if it is_sunk"""
    id_counter = 0

    def __init__(self, iter_coordinates: 'Iterator[Coordinates]'):
        Ship.id_counter += 1
        self._name = "Ship{}".format(Ship.id_counter)
        self._cells = [Cell(coordinates, status='Not Hit') for coordinates in iter_coordinates]
        self._is_sunk = False

    def update_is_sunk(self):
        self._is_sunk = all(cell.get_status() == "Hit" for cell in self._cells)

    def get_is_sunk(self):
        return self._is_sunk

    def get_name(self):
        return self._name

    def is_hit(self, shot: 'Shot'):
        for cell in self._cells:
            if cell.get_coordinates() == shot.coordinates:
                if cell.get_status() == 'Not Hit':
                    cell.set_status("Hit")
                    self.update_is_sunk()
                    return True
        return False


class Board:
    """This class keeps track of the shots taken by a Player """

    def __init__(self, board_len: int):
        self.coordinates = [Coordinates(x=x, y=y) for x in range(1, board_len) for y in range(1, board_len)]
        self.shots_taken = set()

    def take_shot(self, shot):
        self.shots_taken.add(shot)


Coordinates = NamedTuple('Coordinates', x=int, y=int)
Shot = NamedTuple('Shot', coordinates=Coordinates, shooter_name=str)


class Cell:
    """ This class contains the coordinates of a single cell, and keeps track if it has been hit """

    def __init__(self, coordinates: 'Coordinates', status: str = None):
        self._coordinates = coordinates
        self._status = status
        self._allowed_statuses = {'Hit', 'Not Hit'}

    def get_status(self):
        return self._status

    def set_status(self, status: str):
        if status in self._allowed_statuses:
            self._status = status
        else:
            raise ValueError(type(self).__name__ + "supports only these statuses: " + ",".join(self._allowed_statuses))

    def get_coordinates(self):
        return self._coordinates


def mock_game():
    board_len = 9
    player1 = Player("Jack")
    player1.set_ships([Ship([Coordinates(1, 1), Coordinates(1, 2)]), Ship([Coordinates(4, 5), Coordinates(4, 6)])])
    player1.set_board(Board(board_len))
    player2 = Player("Jill")
    player2.set_board(Board(board_len))
    player2.set_ships([Ship([Coordinates(6, 5), Coordinates(6, 6)]), Ship([Coordinates(7, 7), Coordinates(8, 7)])])
    Game(player1, player2).play_game()


if __name__ == "__main__":
    mock_game()
