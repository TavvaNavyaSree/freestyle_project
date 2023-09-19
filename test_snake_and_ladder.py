import unittest
from unittest.mock import patch
from io import StringIO
from snake_and_ladder import Board, Dice, Player

class TestBoard(unittest.TestCase):
    def test_check_for_snakes_ladders_snake(self):
        board = Board()
        position = 25
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            new_position = board.check_for_snakes_ladders(position)
            self.assertEqual(new_position, 5)
            self.assertEqual(
                mock_stdout.getvalue().strip(), "Oops! You have got a snake bite")

    def test_check_for_snakes_ladders_ladder(self):
        board = Board()
        position = 3
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            new_position = board.check_for_snakes_ladders(position)
            self.assertEqual(new_position, 51)
            self.assertEqual(
                mock_stdout.getvalue().strip(), "Hurray! You have got a ladder")

    def test_check_for_snakes_ladders_no_change(self):
        board = Board()
        position = 10
        new_position = board.check_for_snakes_ladders(position)
        self.assertEqual(new_position, position)


class TestDice(unittest.TestCase):
    def test_roll(self):
        dice = Dice()
        for _ in range(1000):
            roll_value = dice.roll()
            self.assertTrue(1 <= roll_value <= 6)


class TestPlayer(unittest.TestCase):
    def test_move_within_bounds(self):
        player = Player("Test Player")
        player.move(3)
        self.assertEqual(player.position, 3)

     # Should not move beyond 100


if __name__ == '__main__':
    unittest.main()
