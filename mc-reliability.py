import numpy as np


def reliability(mtbf=np.array(1.0), time=1):
    lam = 1 / mtbf
    return np.exp(-lam * time)


def is_working(rdn_gen=np.random.default_rng(), rel=np.array(0.5)):
    coin_toss = rdn_gen.uniform(0.0, 1.0, size=rel.size)
    # coin_toss = rdn_gen.exponential(1.0)
    return coin_toss < rel


def series_parallel_series(wk=np.array([1, 1, 1, 1])):
    if len(wk) == 4:
        return wk[0] * wk[-1] * (wk[1] + wk[2]) > 0


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
    # Adjusts for replicability matters
    # seed = 12345
    rng = np.random.default_rng(seed)

    # Defining the reliability for the case
    rel_eqs = reliability_function(mtbf_list, time=time)

    # Monte Carlo coding
    results = list()
    i = 0
    while i < runs:
        wk = is_working(rng, rel=rel_eqs)
        working = working_function(wk)
        results.append(working)
        i = i + 1

    return results


if __name__ == '__main__':
    # Usage example of this
    mtbf_eq1 = 1 / 0.5
    mtbf_eq2 = 1 / 0.3
    mtbf_eq3 = 1 / 0.4
    mtbf_eq4 = 1 / 0.2
    mtbfs = np.array([
        mtbf_eq1,
        mtbf_eq2,
        mtbf_eq3,
        mtbf_eq4,
    ])
    sim_runs = monte_carlo_run(mtbf_list=mtbfs, time=1)
    print(sum(sim_runs) / len(sim_runs))
