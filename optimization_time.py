import timeit
import sys

def time_opt(command, number=1):
    print("-"*50,"\nTiming Original Method")
    python = timeit.timeit("os.system('{}')".format("python " + command), setup='import os', number=number)
    print("Python Time: {} sec".format(python))

    print("-"*50,"\nTiming Optimization Method: Numba")
    numba = timeit.timeit("os.system('{}')".format("python opt_numba/" + command), setup='import os',number=number)
    print("Vectorization Time: {} sec".format(numba))
    print(f"{python/numba}x times faster")

    print("-"*50,"\nTiming Optimization Method: Cython")
    cython = timeit.timeit("os.system('{}')".format("python opt_cython/" + command), setup='import os',number=number)
    print("Cython Time: {} sec".format(cython))
    print(f"{python/cython}x times faster")

    print("-"*50,"\nTiming Optimization Method: Vectorization")
    vectorization = timeit.timeit("os.system('{}')".format("python opt_vectorization/" + command), setup='import os',number=number)
    print("Vectorization Time: {} sec".format(vectorization))
    print(f"{python/vectorization}x times faster")

    print("-"*50,"\nTiming Optimization Method: Cython AND Vectorization")
    cython_vec = timeit.timeit("os.system('{}')".format("python opt_cython+vect/" + command), setup='import os',number=number)
    print("Cython AND Vectorization Time: {} sec".format(cython_vec))
    print(f"{python/cython_vec}x times faster")
    

if __name__ == "__main__":
    command = sys.argv[1] # basic_sim.py, random_vaccine_sim.py, etc.
    duration = int(sys.argv[2])
    num_agents = int(sys.argv[3])
    infection_distance = float(sys.argv[4])
    infection_probability = float(sys.argv[5])
    minimum_infection_duration = int(sys.argv[6])
    recovery_probability = float(sys.argv[7])
    vaccine_availability_day = ""
    daily_vaccine_distribution_count = ""
    initial_vaccine_efficacy = ""
    vaccinated_recovery_reduction = ""
    immunodeficient_proportion = ""
    infection_probability_increase = ""
    complete_rollout_day = ""

    if len(sys.argv) > 8:
        vaccine_availability_day = int(sys.argv[8])
        daily_vaccine_distribution_count = int(sys.argv[9])
        initial_vaccine_efficacy = float(sys.argv[10])
        vaccinated_recovery_reduction = int(sys.argv[11])
    
    if len(sys.argv) > 12:
        immunodeficient_proportion = float(sys.argv[12])
        infection_probability_increase = float(sys.argv[13])
        complete_rollout_day = float(sys.argv[14])
    

    command += " {} {} {} {} {} {} {} {} {} {} {} {} {}".format(duration, num_agents, infection_distance, infection_probability, 
                                           minimum_infection_duration, recovery_probability, 
                                           vaccine_availability_day, daily_vaccine_distribution_count, 
                                           initial_vaccine_efficacy, vaccinated_recovery_reduction,
                                           immunodeficient_proportion, infection_probability_increase,
                                           complete_rollout_day)

    time_opt(command)
