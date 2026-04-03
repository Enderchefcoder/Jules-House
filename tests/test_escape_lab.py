import unittest
import sys
import os

# Add games directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'games')))

import escape_lab

class TestEscapeLab(unittest.TestCase):

    def setUp(self):
        self.state = escape_lab.GameState()

    def test_initial_state(self):
        self.assertEqual(self.state.current_room, "Lab")
        self.assertEqual(self.state.player.health, 100)
        self.assertEqual(self.state.player.energy, 100)

    def test_room_expansion(self):
        self.assertIn("Cryo Chamber", escape_lab.ROOMS)
        self.assertIn("Observation Deck", escape_lab.ROOMS)
        self.assertIn("Main Server Room", escape_lab.ROOMS)

    def test_log_system(self):
        self.assertIn("log_001", escape_lab.ROOMS["Lab"]["logs"])
        self.assertIn("ENTRY 001", escape_lab.LOG_CONTENTS["log_001"])

    def test_player_status(self):
        self.state.player.energy -= 10
        self.assertEqual(self.state.player.energy, 90)
        self.assertIn("Energy: 90", self.state.player.status())

if __name__ == '__main__':
    unittest.main()
