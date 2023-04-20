from unittest.mock import MagicMock, patch
from agent import Agent
from transition import infect, recover

def test_infect_no_infections():
    # Test that no agents become infected when there are no infected agents in the list
    agent1 = Agent("S", (1, 1))
    agent2 = Agent("S", (2, 2))
    agent_list = [agent1, agent2]
    infect(agent_list, 2, 1)
    assert agent1.status == "S"
    assert agent2.status == "S"


def test_infect_single_infection():
    # Test that a single susceptible agent becomes infected when there is a single infected agent nearby
    agent1 = Agent("I", (1, 1))
    agent2 = Agent("S", (2, 2))
    agent_list = [agent1, agent2]
    with patch('random.random', MagicMock(return_value=0.5)):
        infect(agent_list, 2, 1)
    assert agent1.status == "I"
    assert agent2.status == "I"

def test_infect_probability_not_met():
    # Test that a single susceptible agent does not become infected when the infection probability is not met
    agent1 = Agent("I", (1, 1))
    agent2 = Agent("S", (2, 2))
    agent_list = [agent1, agent2]
    with patch('random.random', MagicMock(return_value=0.8)):
        infect(agent_list, 2, 0.5)
    assert agent1.status == "I"
    assert agent2.status == "S"

def test_infect_multiple_infections():
    # Test that multiple susceptible agents become infected when there are multiple infected agents nearby
    agent1 = Agent("I", (1, 1))
    agent2 = Agent("S", (2, 2))
    agent3 = Agent("I", (5, 5))
    agent4 = Agent("S", (6, 6))
    agent_list = [agent1, agent2, agent3, agent4]
    with patch('random.random', MagicMock(return_value=0.5)):
        infect(agent_list, 2, 1)
    assert agent1.status == "I"
    assert agent2.status == "I"
    assert agent3.status == "I"
    assert agent4.status == "I"


def test_infect_infection_distance_0():
    # Test that no agents become infected when the infection distance is 0
    agent1 = Agent("I", (1, 1))
    agent2 = Agent("S", (1, 2))
    agent_list = [agent1, agent2]
    infect(agent_list, 0, 1)
    assert agent1.status == "I"
    assert agent2.status == "S"


def test_infect_infection_probability_0():
    # Test that no agents become infected when the infection probability is 0
    agent1 = Agent("I", (1, 1))
    agent2 = Agent("S", (2, 2))
    agent_list = [agent1, agent2]
    infect(agent_list, 1, 0)
    assert agent1.status == "I"
    assert agent2.status == "S"


def test_infect_infection_probability_1():
    # Test that only agents in range become infected when the infection probability is 1
    agent1 = Agent("I", (1, 1))
    agent2 = Agent("S", (2, 2))
    agent3 = Agent("S", (3, 3))
    agent_list = [agent1, agent2, agent3]
    infect(agent_list, 2, 1)
    assert agent1.status == "I"
    assert agent2.status == "I"
    assert agent3.status == "S"

def test_infect_days_with_status_updates():
    # Test that days with status resets to 0 when an agent gets infected
    agent1 = Agent("I", (1, 1), 1)
    agent2 = Agent("S", (2, 2), 1)
    agent3 = Agent("S", (3, 3), 1)
    agent_list = [agent1, agent2, agent3]
    infect(agent_list, 2, 1)
    assert agent1.days_with_status == 1
    assert agent2.days_with_status == 0
    assert agent3.days_with_status == 1


def test_recover():
    # Create a list of agents with one agent infected for at least the minimum duration
    agent1 = Agent("S", (1, 1), 0)
    agent2 = Agent("I", (2, 2), 5)
    agent3 = Agent("I", (3, 3), 10)
    agent4 = Agent("R", (3, 3), 10)
    agent_list = [agent1, agent2, agent3, agent4]
    minimum_infection_duration = 7
    recover_probability = 0.5

    # Mock the random number generator to always return 0.1
    with patch('random.random', return_value=0.1):
        # Call the recover function
        recover(agent_list, minimum_infection_duration, recover_probability)

    # Check that the infected agent has been updated to recovered
    assert agent1.status == "S"
    assert agent2.status == "I"
    assert agent3.status == "R"
    assert agent4.status == "R"

def test_recover_days_with_status():
    # Create a list of agents with one agent infected for at least the minimum duration
    agent1 = Agent("S", (1, 1), 0)
    agent2 = Agent("I", (2, 2), 5)
    agent3 = Agent("I", (3, 3), 10)
    agent4 = Agent("R", (3, 3), 10)
    agent_list = [agent1, agent2, agent3, agent4]
    minimum_infection_duration = 7
    recover_probability = 0.5

    # Mock the random number generator to always return 0.1
    with patch('random.random', return_value=0.1):
        # Call the recover function
        recover(agent_list, minimum_infection_duration, recover_probability)

    # Check that the infected agent has been updated to recovered
    assert agent1.days_with_status == 0
    assert agent2.days_with_status == 5
    assert agent3.days_with_status == 0
    assert agent4.days_with_status == 10