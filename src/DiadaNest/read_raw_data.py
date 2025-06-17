# Standard library imports
import os
from enum import Enum, EnumMeta

# Third-party imports
import numpy as np  # type: ignore
import xmltodict  # type: ignore


class ListableEnumMeta(EnumMeta):
    def __getitem__(cls, key):
        if isinstance(key, list):
            return [cls[k] for k in key]
        return super().__getitem__(key)


class ChannelEnum(Enum, metaclass=ListableEnumMeta):
    def __new__(cls, idx):
        obj = object.__new__(cls)
        obj._value_ = idx  # still sets .value
        obj.idx = idx  # custom attribute
        return obj

    @classmethod
    def get_idx(cls, channels):
        if isinstance(channels, list):
            return [cls[name].value for name in channels]
        return cls[channels].value


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
    calibration_param = float(
        xml["rs:rawSignal"]["rs:calibrationGain"]["rs:calibrationParam"][0]
    )

    data_path = os.path.join(dir_path, f"{fname}.raw")

    data = np.fromfile(data_path, dtype="float32")
    data = data.reshape((-1, n_ch))
    data = data.T

    return data, channels, fs_eeg, calibration_param
