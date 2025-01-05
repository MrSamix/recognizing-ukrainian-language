import pyaudio
import os
from dotenv import find_dotenv, set_key, load_dotenv
from create_env import creating_env

creating_env() # check if .env file exists, if not - create it

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
    # p.terminate()


def return_microphone(code):
   p = pyaudio.PyAudio()
   device_info = p.get_device_info_by_index(code)
   if device_info.get('maxInputChannels') > 0:
    return device_info.get('name')


load_dotenv(find_dotenv())
choice = os.getenv("LAST_MIC")
if choice is None or choice == "":
    print("Available microphones:")
    print_microphones()
    choice = input("Enter the index of the microphone you want to use: ")
else:
   choice2 = input(f"You used last microphone: {return_microphone(int(choice))}. Do you want to use this microphone or select another microphone?(y/n): ")
   if choice2 == "n":
      print("Available microphones:")
      print_microphones()
      choice = input("Enter the index of the microphone you want to use: ")

choice = int(choice)
if select_microphone(choice):
    print("Microphone selected successfully")
    set_key(find_dotenv(), "LAST_MIC", str(choice))
else:
    print("Failed to select microphone")