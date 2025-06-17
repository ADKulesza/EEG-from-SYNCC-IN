CHILD_EEG_CHANNELS = [
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
]

CAREGIVER_EEG_CHANNELS = [
    "Fp1_cg",
    "Fp2_cg",
    "F7_cg",
    "F3_cg",
    "Fz_cg",
    "F4_cg",
    "F8_cg",
    "M1_cg",
    "T3_cg",
    "C3_cg",
    "Cz_cg",
    "C4_cg",
    "T4_cg",
    "M2_cg",
    "T5_cg",
    "P3_cg",
    "Pz_cg",
    "P4_cg",
    "T6_cg",
]

EEG_CHANNELS = {
    "caregiver": CAREGIVER_EEG_CHANNELS,
    "child": CHILD_EEG_CHANNELS,
}

CHILD_ECG_CHANNELS = ["EKG1", "EKG2"]
CAREGIVER_ECG_CHANNELS = ["EKG1_cg", "EKG2_cg"]

ECG_CHANNELS = {
    "caregiver": CAREGIVER_ECG_CHANNELS,
    "child": CHILD_ECG_CHANNELS,
}
