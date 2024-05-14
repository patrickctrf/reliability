import numpy as np


def truth_table_generator(header):
    """
Receives a list of names for each column (header) and returns a
integer simple truth table.
    :param header: List of names for each column.
    """
    # Generate truth values (True or False) for each name
    truth_values = [True, False]

    # Create a meshgrid of truth values for each name
    truth_combinations = np.array(np.meshgrid(*([truth_values] * len(header)))).T.reshape(-1, len(header))

    # Convert boolean values to 1s and 0s
    truth_table = truth_combinations.astype(int)

    # Generate a binary weight for each column based on its position
    weights = 2 ** np.arange(truth_table.shape[1])[::-1]

    # Calculate the weighted sum of each row to get a unique number for each combination
    sorted_indices = np.dot(truth_table, weights)

    # Use argsort to get the indices that would sort the table
    sorted_truth_table = truth_table[np.argsort(sorted_indices)]

    # Print the sorted truth table
    print("Sorted Truth Table:")
    print(sorted_truth_table)
