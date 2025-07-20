import numpy as np


def save_signal(output_sig, output_path):
    np.save(
        output_path,
        output_sig,
    )
