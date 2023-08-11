PARAMS_RANGE = [
    ["mp1", [1, 100, 1]],
    ["mp3", [1, 100, 1]],
    ["mn1", [1, 100, 1]],
    ["mn3", [1, 100, 1]],
    ["mn4", [1, 100, 1]],
    ["mn5", [1, 100, 1]],
    ["cc", [0.1e-12, 10.0e-12, 0.1e-12]],
]

NORM_CONSTANT = [["gain", 350], ["ibias", 0.001], ["phm", 60], ["ugbw", 950000.0]]

TARGET_RANGE = [
    ["gain_min", [200, 400]],
    ["ibias_max", [1.0e6, 2.5e7]],
    ["phm_min", [60, 60.0000001]],
    ["ugbw_min", [0.0001, 0.01]],
]
