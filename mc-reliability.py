import numpy as np


# Define a function to calculate reliability based on Mean Time Between Failures (MTBF)
def reliability(mtbf=np.array(1.0), time=1):
    # Calculate the failure rate (lambda) as the inverse of MTBF
    lam = 1 / mtbf
    # Return the exponential of the negative product of lambda and time
    return np.exp(-lam * time)


# Define a function to simulate whether equipment is working based on reliability
def is_working(rdn_gen=np.random.default_rng(), rel=np.array(0.5)):
    # Generate a random number between 0 and 1 for each element in the reliability array
    coin_toss = rdn_gen.uniform(0.0, 1.0, size=rel.size)
    # Return a boolean array where True indicates the equipment is working (random number < reliability)
    return coin_toss < rel


# Define a function to evaluate a series-parallel-series system's working status
def series_parallel_series(wk=np.array([1, 1, 1, 1])):
    # Check if the input array has four elements
    if len(wk) == 4:
        # Return True if the series-parallel-series system is working
        return wk[0] * wk[-1] * (wk[1] + wk[2]) > 0


# Define a function to run a Monte Carlo simulation
def monte_carlo_run(
        mtbf_list,
        time=1,
        runs=10e4,
        seed=12345,
        reliability_function=reliability,
        working_function=series_parallel_series,
):
    """

    :param mtbf_list: list with MTBF values for your case
    :param time: the time value that you want to verify if your system is working
    :param runs: number of monte carlo runs
    :param seed: the seed number for replicability purposes (default 12345)
    :param reliability_function: a function that describes how your equipment degrades
    :param working_function: the function that verifies whether your system is working or not
    :return: vector with length runs with the results of the simulation,
        whether either is properly working for a given case (True) or not (False)

    This function implements a naïve implementation of Monte Carlo simulation. The reliability_function receives a param
    that describes the way that your piece of equipment degrades over time (its default value is an internal function
    that models an exponential degradation without correction).

    Considering the time and the reliability parameters (this implementation considers only MTBF), it is possible to
    assert whether one piece of equipment is properly working or not, by comparing a random variable to the expected
    reliability for a given time.

    The results for each piece of equipment will be tested within the customized
    system working function (working_function). The compiled result will be returned then appended to the output
    of this monte carlo function.

    The output of this function is a vector of Boolean values that holds True for working cases and False for not
    working ones. It is up to the user to perform additional calculations with the results (summarize etc).
    """
    # Initialize a random number generator with a given seed for reproducibility
    rng = np.random.default_rng(seed)

    # Calculate the reliability for each MTBF value at the given time
    rel_eqs = reliability_function(mtbf_list, time=time)

    # Initialize a list to store the results of each run
    results = list()
    # Loop over the number of runs
    i = 0
    while i < runs:
        # Determine if the system is working based on the reliability
        wk = is_working(rng, rel=rel_eqs)
        # Evaluate the system's working status using the specified function
        working = working_function(wk)
        # Append the result to the list
        results.append(working)
        # Increment the counter
        i = i + 1

    # Return the list of results
    return results


# Main execution block
if __name__ == '__main__':
    # Define MTBF values for four pieces of equipment
    mtbf_eq1 = 1 / 0.5
    mtbf_eq2 = 1 / 0.3
    mtbf_eq3 = 1 / 0.4
    mtbf_eq4 = 1 / 0.2
    # Create an array of MTBF values
    mtbfs = np.array([
        mtbf_eq1,
        mtbf_eq2,
        mtbf_eq3,
        mtbf_eq4,
    ])
    # Run the Monte Carlo simulation
    sim_runs = monte_carlo_run(mtbf_list=mtbfs, time=1)
    # Calculate and print the proportion of runs where the system was working
    print(sum(sim_runs) / len(sim_runs))
