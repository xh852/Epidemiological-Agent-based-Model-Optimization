# Advanced Python Group 11 Final Project

## Project Overview

This project is created for DS-GA 1007 Advanced Python. It centers around building, visualizing, and optimizing an epidemiological agent-based model that builds upon the SIR (Suspectible, Infectious, Recovered) model to simulate how an epidemic may unfold. 

Our main research question is how different vaccination roll out methods affect an epidemic depending on when the vaccine is administered, who that vaccine is administered to, and other variables.

Additionally, the project attempts to optimize the model runtime by comparing and combining various optimization strategies learned in class.

## How to Run

To run the basic simulation, from the root directory, run in your terminal
```
python -m basic_sim {duration} {num_agents} {infection_distance} {infection_prob} {minimum_infection_duration} {recovery_prob}
```

For example,
you can run
```
python -m basic_sim 100 1000 0.05 0.3 7 0.3
```
which will simulate how an epidemic unfolds with a population of 10,000 agents over 100 days with 0.3 infection and recovery chance. At the end the command will print out the model's runtime and produce a plot of the population counts in the agent-based SIR model.

To run the random vaccine simulation, from the root directory, run in your terminal
```
python -m random_vaccine_sim {duration} {num_agents} {infection_distance} {infection_prob} {minimum_infection_duration} {recovery_prob} {vaccine_availability_day} {daily_vaccine_distribution_count} {initial_vaccine_efficacy} {vaccinated_recovery_reduction}
```

For example,
you can run
```
python -m random_vaccine_sim 365 1000 0.05 0.3 7 0.3 50 10 0.95 2
```

To run the targeted vaccine simulation, from the root directory, run in your terminal
```
python -m targeted_vaccine_sim {duration} {num_agents} {infection_distance} {infection_prob} {minimum_infection_duration} {recovery_prob} {vaccine_availability_day} {daily_vaccine_distribution_count} {initial_vaccine_efficacy} {vaccinated_recovery_reduction}
{immunodeficient_proportion} {infection_probability_increase} {complete_rollout_day}
```

For example,
you can run
```
python -m targeted_vaccine_sim 365 1000 0.05 0.1 7 0.1 50 10 0.95 2 0.1 0.4 100
```

To view an animation of the agent's locations over time, you can run
```
python -m animation {parameters}
```

To run the unit tests, you can run
```
pytest tests
```

## Optimization Methods

### Cython
Cython may be used to translate Python code into optimized C code, and compile C code as extension modules for Python. Cython also allows for the use of C data types in Python. There are two main benefits of Cython:
* Speed: Use of C compiliation allows for fast execution. Note, simple numerical programs that use lower-level C may not see a difference. However, programs that use many iterations can improve by many orders of magnitude.
* Easy calling into C code: Use of C libraries and data types allows for more efficient C compilation, while still allowing the user to code in Python.

Source: [Cython Docs](https://cython.readthedocs.io/en/latest/src/quickstart/overview.html); [NYU-CDS Notes](https://nyu-cds.github.io/python-cython/)

### Vectorization
Vectorization with NumPy is useful to write more efficient code for the following reasons:
* Compute operations in parallel - for instance, carry out arithmetic on an entire vector or matrix.
* NumPy is implemented in a low-level language (C), that operates quickly on large data.


### Testing Optimization Techniques (Cython, Vectorization)
To compare time efficiency of optimization methods vs. the original code, use the following command:
```
python optimization_time.py basic_sim.py 100 1000 0.05 0.3 7 0.3
python optimization_time.py random_vaccine_sim.py 365 1000 0.05 0.3 7 0.3 50 10 0.95 2
```

### Line Profiler
python -m basic_sim 100 1000 0.05 0.3 7 0.3 True

```
Output example: Total time: 2.56755 s
Function: main at line 9

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
     9                                           def main(duration, num_agents, infection_distance, infection_probability, minimum_infection_duration, recovery_probability, profile=True):
    10                                               # Initialize random seed
    11         1     135000.0 135000.0      0.0      random.seed(42)   
    12                                               
    13                                               # Initialize the list of agents
    14         1    1112000.0 1112000.0      0.0      agents = [Agent("S", (random.random(), random.random())) for _ in range(num_agents)]
    15                                           
    16                                               # Set one agent as patient zero
    17         1      14000.0  14000.0      0.0      agents[0].status = "I"
    18                                           
    19                                               # Initialize status counts
    20         1       6000.0   6000.0      0.0      status_counts = {"S": [], "I": [], "R": []}
    21                                           
    22                                           
    23                                               # Run simulation for given duration
    24       100      21000.0    210.0      0.0      for _ in range(duration):
    25                                                   # Update status counts for current day
    26       300      88000.0    293.3      0.0          for status in ["S", "I", "R"]:
    27       300   54018000.0 180060.0      2.1              count = sum(1 for agent in agents if agent.status == status)
    28       300     139000.0    463.3      0.0              status_counts[status].append(count)
    29                                           
    30                                                   # Update agent days with status and locations
    31    100000   18508000.0    185.1      0.7          for agent in agents:
    32    100000   46577000.0    465.8      1.8              agent.increase_days_with_status()
    33    100000   14458000.0    144.6      0.6              max_distance = 0.01
    34    100000  159658000.0   1596.6      6.2              new_location = generate_random_location(agent.location, max_distance)
    35    100000   70931000.0    709.3      2.8              new_location = snap_to_edge(new_location, 0, 0, 1, 1)
    36    100000   20340000.0    203.4      0.8              agent.location = new_location
    37                                           
    38                                                   # Infect agents
    39       100 2114803000.0 21148030.0     82.4          infect(agents, infection_distance, infection_probability)
    40                                           
    41                                                   # Recover agents
    42       100   13293000.0 132930.0      0.5          recover(agents, minimum_infection_duration, recovery_probability)
    43                                           
    44                                               # Add final day status counts
    45         3       1000.0    333.3      0.0      for status in ["S", "I", "R"]:
    46         3     544000.0 181333.3      0.0          count = sum(1 for agent in agents if agent.status == status)
    47         3          0.0      0.0      0.0          status_counts[status].append(count)
    48                                           
    49                                               # Plot status counts over time
    50         1    1987000.0 1987000.0      0.1      plt.plot(status_counts["S"], label="Susceptible")
    51         1     502000.0 502000.0      0.0      plt.plot(status_counts["I"], label="Infected")
    52         1     453000.0 453000.0      0.0      plt.plot(status_counts["R"], label="Recovered")
    53         1      83000.0  83000.0      0.0      plt.xlabel("Day")
    54         1      24000.0  24000.0      0.0      plt.ylabel("Number of Agents")
    55         1     177000.0 177000.0      0.0      plt.title("Agent-based Simulation")
    56         1    3872000.0 3872000.0      0.2      plt.legend()
    57         1   45796000.0 45796000.0      1.8      plt.savefig("plot_basic_sim_{}_{}_{}_{}_{}_{}.png".format(duration, num_agents, infection_distance, infection_probability, minimum_infection_duration, recovery_probability))
    58                                           
    59                                               # line_profiler
    60         1       2000.0   2000.0      0.0      import line_profiler
    61         1          0.0      0.0      0.0      if profile:
    62                                                   profiler = line_profiler.LineProfiler(main)
    63                                                   profiler.enable()
    64         1       9000.0   9000.0      0.0          main(duration, num_agents, infection_distance, infection_probability, minimum_infection_duration, recovery_probability, False)
    65                                                   profiler.disable()
    66                                                   profiler.print_stats()

Model runtime: 4.136656284332275
```

