import random


class Board:
    def __init__(self):
        self.snakes = {25: 5, 34: 1, 47: 19, 65: 52, 87: 57, 91: 61, 99: 69}
        self.ladders = {3: 51, 6: 27, 20: 70, 36: 55, 63: 95, 68: 98}
        self.size = 100

    def check_for_snakes_ladders(self, position):
        if position in self.snakes:
            print("Oops! You have got a snake bite")
            return self.snakes[position]
        elif position in self.ladders:
            print("Hurray! You have got a ladder")
            return self.ladders[position]
        else:
            return position


class Dice:
    def roll(self):
        return random.randint(1, 6)


class Player:
    def __init__(self, name):
        self.name = name
        self.position = 0

    def move(self, value):
        if self.position < 100:
            self.position += value


class Game:
    def __init__(self):
        self.board = Board()
        self.dice = Dice()
        self.players = []

    def add_player(self, name):
        self.players.append(Player(name))

    def play(self):
        while True:
            for player in self.players:

                value = self.dice.roll()
                print("_______________________________________________________")
                print("{} rolled a {}.".format(player.name, value))
                if value + player.position > self.board.size:
                    print('Better luck next time...You have crossed board size')
                    continue
                player.move(value)
                player.position = self.board.check_for_snakes_ladders(player.position)
                print("You are now on square {}.".format(player.position))

                if player.position >= 100:
                    print("Congratulations, {}! You have won the game!".format(player.name))
                    return


game = Game()

game.add_player("Navya")
game.add_player("Sravya")
print("***** GAME STARTS NOW *****")
print("***** Navya and Sree are playing!!! *****")
game.play()
