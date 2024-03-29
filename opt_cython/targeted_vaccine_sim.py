import sys
import matplotlib.pyplot as plt
import random
import time
from agent import Agent
from transition import infect, recover, distribute_targeted_vaccine
from location import generate_random_location, snap_to_edge

def main(duration, num_agents, infection_distance, infection_probability, minimum_infection_duration, recovery_probability, vaccine_availability_day, daily_vaccine_distribution_count, initial_vaccine_efficacy=0.95, vaccinated_recovery_reduction=2, immunodeficient_proportion = 0.1, infection_probability_increase = 0.4, complete_rollout_day=100):
    # Initialize random seed
    random.seed(42)

    # Initialize the list of agents
    agents = [Agent("S", (random.random(), random.random()), targetable = False, immunodeficient = random.random() < immunodeficient_proportion) for _ in range(num_agents)]

    # Set one agent as patient zero
    agents[0].status = "I"

    # Initialize status counts
    status_counts = {"S": [], "I": [], "R": []}

    for agent in agents:
        if agent.immunodeficient == True:
            agent.targetable = True

    # Run simulation for given duration
    for day in range(duration):
        # Update status counts for current day
        for status in ["S", "I", "R"]:
            count = sum(1 for agent in agents if agent.status == status)
            status_counts[status].append(count)

        # Update agent days with status, locations, and targetability
        for agent in agents:
            agent.increase_days_with_status()
            max_distance = 0.01
            new_location = generate_random_location(agent.location, max_distance)
            new_location = snap_to_edge(new_location, 0, 0, 1, 1)
            agent.location = new_location
            if day == complete_rollout_day:
                agent.targetable = True

        # Distribute vaccines
        distribute_targeted_vaccine(agents, vaccine_availability_day, daily_vaccine_distribution_count, initial_vaccine_efficacy, day)

        # Infect agents
        infect(agents, infection_distance, infection_probability, infection_probability_increase)

        # Recover agents
        recover(agents, minimum_infection_duration, recovery_probability, vaccinated_recovery_reduction)

    # Add final day status counts
    for status in ["S", "I", "R"]:
        count = sum(1 for agent in agents if agent.status == status)
        status_counts[status].append(count)

    # Plot status counts over time
    plt.plot(status_counts["S"], label="Susceptible")
    plt.plot(status_counts["I"], label="Infected")
    plt.plot(status_counts["R"], label="Recovered")
    plt.xlabel("Day")
    plt.ylabel("Number of Agents")
    plt.title("Agent-based Simulation")
    plt.legend()
    plt.savefig("plot_targeted_vaccine_sim_optcyt_{}_{}_{}_{}_{}_{}_{}_{}_{}_{}_{}_{}_{}.png".format(duration, num_agents, infection_distance, infection_probability, minimum_infection_duration, recovery_probability, vaccine_availability_day, daily_vaccine_distribution_count, initial_vaccine_efficacy, vaccinated_recovery_reduction, immunodeficient_proportion, infection_probability_increase, complete_rollout_day))

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
    immunodeficient_proportion = float(sys.argv[11])
    infection_probability_increase = float(sys.argv[12])
    complete_rollout_day = float(sys.argv[13])

    start_time = time.time()
    main(duration, num_agents, infection_distance, infection_probability, minimum_infection_duration, recovery_probability, vaccine_availability_day, daily_vaccine_distribution_count, initial_vaccine_efficacy, vaccinated_recovery_reduction, immunodeficient_proportion, infection_probability_increase, complete_rollout_day)
    end_time = time.time()
    print(f"Model runtime: {end_time - start_time}")