import math
import random
from agent import Agent

def infect(agent_list, infection_distance, infection_probability):
    """
    Infects any susceptible agents within a given distance of an infected agent, with a given infection probability.

    Args:
    - agent_list: A list of agents.
    - infection_distance: A float representing the maximum distance at which other agents can be infected.
    - infection_probability: A float representing the probability of infection if an agent is within infection_distance.

    Returns:
    - None
    """
    infected_agents = [agent for agent in agent_list if agent.status == "I"]
    susceptible_agents = [agent for agent in agent_list if agent.status == "S"]
    for infected_agent in infected_agents:
        infected_location = infected_agent.location
        for susceptible_agent in susceptible_agents:
            susceptible_location = susceptible_agent.location
            distance = math.sqrt((infected_location[0] - susceptible_location[0]) ** 2 + (infected_location[1] - susceptible_location[1]) ** 2)
            if distance <= infection_distance:
                if random.random() < infection_probability:
                    susceptible_agent.status = 'I'
                    susceptible_agent.reset_days_with_status()
    
def recover(agents, minimum_infection_duration, recovery_probability):
    """
    Recovers agents they have been infected for at least minimum_infection_duration days, with a given recovery probability.

    Args:
    - agents: A list of agents.
    - minimum_infection_duration: An int representing the minimum number of days an infected agent takes to recover.
    - recovery_probability: A float representing the probability of an infected agent recovering.

    Returns:
    - None
    """
    for agent in agents:
        if agent.status == 'I' and agent.days_with_status >= minimum_infection_duration:
            if random.random() < recovery_probability:
                agent.status = 'R'
                agent.reset_days_with_status()