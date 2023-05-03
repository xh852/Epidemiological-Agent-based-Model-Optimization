import random
import numpy as np
from numba import jit
# import itertools
from agent import Agent

def distribute_random_vaccine(agent_list, vaccine_availability_day, daily_vaccine_distribution_count, vaccine_efficacy=0.95, current_day=0):
    """
    Distributes a specific number of vaccines to susceptible agents randomly in the agent list after the vaccine becomes available.

    Args:
    - agent_list (list): A list of Agent objects.
    - vaccine_availability_day (int): The day when the vaccine becomes available.
    - daily_vaccine_distribution_count (int): The number of vaccines distributed daily after the vaccine becomes available.
    - vaccine_efficacy (float): A float between 0 and 1 representing the initial efficacy of the vaccine.
    - current_day (int): The current day of the simulation.

    Returns:
    - None
    """
    if current_day >= vaccine_availability_day:
        susceptible_agents = [agent for agent in agent_list if agent.status == "S" if agent.vaccinated == False]
        selected_agents = random.sample(susceptible_agents, min(daily_vaccine_distribution_count, len(susceptible_agents)))

        for agent in selected_agents:
            agent.vaccinated = True
            agent.vaccine_efficacy = vaccine_efficacy

def distribute_targeted_vaccine(agent_list, vaccine_availability_day, daily_vaccine_distribution_count, vaccine_efficacy=0.95, current_day=0):
    """
    Distributes a specific number of vaccines to susceptible and targetable agents in agent list after the vaccine becomes available.

    Args:
    - agent_list (list): A list of Agent objects.
    - vaccine_availability_day (int): The day when the vaccine becomes available.
    - daily_vaccine_distribution_count (int): The number of vaccines distributed daily after the vaccine becomes available.
    - vaccine_efficacy (float): A float between 0 and 1 representing the initial efficacy of the vaccine.
    - current_day (int): The current day of the simulation.

    Returns:
    - None
    """
    if current_day >= vaccine_availability_day:
        susceptible_agents = [agent for agent in agent_list if agent.status == "S" if agent.targetable == True if agent.vaccinated == False]
        selected_agents = random.sample(susceptible_agents, min(daily_vaccine_distribution_count, len(susceptible_agents)))

        for agent in selected_agents:
            agent.vaccinated = True
            agent.vaccine_efficacy = vaccine_efficacy

@jit
def infect(agent_list, infection_distance, infection_probability, infection_probability_increase = 0.4):
    """
    Infects any susceptible agents within a given distance of an infected agent, with a given infection probability.

    Args:
    - agent_list: A list of agents.
    - infection_distance: A float representing the maximum distance at which other agents can be infected.
    - infection_probability: A float representing the probability of infection if an agent is within infection_distance.
    - infection_probability_increase: A flat increase for how likely an immunodeficient person gets infected

    Returns:
    - None
    """
    # Get infected and susceptible agent locations
    infected_locations = np.array([list(agent.location) for agent in agent_list if agent.status == "I"])
    susceptible_agents = np.array([[agent.location[0],agent.location[1], agent] for agent in agent_list if agent.status == "S"])
    if len(infected_locations) == 0 or len(susceptible_agents) == 0:
        #Only proceed if infected AND susceptible agents exist
        return
    susceptible_locations = susceptible_agents[:, :2].astype("float64")
    susceptible_info = susceptible_agents[:, 2:]

    # Get distance between every infected and susceptible pair
    distances = np.sqrt(np.sum((np.array(infected_locations)[:, np.newaxis, :] - np.array(susceptible_locations)[np.newaxis, :, :])**2, axis=-1))

    # # Compute distances for all pairs of agents between A and B
    # distances = [np.sqrt(np.sum((np.array(a) - np.array(b))**2)) for a, b in itertools.product(infected_locations, susceptible_locations)]
    # distances = np.array(distances).reshape(len(infected_locations), len(susceptible_locations))

    # Find indices of distances below the threshold and update susceptible agents
    infectable_agents = np.argwhere(distances < infection_distance)
    infectable_agents = infectable_agents[:, 1]

    for idx in infectable_agents:
        agent = susceptible_info[idx][0]
        
        adjusted_infection_probability = (infection_probability + agent.immunodeficient*infection_probability_increase) * (1 - agent.vaccine_efficacy)
        if random.random() < adjusted_infection_probability:
            agent.status = 'I'
            agent.reset_days_with_status()

def recover(agents, minimum_infection_duration, recovery_probability, vaccinated_recovery_reduction=0):
    """
    Recovers agents they have been infected for at least minimum_infection_duration days, with a given recovery probability.

    Args:
    - agents: A list of agents.
    - minimum_infection_duration: An int representing the minimum number of days an infected agent takes to recover.
    - recovery_probability: A float representing the probability of an infected agent recovering.
    - vaccinated_recovery_reduction: An int representing the reduction in recovery time for vaccinated agents.

    Returns:
    - None
    """
    for agent in agents:
        if agent.status == 'I' and agent.days_with_status >= minimum_infection_duration - (vaccinated_recovery_reduction if agent.vaccinated else 0):
            if random.random() < recovery_probability:
                agent.status = 'R'
                agent.reset_days_with_status()
