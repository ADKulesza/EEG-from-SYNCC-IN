import glob
import os

import neurokit2 as nk
import numpy as np


def get_gfp(dir_name):
    subdirectories = [
        f for f in glob.glob(os.path.join(dir_name, "*/")) if os.path.isdir(f)
    ]

    for subdir in subdirectories:
        data_paths = glob.glob(os.path.join(subdir, "eeg_*.npy"))
        for eeg_path in data_paths:
            eeg = np.load(eeg_path)

            # eeg = eeg.reshape((eeg.shape[1], -1,))
            # print("po", eeg.shape)
            gfp = nk.eeg_gfp(eeg)
            # gfp = np.std(eeg, axis=1)
            # print(gfp.shape)

            filename = os.path.basename(data_path)
            out_filename = "gfp" + filename[3:]
            out_path = os.path.join(subdir, out_filename)
            np.save(out_path, gfp)


data_path = "../../results/01_processed_eeg"
get_gfp(data_path)
