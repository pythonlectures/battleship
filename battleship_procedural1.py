board = [(x, y) for x in range(1, 9) for y in range(1, 9)]
player1 = 'Jack'
player2 = 'Jill'
ship1 = (1, 1)
ship2 = (8, 8)

def main():
    sunk_ship = None
    player_takes_turn = player1
    while sunk_ship is None:
        shot = call_your_shot(player_takes_turn)
        sunk_ship = has_ship_sunk(shot, player_takes_turn)
        player_takes_turn = alternate_turns(player_takes_turn)
    declare_winner(sunk_ship)


def call_your_shot(player_takes_turn):
    return tuple(int(x.strip()) for x in input('{}, call your shot using coma separated coordinates x, y: '.format(player_takes_turn)).split(','))


def has_ship_sunk(shot, player_takes_turn):
    if shot == ship1:
        print('{}, your shot hit ship1!'.format(player_takes_turn))
        return ship1
    elif shot == ship2:
        print('{}, your shot hit ship2!'.format(player_takes_turn))
        return ship2
    else:
        print('{}, you missed your shot!'.format(player_takes_turn))
        return None


def alternate_turns(player_takes_turn):
    return player2 if player_takes_turn == player1 else player1


def declare_winner(sunk_ship):
    print('{}, you won the game!'.format(player2 if sunk_ship == ship1 else player1))

if __name__ == "__main__":
    main()