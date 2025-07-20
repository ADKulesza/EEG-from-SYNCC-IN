import glob
import json
import os

import matplotlib.pyplot as plt
import neurokit2 as nk
import numpy as np
import scipy.signal as ss
from constants import DIODE_CHANNEL, ECG_CHANNELS, EEG_CHANNELS
from read_raw_data import read_eeg
from save_data import save_signal


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


def find_diode_blinks(diode_sig, fs):
    reversed_diode_sig = -diode_sig + np.max(diode_sig)
    peaks, prop_dict = ss.find_peaks(
        reversed_diode_sig,
        height=55000,
        prominence=50000,
        width=(fs / 2 - 100, fs),
        distance=fs / 2 - 100,
    )

    peaks = np.array(peaks)
    if len(peaks) < 6:
        return -1
    # peaks = np.append(peaks, len(diode_sig))
    diff_between_peaks = np.diff(peaks)
    wh = np.where(diff_between_peaks > 3 * fs)[0]
    groups = {}
    groups[int(wh[0]) + 1] = peaks[: wh[0] + 1].tolist()
    groups[int(wh[1] - wh[0])] = peaks[wh[0] + 1 : wh[1] + 1].tolist()
    groups[len(peaks[wh[1] + 1 :])] = peaks[wh[1] + 1 :].tolist()

    return groups


def save_blinks_timestamps(blinks_range, output_path):
    filename = os.path.join(output_path, "diode_blinks.json")
    # print(filename)
    with open(filename, "w") as f:
        json.dump(blinks_range, f, indent=4)

    f.close()


def preprocess_diode_signal(data, channels, fs, output_path):
    diode_idx = channels.get_idx(DIODE_CHANNEL)

    diode_sig = data[diode_idx, :]

    blinks = find_diode_blinks(diode_sig, fs)
    blinks_range = {}
    if type(blinks) is dict:
        for k, v in blinks.items():
            blinks_range[k] = [int(v[0] - fs / 2), int(v[-1] + fs / 2)]

    else:
        for i in range(1, 4):
            blinks_range[i] = []
    # print(blinks_range)
    save_blinks_timestamps(blinks_range, output_path)


def preprocess_multiple_data(dir_name, output_dir):
    subdirectories = [
        f for f in glob.glob(os.path.join(dir_name, "*/")) if os.path.isdir(f)
    ]

    # blinks_df = pd.DataFrame(columns=['diade', '1start', '1end', '2start', '2end', '3start', '3end'])
    for subdir in subdirectories:
        data_paths = glob.glob(os.path.join(subdir, "*.obci.raw"))
        for data_path in data_paths:  # ?
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

            save_signal(eeg, os.path.join(output_path, "eeg_caregiver.npy"))

            eeg = preprocess_eeg(
                data,
                channels,
                fs_eeg,
                calibration_param,
                "child",
            )

            save_signal(eeg, os.path.join(output_path, "eeg_child.npy"))

            ecg, ecg_rate = preprocess_ecg(
                data,
                channels,
                fs_eeg,
                calibration_param,
                "caregiver",
            )

            save_signal(ecg, os.path.join(output_path, "ecg_caregiver.npy"))
            save_signal(ecg_rate, os.path.join(output_path, "ecg_rate_caregiver.npy"))

            ecg, ecg_rate = preprocess_ecg(
                data,
                channels,
                fs_eeg,
                calibration_param,
                "child",
            )

            save_signal(ecg, os.path.join(output_path, "ecg_child.npy"))
            save_signal(ecg_rate, os.path.join(output_path, "ecg_rate_child.npy"))

            # Diode
            preprocess_diode_signal(data, channels, fs_eeg, output_path)


path = "../../../Warsaw pilot"
out_path = "../../results/01_processed_eeg"
preprocess_multiple_data(path, out_path)
