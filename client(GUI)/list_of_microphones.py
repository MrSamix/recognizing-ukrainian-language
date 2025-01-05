import pyaudio



def select_microphone(index):
   p = pyaudio.PyAudio()
   device_info = p.get_device_info_by_index(index)
   if device_info.get('maxInputChannels') > 0:
      print(f"Selected Microphone: {device_info.get('name')}")
    #   p.terminate()
      return True
   else:
      print(f"No microphone at index {index}")
#    p.terminate()
   return False



def print_microphones():
    p = pyaudio.PyAudio()
    for i in range (p.get_device_count()):
        device_info = p.get_device_info_by_index(i)
        if device_info['maxInputChannels'] != 0 and device_info['hostApi'] == 0:
            print('Device ' + str(i) + ': ' + device_info['name'])
    # p.terminate()


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

# print("Available microphones:")
# print_microphones()
# choice = int(input("Enter the index of the microphone you want to use: "))
# if select_microphone(choice):
#     print("Microphone selected successfully")
# else:
#     print("Failed to select microphone")