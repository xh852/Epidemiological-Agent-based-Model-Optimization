import sys
import matplotlib.pyplot as plt
import random
import time
import numpy as np
from agent import Agent
from transition import infect, recover, distribute_random_vaccine
from location import generate_random_location, snap_to_edge

def main(duration, num_agents, infection_distance, infection_probability, minimum_infection_duration, recovery_probability, vaccine_availability_day, daily_vaccine_distribution_count, initial_vaccine_efficacy=0.95, vaccinated_recovery_reduction=2):
    # Initialize the list of agents
    agents = [Agent("S", (random.random(), random.random())) for _ in range(num_agents)]

    # Set one agent as patient zero
    agents[0].status = "I"

    # Initialize status counts
    status_counts = {"S": np.zeros(duration+1), "I": np.zeros(duration+1), "R": np.zeros(duration+1)}

    # Run simulation for given duration
    for day in range(duration):
         # Update status counts for current day
        status_counts["S"][day] = np.count_nonzero([agent.status == "S" for agent in agents])
        status_counts["I"][day] = np.count_nonzero([agent.status == "I" for agent in agents])
        status_counts["R"][day] = np.count_nonzero([agent.status == "R" for agent in agents])

        # Update agent days with status and locations
        max_distance = 0.01
        for agent in agents:
            agent.increase_days_with_status()
            new_location = generate_random_location(agent.location, max_distance)
            new_location = snap_to_edge(new_location, 0, 0, 1, 1)
            agent.location = new_location

        # Distribute vaccines
        distribute_random_vaccine(agents, vaccine_availability_day, daily_vaccine_distribution_count, initial_vaccine_efficacy, day)

        # Infect agents
        infect(agents, infection_distance, infection_probability)

        # Recover agents
        recover(agents, minimum_infection_duration, recovery_probability, vaccinated_recovery_reduction)

    # Update status counts for last day
    status_counts["S"][duration] = np.count_nonzero([agent.status == "S" for agent in agents])
    status_counts["I"][duration] = np.count_nonzero([agent.status == "I" for agent in agents])
    status_counts["R"][duration] = np.count_nonzero([agent.status == "R" for agent in agents])

    # Plot status counts over time
    plt.plot(status_counts["S"], label="Susceptible")
    plt.plot(status_counts["I"], label="Infected")
    plt.plot(status_counts["R"], label="Recovered")
    plt.xlabel("Day")
    plt.ylabel("Number of Agents")
    plt.title("Agent-based Simulation")
    plt.legend()
    plt.savefig("plot_random_vaccine_sim_optvec_{}_{}_{}_{}_{}_{}_{}_{}_{}_{}.png".format(duration, num_agents, infection_distance, infection_probability, minimum_infection_duration, recovery_probability, vaccine_availability_day, daily_vaccine_distribution_count, initial_vaccine_efficacy, vaccinated_recovery_reduction))




if __name__ == "__main__":
    duration = int(sys.argv[1])
    num_agents = int(sys.argv[2])
    infection_distance = float(sys.argv[3])
    infection_probability = float(sys.argv[4])
    minimum_infection_duration = int(sys.argv[5])
    recovery_probability = float(sys.argv[6])
    vaccine_availability_day = int(sys.argv[7])
    daily_vaccine_distribution_count = int(sys.argv[8])
    initial_vaccine_efficacy = float(sys.argv[9])
    vaccinated_recovery_reduction = int(sys.argv[10])

    start_time = time.time()
    main(duration, num_agents, infection_distance, infection_probability, minimum_infection_duration, recovery_probability, vaccine_availability_day, daily_vaccine_distribution_count, initial_vaccine_efficacy, vaccinated_recovery_reduction)
    end_time = time.time()
    print(f"Model runtime: {end_time - start_time}")