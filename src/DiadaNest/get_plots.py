import glob
import os

import matplotlib.pyplot as plt
import neurokit2 as nk
import numpy as np


def gfp_hr_plot(dir_name):
    subdirectories = [
        f for f in glob.glob(os.path.join(dir_name, "*/")) if os.path.isdir(f)
    ]

    for subdir in subdirectories:
        cg_gfp_path = os.path.join(subdir, "gfp_caregiver.npy")
        cg_gfp = np.load(cg_gfp_path)
        child_gfp_path = os.path.join(subdir, "gfp_child.npy")
        child_gfp = np.load(child_gfp_path)

        cg_hr_path = os.path.join(subdir, "ecg_rate_caregiver.npy")
        cg_hr = np.load(cg_hr_path)
        child_hr_path = os.path.join(subdir, "ecg_rate_child.npy")
        child_hr = np.load(child_hr_path)

        print("caregiver", cg_gfp.shape, cg_hr.shape)

        nk.signal_plot([cg_gfp, cg_hr])

        plt.title("Caregiver")
        plt.show()

        print("child", child_gfp.shape, child_hr.shape)
        nk.signal_plot([child_gfp[1000:2000], child_hr[1000:2000]])
        plt.title("Child")
        plt.show()


data_path = "../../results/01_processed_eeg"
gfp_hr_plot(data_path)
