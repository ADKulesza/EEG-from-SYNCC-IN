# Standard library imports
import os

import matplotlib.pylab as plt  # type: ignore
import neurokit2 as nk  # type: ignore
# Third-party imports
import numpy as np  # type: ignore
import pandas as pd  # type: ignore
import scipy.signal as signal  # type: ignore
import xmltodict  # type: ignore
from scipy.interpolate import CubicSpline  # type: ignore
from scipy.stats import zscore  # type: ignore


# Local application/library imports
# from mtmvar import mvar_criterion, AR_coeff, mvar_H, mvar_plot  # type: ignore


def read_ecg_data(file, folder, T_EEG=None, plot=False):
    """
    Reads ECG data from the specified file and extracts child and caregiver ECG signals.

    Args:
        file (str): File name without extension.
        folder (str): Folder path containing the file.
        T_EEG (int, optional): Duration of EEG data to extract. Defaults to None.
        plot (bool, optional): Whether to plot the signals. Defaults to False.

    Returns:
        tuple: Child ECG, Caregiver ECG, and sampling frequency.
    """
    with open(os.path.join(folder, f"{file}.xml")) as fd:
        xml = xmltodict.parse(fd.read())

    N_ch = int(xml["rs:rawSignal"]["rs:channelCount"])
    Fs_EEG = int(float(xml["rs:rawSignal"]["rs:samplingFrequency"]))
    ChanNames = xml["rs:rawSignal"]["rs:channelLabels"]["rs:label"]

    data = np.fromfile(os.path.join(folder, f"{file}.raw"), dtype="float32").reshape(
        (-1, N_ch)
    )
    wyc_T = np.arange(0, Fs_EEG * T_EEG, 1) if T_EEG else np.arange(0, data.shape[0], 1)
    data = data[wyc_T, :]

    ECG_CH = data[:, ChanNames.index("EKG1")] - data[:, ChanNames.index("EKG2")]
    ECG_CG = data[:, ChanNames.index("EKG1_cg")] - data[:, ChanNames.index("EKG2_cg")]

    if plot:
        fig, ax = plt.subplots(2, 1, sharex=True, sharey=True)
        ax[0].plot(ECG_CH, label="Child ECG")
        ax[1].plot(ECG_CG, label="Caregiver ECG")
        plt.legend()
        plt.show()

    return ECG_CH, ECG_CG, Fs_EEG


def read_eeg_data(file, folder, T_EEG=None, plot=False):
    """ """

    CHANNELS = [
        "Fp1",
        "Fp2",
        "F7",
        "F3",
        "Fz",
        "F4",
        "F8",
        "M1",
        "T3",
        "C3",
        "Cz",
        "C4",
        "T4",
        "M2",
        "T5",
        "P3",
        "Pz",
        "P4",
        "T6",
        "O1",
        "O2",
    ]

    with open(os.path.join(folder, f"{file}.xml")) as fd:
        xml = xmltodict.parse(fd.read())

    N_ch = int(xml["rs:rawSignal"]["rs:channelCount"])
    Fs_EEG = int(float(xml["rs:rawSignal"]["rs:samplingFrequency"]))
    ChanNames = xml["rs:rawSignal"]["rs:channelLabels"]["rs:label"]

    data = np.fromfile(os.path.join(folder, f"{file}.raw"), dtype="float32").reshape(
        (-1, N_ch)
    )
    wyc_T = np.arange(0, Fs_EEG * T_EEG, 1) if T_EEG else np.arange(0, data.shape[0], 1)
    data = data[wyc_T, :]

    EEG_data = np.zeros((data.shape[0], len(CHANNELS)))
    for i, ch in enumerate(CHANNELS):
        EEG_data[:, i] = data[:, ChanNames.index(ch)]

    if plot:
        fig, ax = plt.subplots(1, 1, sharex=True, sharey=True)
        ax.plot(EEG_data[:, 0], label="Child ECG")
        plt.legend()
        plt.show()


# docelowy sposób nazywania plików:
# rok_miesiąc_dzien_typdanych_godzina_minuta_diada

folder = "../../Warsaw pilot/03_17/"
date = "2025_03_17_17_59"
diada = "gabrys"
file = "gabrysiasia.obci"

read_eeg_data(file, folder)
