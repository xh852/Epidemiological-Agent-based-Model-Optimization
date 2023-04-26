import sys
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
from agent import Agent
from transition import infect, recover
from location import generate_random_location, snap_to_edge

def main(duration, num_agents, infection_probability, recovery_probability):
    # Initialize the list of agents
    agents = [Agent("S", (random.random(), random.random())) for _ in range(num_agents)]

    # Create a scatter plot of the agents' initial locations
    fig, ax = plt.subplots()
    ax.set_xlim([0, 1])
    ax.set_ylim([0, 1])
    scatter = ax.scatter([agent.location[0] for agent in agents], [agent.location[1] for agent in agents])

    # Set one agent as patient zero
    agents[0].status = "I"

    # Run simulation for given duration
    def simulate(frame_number):
        for _ in range(duration):
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

            scatter.set_offsets([[agent.location[0], agent.location[1]] for agent in agents])
        return scatter
    
    # Create the animation
    ani = animation.FuncAnimation(fig, simulate, frames=range(duration))
    
    # Show the animation
    plt.show()

if __name__ == "__main__":
    duration = int(sys.argv[1])
    num_agents = int(sys.argv[2])
    infection_probability = float(sys.argv[3])
    recover_probability = float(sys.argv[4])
    main(duration, num_agents, infection_probability, recover_probability)