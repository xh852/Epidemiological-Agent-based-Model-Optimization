# Advanced Python Group 11 Final Project

## Project Overview

This project is created for DS-GA 1007 Advanced Python. It centers around building, visualizing, and optimizing an epidemiological agent-based model that builds upon the SIR (Suspectible, Infectious, Recovered) model to simulate how an epidemic may unfold. 

Our main research question is how different vaccination roll out methods affect an epidemic depending on when the vaccine is administered, who that vaccine is administered to, and other variables.

Additionally, the project attempts to optimize the model runtime by comparing and combining various optimization strategies learned in class.

## How to Run

To run the basic simulation, from the root directory, run in your terminal
```
python -m basic_sim {duration} {num_agents} {infection_distance} {infection_prob} {minimum_infection_duration} {recovery_prob} {vaccine_availability_day} {daily_vaccine_distribution_count} {initial_vaccine_efficacy} {vaccinated_recovery_reduction}
```

For example,
you can run
```
python -m basic_sim 365 1000 0.1 0.3 7 0.3 50 10 0.95 2
```
which will simulate how an epidemic unfolds with a population of 10,000 agents over 100 days with 0.3 infection and recovery chance. At the end the command will print out the model's runtime and produce a plot of the population counts in the agent-based SIR model.

To view an animation of the agent's locations over time, you can run
```
python -m animation {parameters}
```

To run the unit tests, you can run
```
pytest tests
```

blahblahblah this a test