import random

class DiceGame:
    def __init__(self):
        self.score = 0

    def roll_dice(self):
        """Simulate rolling two dice and return their values."""
        die1 = random.randint(1, 6)
        die2 = random.randint(1, 6)
        return die1, die2

    def play_round(self):
        """Play a round of the dice game."""
        die1, die2 = self.roll_dice()
        total = die1 + die2
        self.score += total
        return die1, die2, total, self.score

    def reset_game(self):
        """Reset the game score."""
        self.score = 0