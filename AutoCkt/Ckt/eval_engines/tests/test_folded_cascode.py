def main():
    from autockt_shared import FoldedCascodeInput
    from eval_engines.FoldedCascode import FoldedCascode_inner

    inp = FoldedCascodeInput(
        w1_2=10,
        w5_6=10,
        w7_8=10,
        w9_10=10,
        w11_12=10,
        w13_14=10,
        w15_16=10,
        w17=10,
        w18=10,
        cl=10e-15,
        cc=10e-15,
        rc=1e3,
        wb0=10,
        wb1=10,
        wb2=10,
        wb3=10,
        wb4=10,
        wb5=10,
        wb6=10,
        wb7=10,
        wb8=10,
        wb9=10,
        wb10=10,
        wb11=10,
        wb12=10,
        wb13=10,
        wb14=10,
        wb15=10,
        wb16=10,
        wb17=10,
        wb18=10,
        wb19=10,
        ibias=40e-6,
        Vcm=1,
    )

    r = FoldedCascode_inner(inp)
    print(r)


def test():
    main()


if __name__ == "__main__":
    main()
