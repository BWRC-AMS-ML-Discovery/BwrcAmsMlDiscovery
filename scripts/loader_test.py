from autockt.envs.ngspice_vanilla_opamp import ParamManager


def main():
    params = [
        [1, 100, 1],
        [1, 100, 1],
        [1, 100, 1],
        [1, 100, 1],
        [1, 100, 1],
        [1, 100, 1],
        [1, 100, 1],
    ]
    norm = [350, 0.001, 60, 950000.0]
    target = [
        [200, 400],
        [1.0e6, 2.5e7],
        [60, 60.0000001],
        [0.0001, 0.01],
    ]

    print(ParamManager.load_spec(params, target, norm))


if __name__ == "__main__":
    main()
