board = [(x, y) for x in range(1, 9) for y in range(1, 9)]
player1 = 'Jack'
player2 = 'Jill'
ships1 = [[(1, 1), (1,2)],[(3,3), (3,4)]]
ships2 = [[(8, 8), (8,7)],[(6, 7), (6,6)]]


def main():
    winner = None
    player_takes_turn = player1
    while winner is None:
        take_shot(call_your_shot(player_takes_turn), player_takes_turn)
        winner = has_player_won()
        player_takes_turn = alternate_turns(player_takes_turn)
    declare_winner(winner)


def call_your_shot(player_takes_turn):
    return tuple(int(x.strip()) for x in input('{}, call your shot using comma separated coordinates x, y: '.format(player_takes_turn)).split(','))


def take_shot(shot, player_takes_turn):
    for ship in ships1:
        if shot in ship:
            print('{}, your shot hit {}\'s ship!'.format(player_takes_turn, player1))
            ship.remove(shot)
            if len(ship) == 0:
                ships1.remove(ship)
                print('{}\'s ship sunk!'.format(player1))
            return
    for ship in ships2:
        if shot in ship:
            print('{}, your shot hit {}\'s ship'.format(player_takes_turn, player2))
            ship.remove(shot)
            if len(ship) == 0:
                ships2.remove(ship)
                print('{}\'s ship sunk!'.format(player2))
            return
    print('{}, you missed your shot!'.format(player_takes_turn))

def has_player_won():
    if len(ships1) == 0:
        return player2
    elif len(ships2) == 0:
        return player1
    else:
        return None



def alternate_turns(player_takes_turn):
    return player2 if player_takes_turn == player1 else player1


def declare_winner(winner):
    print('{}, you won the game!'.format(winner))

if __name__ == "__main__":
    main()