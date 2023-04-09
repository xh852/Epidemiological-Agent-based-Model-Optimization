import sys
import matplotlib.pyplot as plt
import random
from agent import Agent
from transition import infect, recover
from location import generate_random_location, snap_to_edge

def main(duration, num_agents, infection_probability, recovery_probability):
    # Initialize the list of agents
    agents = [Agent("S", (random.random(), random.random())) for _ in range(num_agents)]

    # Set one agent as patient zero
    agents[0].status = "I"

    # Initialize status counts
    status_counts = {"S": [], "I": [], "R": []}


    # Run simulation for given duration
    for _ in range(duration):
        # Update status counts for current day
        for status in ["S", "I", "R"]:
            count = sum(1 for agent in agents if agent.status == status)
            status_counts[status].append(count)

        # Update agent days with status and locations
        for agent in agents:
            agent.increase_days_with_status()
            max_distance = 0.01
            new_location = generate_random_location(agent.location, max_distance)
            new_location = snap_to_edge(new_location, 0, 0, 1, 1)
            agent.location = new_location

        # Infect agents
        infect(agents, infection_distance=0.01, infection_probability=infection_probability)

        # Recover agents
        recover(agents, minimum_infection_duration=7, recovery_probability=recovery_probability)

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
    plt.show()

if __name__ == "__main__":
    duration = int(sys.argv[1])
    num_agents = int(sys.argv[2])
    infection_probability = float(sys.argv[3])
    recover_probability = float(sys.argv[4])
    main(duration, num_agents, infection_probability, recover_probability)