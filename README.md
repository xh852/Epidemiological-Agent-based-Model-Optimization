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
{essential_worker_proportion} {infection_probability_increase} {complete_rollout_day}
```

For example,
you can run
```
python -m targeted_vaccine_sim 365 1000 0.05 0.2 7 0.2 50 10 0.95 2 0.1 2 100
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

### Testing Optimization Techniques
To compare time efficiency of optimization methods vs. the original code, use the following command:
```
python optimization_time.py
```

