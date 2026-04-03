import unittest
import sys
import os

# Add projects directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'projects', 'aether')))

from core.engine import SimulationEngine
from world.grid import WorldGrid
from agents.humanoid import HumanoidAgent

class TestAETHER(unittest.TestCase):

    def setUp(self):
        self.world = WorldGrid(width=5, height=5)
        self.engine = SimulationEngine(self.world)
        self.agent = HumanoidAgent("TestBot", self.world, position=(0, 0))

    def test_grid_initialization(self):
        self.assertEqual(self.world.width, 5)
        self.assertFalse(self.world.is_occupied((1, 1)))

    def test_place_agent(self):
        success = self.world.place_agent(self.agent, (1, 1))
        self.assertTrue(success)
        self.assertTrue(self.world.is_occupied((1, 1)))

    def test_move_agent(self):
        self.world.place_agent(self.agent, (0, 0))
        success = self.agent.move(1, 1)
        self.assertTrue(success)
        self.assertEqual(self.agent.position, (1, 1))
        self.assertFalse(self.world.is_occupied((0, 0)))
        self.assertTrue(self.world.is_occupied((1, 1)))

    def test_battery_depletion(self):
        self.world.place_agent(self.agent, (0, 0))
        # Initial battery is 100. Each move (dx or dy != 0) costs 5.
        # Moving back and forth to deplete battery.
        for i in range(20):
            if i % 2 == 0:
                self.agent.move(1, 1)
            else:
                self.agent.move(-1, -1)

        self.assertEqual(self.agent.battery, 0)
        success = self.agent.move(1, 0)
        self.assertFalse(success)

    def test_simulation_step(self):
        self.engine.add_agent(self.agent, (0, 0))
        self.engine.step()
        self.assertEqual(self.engine.current_step, 1)

if __name__ == '__main__':
    unittest.main()
