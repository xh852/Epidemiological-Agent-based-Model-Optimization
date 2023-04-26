import timeit

def time_opt_cython():
    print("Timing Optimization Method: Cython")
    python_command = "python basic_sim.py 100 1000 0.05 0.3 7 0.3"
    cython_command = "python opt_cython/basic_sim.py 100 1000 0.05 0.3 7 0.3"

    python = timeit.timeit("os.system('{}')".format(python_command), setup='import os', number=5)
    cython = timeit.timeit("os.system('{}')".format(cython_command), setup='import os',number=5)
    print()
    print("Python Time: ", python)
    print("Cython Time: ", cython)
    print(f"{python/cython}x times faster")

if __name__ == "__main__":
    time_opt_cython()