import unittest
from transition import infect, recover
from agent import Agent
import random

class TestTransition(unittest.TestCase):

    def test_infect(self):
        agent1 = Agent("S", (0.5, 0.5))
        agent2 = Agent("I", (0.5, 0.5))
        agents = [agent1, agent2]
        infect(agents, infection_distance=0.1, infection_probability=1.0)
        self.assertEqual(agent1.status, "I")

    def test_recover(self):
        agent1 = Agent("I", (0.5, 0.5))
        agent1.days_with_status = 6
        agent2 = Agent("S", (0.5, 0.5))
        agents = [agent1, agent2]
        recover(agents, minimum_infection_duration=5, recovery_probability=1.0, vaccinated_recovery_reduction=1)
        self.assertEqual(agent1.status, "R")

if __name__ == '__main__':
    unittest.main()
