def main():
    from autockt_shared import TwoStageOpAmpNgmInput
    from eval_engines.TwoStageOpAmp_ngm import ngm_opamp_inner

    inp = TwoStageOpAmpNgmInput(
        wtail1=10,
        wtail2=10,
        wcm=10,
        win=10,
        wref=10,
        wd1=10,
        wd=10,
        wn_gm=10,
        wtail=10,
        wtailr=10,
        Cc=100e-15,
        Rf=1e3,
        VDD=1.2,
        Vcm=1,
        Vref=1,
        ibias=2e-6,
    )
    r = ngm_opamp_inner(inp)
    print(r)


def test():
    main()


if __name__ == "__main__":
    main()
