# StdLib Imports
import os, tempfile
from pathlib import Path
import re
import random
import copy
from dataclasses import asdict

# PyPi Imports
import numpy as np
import scipy.interpolate as interp
import scipy.optimize as sciopt

# Workspace Imports
from example_shared import (
    AutoCktInput,
    AutoCktOutput,
)


# TODO maybe don't need to save files at all
IO_BASE_DIR = "/tmp/ckt_da_new/"


_raw_file = open(IO_BASE_DIR + "in/" + "two_stage_opamp.cir", "r")
_tmp_lines = _raw_file.readlines()
_raw_file.close()


def _mkdir():
    tmpdir = tempfile.TemporaryDirectory()
    rundir = Path(tmpdir.name).absolute()
    return (tmpdir, rundir)


def create_design(state: AutoCktInput):
    tmpdir, design_folder = _mkdir()
    fpath = os.path.join(design_folder, ".cir")

    lines = copy.deepcopy(_tmp_lines)
    for line_num, line in enumerate(lines):
        if ".include" in line:
            regex = re.compile('\.include\s*"(.*?)"')
            found = regex.search(line)
            if found:
                # current_fpath = os.path.realpath(__file__)
                # parent_path = os.path.abspath(os.path.join(current_fpath, os.pardir))
                # parent_path = os.path.abspath(os.path.join(parent_path, os.pardir))
                # path_to_model = os.path.join(parent_path, 'spice_models/45nm_bulk.txt')
                # lines[line_num] = lines[line_num].replace(found.group(1), path_to_model)
                pass  # do not change the model path
        if ".param" in line:
            for key, value in asdict(state).items():
                regex = re.compile("%s=(\S+)" % (key))
                found = regex.search(line)
                if found:
                    new_replacement = "%s=%s" % (key, str(value))
                    lines[line_num] = lines[line_num].replace(
                        found.group(0), new_replacement
                    )
        if "wrdata" in line:
            regex = re.compile("wrdata\s*(\w+\.\w+)\s*")
            found = regex.search(line)
            if found:
                replacement = os.path.join(design_folder, found.group(1))
                lines[line_num] = lines[line_num].replace(found.group(1), replacement)

    with open(fpath, "w") as f:
        f.writelines(lines)
        f.close()
    return tmpdir, design_folder, fpath


def simulate(fpath):
    info = 0  # this means no error occurred
    command = "ngspice -b %s >/dev/null 2>&1" % fpath
    exit_code = os.system(command)
    # if debug:
    #     print(command)
    #     print(fpath)

    if exit_code % 256:
        # raise RuntimeError('program {} failed!'.format(command))
        info = 1  # this means an error has occurred
    return info


def translate_result(tmpdir, output_path):
    """

    :param output_path:
    :return
        result: dict(spec_kwds, spec_value)
    """

    # use parse output here
    freq, vout, ibias = parse_output(output_path)
    gain = find_dc_gain(vout)
    ugbw = find_ugbw(freq, vout)
    phm = find_phm(freq, vout)

    spec = AutoCktOutput(
        ugbw=ugbw,
        gain=gain,
        phm=phm,
        ibias=ibias,
    )

    tmpdir.cleanup()
    return spec


def parse_output(output_path):
    ac_fname = os.path.join(output_path, "ac.csv")
    dc_fname = os.path.join(output_path, "dc.csv")

    if not os.path.isfile(ac_fname) or not os.path.isfile(dc_fname):
        print("ac/dc file doesn't exist: %s" % output_path)

    ac_raw_outputs = np.genfromtxt(ac_fname, skip_header=1)
    dc_raw_outputs = np.genfromtxt(dc_fname, skip_header=1)
    freq = ac_raw_outputs[:, 0]
    vout_real = ac_raw_outputs[:, 1]
    vout_imag = ac_raw_outputs[:, 2]
    vout = vout_real + 1j * vout_imag
    ibias = -dc_raw_outputs[1]

    return freq, vout, ibias


def find_dc_gain(vout):
    return np.abs(vout)[0]


def find_ugbw(freq, vout):
    gain = np.abs(vout)
    ugbw, valid = _get_best_crossing(freq, gain, val=1)
    if valid:
        return ugbw
    else:
        return freq[0]


def find_phm(freq, vout):
    gain = np.abs(vout)
    phase = np.angle(vout, deg=False)
    phase = np.unwrap(phase)  # unwrap the discontinuity
    phase = np.rad2deg(phase)  # convert to degrees
    #
    # plt.subplot(211)
    # plt.plot(np.log10(freq[:200]), 20*np.log10(gain[:200]))
    # plt.subplot(212)
    # plt.plot(np.log10(freq[:200]), phase)

    phase_fun = interp.interp1d(freq, phase, kind="quadratic")
    ugbw, valid = _get_best_crossing(freq, gain, val=1)
    if valid:
        if phase_fun(ugbw) > 0:
            return -180 + phase_fun(ugbw)
        else:
            return 180 + phase_fun(ugbw)
    else:
        return -180


def _get_best_crossing(xvec, yvec, val):
    interp_fun = interp.InterpolatedUnivariateSpline(xvec, yvec)

    def fzero(x):
        return interp_fun(x) - val

    xstart, xstop = xvec[0], xvec[-1]
    try:
        return sciopt.brentq(fzero, xstart, xstop), True
    except ValueError:
        # avoid no solution
        # if abs(fzero(xstart)) < abs(fzero(xstop)):
        #     return xstart
        return xstop, False
