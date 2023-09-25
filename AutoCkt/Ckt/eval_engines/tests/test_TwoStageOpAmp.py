def main():
    from autockt_shared import OpAmpInput
    from eval_engines.TwoStageOpAmp import opamp_inner

    inp = OpAmpInput(
        mp1=34,
        mn1=34,
        mp3=34,
        mn3=34,
        mn4=34,
        mn5=15,
        cc=2.1e-12,
    )
    r = opamp_inner(inp)
    print(r)


def test():
    main()


if __name__ == "__main__":
    main()
