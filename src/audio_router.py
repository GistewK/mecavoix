import sounddevice as sd
def find_vb_cable_id():
    devices = sd.query_devices()
    for index, dev in enumerate(devices):
        name = dev['name'].lower()
        outputs = dev['max_output_channels']
        if "cable input" in name and outputs > 0:
            return index
    return None
def find_mic_id(keyword="microphone"):
    devices = sd.query_devices()
    for index, dev in enumerate(devices):
        name = dev['name'].lower()
        inputs = dev['max_input_channels']
        if keyword.lower() in name and inputs > 0 and "cable" not in name:
            return index
    return None
if __name__ == "__main__":
    vb_id = find_vb_cable_id()
    mic_id = find_mic_id()
    print(f"Found VB-Cable Input ID: {vb_id}")
    print(f"Found Physical Mic ID: {mic_id}")
