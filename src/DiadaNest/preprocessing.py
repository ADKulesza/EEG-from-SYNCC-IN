import glob
import os

import matplotlib.pyplot as plt
import neurokit2 as nk
import numpy as np
from constants import ECG_CHANNELS, EEG_CHANNELS
from read_raw_data import read_eeg


def preprocess_eeg(data, channels, fs_eeg, calibration_param, to_process):
    channels_idx = channels.get_idx(EEG_CHANNELS[to_process])
    eeg = data[channels_idx,] * calibration_param
    eeg = nk.eeg_rereference(eeg, "average")
    eeg = nk.signal_filter(
        eeg,
        sampling_rate=fs_eeg,
        lowcut=1,
        method="butterworth",
        order=2,
    )
    eeg = nk.signal_filter(
        eeg,
        sampling_rate=fs_eeg,
        highcut=49,
        lowcut=51,
        method="butterworth_ba",
        order=2,
    )

    # plt.plot(eeg[:, :10*fs_eeg].T)
    # plt.title("Po filtrowaniu")
    # plt.show()
    return eeg


def preprocess_ecg(data, channels, fs, calib_param, to_process, plot=False):
    channels_idx = channels.get_idx(ECG_CHANNELS[to_process])

    ecg = data[channels_idx, :] * calib_param
    ecg = ecg[0, :] - ecg[1, :]

    ecg_clean, info_ecg = nk.ecg_process(ecg, sampling_rate=fs)
    # r_peaks = info_ecg["ECG_R_Peaks"]

    cleaned_ecg = ecg_clean["ECG_Clean"]
    ecg_rate = ecg_clean["ECG_Rate"]

    if plot:
        # nk.ecg_plot(ecg_clean, info_ecg)
        peaks, info = nk.ecg_peaks(
            cleaned_ecg,
            sampling_rate=fs,
            correct_artifacts=True,
        )

        # Compute HRV indices
        nk.hrv(peaks, sampling_rate=fs, show=True)
        plt.show()

        plt.plot(ecg_rate)
        plt.show()

    return cleaned_ecg, ecg_rate


def preprocess_multiple_data(dir_name, output_dir):
    subdirectories = [
        f for f in glob.glob(os.path.join(dir_name, "*/")) if os.path.isdir(f)
    ]

    for subdir in subdirectories:
        data_paths = glob.glob(os.path.join(subdir, "*.obci.raw"))
        for data_path in data_paths:
            filename = os.path.basename(data_path)
            diada = filename[:-4]
            output_path = os.path.join(
                output_dir,
                os.path.basename(os.path.normpath(subdir)),
            )
            if not os.path.exists(output_path):
                os.mkdir(output_path)

            (data, channels, fs_eeg, calibration_param) = read_eeg(diada, subdir)

            eeg = preprocess_eeg(
                data,
                channels,
                fs_eeg,
                calibration_param,
                "caregiver",
            )

            np.save(
                os.path.join(output_path, "eeg_caregiver.npy"),
                eeg,
            )

            eeg = preprocess_eeg(
                data,
                channels,
                fs_eeg,
                calibration_param,
                "child",
            )

            np.save(
                os.path.join(output_path, "eeg_child.npy"),
                eeg,
            )

            ecg, ecg_rate = preprocess_ecg(
                data,
                channels,
                fs_eeg,
                calibration_param,
                "caregiver",
            )

            np.save(
                os.path.join(output_path, "ecg_caregiver.npy"),
                ecg,
            )
            np.save(
                os.path.join(output_path, "ecg_rate_caregiver.npy"),
                ecg_rate,
            )

            ecg, ecg_rate = preprocess_ecg(
                data,
                channels,
                fs_eeg,
                calibration_param,
                "child",
            )

            np.save(
                os.path.join(output_path, "ecg_child.npy"),
                ecg,
            )
            np.save(
                os.path.join(output_path, "ecg_rate_child.npy"),
                ecg_rate,
            )


path = "../../../Warsaw pilot"
out_path = "../../results/01_processed_eeg"
preprocess_multiple_data(path, out_path)
