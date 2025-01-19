import pyaudio



def select_microphone(index):
    p = pyaudio.PyAudio()
    device_info = p.get_device_info_by_index(index)
    if device_info.get('maxInputChannels') > 0:
        print(f"Selected Microphone: {device_info.get('name')}")
        return True
    else:
        print(f"No microphone at index {index}")
    return False



def print_microphones():
    p = pyaudio.PyAudio()
    for i in range (p.get_device_count()):
        device_info = p.get_device_info_by_index(i)
        if device_info['maxInputChannels'] != 0 and device_info['hostApi'] == 0:
            print('Device ' + str(i) + ': ' + device_info['name'])


def set_array_microphones():
    list_of_microphones = []
    p = pyaudio.PyAudio()
    for i in range (p.get_device_count()):
        device_info = p.get_device_info_by_index(i)
        if device_info['maxInputChannels'] != 0 and device_info['hostApi'] == 0:
            list_of_microphones.append(device_info['name'])
    return list_of_microphones


def return_id_microphone(mic):
    p = pyaudio.PyAudio()
    for i in range (p.get_device_count()):
        device_info = p.get_device_info_by_index(i)
        if device_info['maxInputChannels'] != 0 and device_info['hostApi'] == 0:
            if device_info['name'] == mic:
                return i
    return 0