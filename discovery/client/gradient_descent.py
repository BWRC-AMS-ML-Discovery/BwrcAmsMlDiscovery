import numpy as np

# from shared import ParametersObject, ResultsObject

# class ParametersObject:

#     parameters: dict

# class ResultsObject:
#     results: dict


def gradient_descent(gradient, start, learn_rate, n_iter=100, tolerance=1e-06):
    vector = start
    for _ in range(n_iter):
        diff = -learn_rate * gradient(vector)
        if np.all(np.abs(diff) <= tolerance):
            break
        vector += diff

    return vector


def test_objective(wp, wn):
    wp_constant = 3
    wn_constant = 4
    return (wp - wp_constant) ** 2 + (wn - wn_constant) ** 2


def test_objective_gradient(wp_wn):
    wp = wp_wn[0]
    wn = wp_wn[1]
    return np.array([2 * wp - 6, 2 * wn - 8])


# parameters = ParametersObject({"start": np.array([10.0, 10.0]),
#                                "learn_rate": 0.1,
#                                "iterations": 100})

test_start = np.array([10.0, 10.0])
test_learn_rate = 0.1
test_iterations = 100


result = gradient_descent(test_objective_gradient, test_start, test_learn_rate)

print(
    "wp: "
    + str(result[0])
    + "\nwn: "
    + str(result[1])
    + "\nvalue: "
    + str(test_objective(result[0], result[1]))
)
