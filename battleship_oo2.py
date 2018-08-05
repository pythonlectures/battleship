class Game:    def __init__(self, player1, player2, board):        self.player1 = player1        self.player2 = player2        self.board = board        self.board.ships.extend(player1.ships)        self.board.ships.extend(player2.ships)        self.player_takes_turn = self.player1        self.winner = None    @classmethod    def default(cls):        player1 = Player("Jack", [Ship([(1, 1), (1,2)]), Ship([(4, 5), (4,6)])])        player2 = Player("Jill", [Ship([(6, 5), (6, 6)]), Ship([(7, 7), (8,7)])])        board = Board(9)        return cls(player1, player2, board)    def play_game(self):        while self.winner is None:            shot = Shot(self.player_takes_turn.call_your_shot(), self.player_takes_turn)            self.take_shot(shot)            self.winner = self.return_winner()            self.alternate_turns()        self.declare_winner()    def alternate_turns(self):        self.player_takes_turn = self.player2 if self.player_takes_turn == self.player1 else self.player1    def declare_winner(self):        print('{}, you won the game!'.format(self.winner.name))    def take_shot(self, shot):        ship_hit = self.board.take_shot(shot)        if ship_hit:            print('{}, your shot hit {}\'s {}!'.format(shot.shooter.name, ship_hit.owner.name, ship_hit.name))            if ship_hit.is_sunk:                print('{}\'s {} sunk!'.format(ship_hit.owner.name, ship_hit.name))        else:            print('{}, you missed your shot!'.format(shot.shooter.name))    def return_winner(self):        if self.player1.has_lost():            return self.player2        elif self.player2.has_lost():            return self.player1        else:            return Noneclass Board:    def __init__(self, board_len):        self.coordinates = [(x, y) for x in range(1, board_len) for y in range(1, board_len)]        self.ships = []    def take_shot(self, shot):        for ship in self.ships:            if ship.is_hit(shot.coordinate):                return ship        return Noneclass Player:    def __init__(self, name, ships):        self.name = name        self.ships = []        self.ships.extend(ships)        self.set_ships_ownership()    def call_your_shot(self):        return tuple(int(x.strip()) for x in                     input('{}, call your shot using comma separated coordinates x, y: '.format(self.name)).split(','))    def has_lost(self):        return all(ship.is_sunk for ship in self.ships)    def set_ships_ownership(self):        for ship in self.ships:            setattr(ship, 'owner', self)class Ship:    id_counter = 0    def __init__(self, coordinates):        Ship.id_counter += 1        self.name = "Ship{}".format(Ship.id_counter)        self.coordinates = coordinates        self.is_sunk = False        self.owner = None    def is_hit(self, shot_coordinates):        hit = (shot_coordinates in self.coordinates)        if hit:            self.coordinates.remove(shot_coordinates)            if len(self.coordinates) == 0:                self.is_sunk = True        return hitclass Shot:    def __init__(self, coordinate, shooter):        self.coordinate = coordinate        self.shooter = shooterif __name__ == "__main__":    Game.default().play_game()