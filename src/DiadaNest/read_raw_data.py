# Standard library imports
import glob
import os
from enum import Enum

# Third-party imports
import numpy as np  # type: ignore
import xmltodict  # type: ignore
from preprocessing import preprocess_data


class ChannelEnum(Enum):
    def __new__(cls, idx):
        obj = object.__new__(cls)
        obj._value_ = idx  # still sets .value
        obj.idx = idx  # custom attribute
        return obj


def channels_from_xml(xml, enum_name):
    ch_names = xml["rs:rawSignal"]["rs:channelLabels"]["rs:label"]
    mapping = {name: idx for idx, name in enumerate(ch_names)}
    return ChannelEnum(enum_name, mapping)


def read_eeg(fname, dir_path):
    with open(os.path.join(dir_path, f"{fname}.xml")) as fd:
        xml = xmltodict.parse(fd.read())

    channels = channels_from_xml(xml, "Channel")
    n_ch = int(xml["rs:rawSignal"]["rs:channelCount"])
    fs_eeg = int(float(xml["rs:rawSignal"]["rs:samplingFrequency"]))

    data_path = os.path.join(dir_path, f"{fname}.raw")
    data = np.fromfile(data_path, dtype="float32").reshape((-1, n_ch))

    return data, channels, fs_eeg


def load_multiple_data(dir_name):
    subdirectories = [
        f for f in glob.glob(os.path.join(dir_name, "*/")) if os.path.isdir(f)
    ]

    for subdir in subdirectories:
        data_paths = glob.glob(os.path.join(subdir, "*.obci.raw"))
        for data_path in data_paths:
            filename = os.path.basename(data_path)
            diada = filename[:-4]
            data, channels, fs_eeg = read_eeg(diada, subdir)

            preprocess_data(data)


path = "../../Warsaw pilot"
load_multiple_data(path)
