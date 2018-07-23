class Game:
    def __init__(self, player1, player2, board):
        self.player1 = player1
        self.player2 = player2
        self.board = board
        self.board.ships.extend(player1.ships)
        self.board.ships.extend(player2.ships)
        self.player_takes_turn = self.player1
        self.winner = None

    @classmethod
    def default(cls):
        player1 = Player("Jack", [Ship(1, 1), Ship(2, 2)])
        player2 = Player("Jill", [Ship(8, 8), Ship(3, 3)])
        board = Board(9)
        return cls(player1, player2, board)

    def play_game(self):
        while self.winner is None:
            shot = self.player_takes_turn.call_your_shot()
            self.take_shot(shot)
            self.winner = self.return_winner()
            self.alternate_turns()
        self.declare_winner()

    def alternate_turns(self):
        self.player_takes_turn = self.player2 if self.player_takes_turn == self.player1 else self.player1

    def declare_winner(self):
        print('{}, you won the game!'.format(self.winner.name))

    def take_shot(self, shot):
        ship_hit = self.board.take_shot(shot)
        if ship_hit:
            print('{}, your shot hit {}!'.format(self.player_takes_turn.name, ship_hit.name))
            self.winner = self.player2
        else:
            print('{}, you missed your shot!'.format(self.player_takes_turn.name))
            self.winner = None

    def return_winner(self):
        if self.player1.has_lost():
            return self.player2
        elif self.player2.has_lost():
            return self.player1
        else:
            return None


class Board:
    def __init__(self, board_len):
        self.coordinates = [(x, y) for x in range(1, board_len) for y in range(1, board_len)]
        self.ships = []

    def take_shot(self, shot):
        for ship in self.ships:
            if ship.is_hit(shot):
                return ship
        return None


class Player:
    def __init__(self, name, ships):
        self.name = name
        self.ships = []
        self.ships.extend(ships)

    def call_your_shot(self):
        return tuple(int(x.strip()) for x in
                     input('{}, call your shot using coma separated coordinates x, y: '.format(self.name)).split(','))

    def has_lost(self):
        return all(ship.is_sunk for ship in self.ships)


class Ship:
    id_counter = 0

    def __init__(self, x, y):
        Ship.id_counter += 1
        self.name = "Ship{}".format(Ship.id_counter)
        self.coordinates = (x, y)
        self.is_sunk = False

    def is_hit(self, shot):
        hit = (shot == self.coordinates)
        if hit:
            self.is_sunk = True
        return hit


if __name__ == "__main__":
    Game.default().play_game()
