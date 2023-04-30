import math
import random
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
        susceptible_agents = [agent for agent in agent_list if agent.status == "S"]
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
        susceptible_agents = [agent for agent in agent_list if agent.status == "S" if agent.targetable == True]
        selected_agents = random.sample(susceptible_agents, min(daily_vaccine_distribution_count, len(susceptible_agents)))

        for agent in selected_agents:
            agent.vaccinated = True
            agent.vaccine_efficacy = vaccine_efficacy

def infect(agent_list, infection_distance, infection_probability, infection_probability_increase = 0.4):
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
                adjusted_infection_probability = (infection_probability + susceptible_agent.essential_worker*infection_probability_increase) * (1 - susceptible_agent.vaccine_efficacy)
                if random.random() < adjusted_infection_probability:
                    susceptible_agent.status = 'I'
                    susceptible_agent.reset_days_with_status()
    
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