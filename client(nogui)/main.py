import signal
import sys
import shutil
from record import record_audio
from threading import Thread
from queue import Queue
from dotenv import load_dotenv, find_dotenv, set_key
import os
import send_file as sf
import uuid
import socket
from list_of_languages import list_of_avaibable_languages_codes, get_native_name


def signal_handler(sig, frame):
    print('You pressed Ctrl+C! Exiting...')
    for _ in range(num_worker_threads):
        files_queue.put(None)
    for thread in threads:
        thread.join()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

load_dotenv(find_dotenv())
SERVER_IP = os.getenv('SERVER_IP')
SERVER_PORT = os.getenv('SERVER_PORT')

UUID = os.getenv('UUID')

if UUID is None or UUID == "":
    UUID = str(uuid.uuid4())
    set_key(find_dotenv(), 'UUID', UUID)

if SERVER_IP is None or SERVER_IP == "" or SERVER_PORT is None or SERVER_PORT == "":
    choice = input("SERVER_IP or SERVER_PORT is not set. Do you want to set it now?(y/n): ")
    if choice == 'y':
        choice2 = input("Use local ip your computer?(y/n): ")
        if choice2 == 'y':
            SERVER_IP = socket.gethostname()
        else:
            SERVER_IP = input("Enter SERVER_IP: ")
        SERVER_PORT = input("Enter SERVER_PORT: ")
        set_key(find_dotenv(), 'SERVER_IP', SERVER_IP)
        set_key(find_dotenv(), 'SERVER_PORT', SERVER_PORT)
    else:
        print("Please set SERVER_IP and SERVER_PORT in .env file")
        print("Exiting...")
        exit()

# check folder
if os.path.exists("records"):
    shutil.rmtree("records")
os.mkdir("records")


language = ""
last_language = os.getenv('LAST_LANGUAGE')
if last_language is None or last_language == "":
    print("Available languages:")
    print("Format: Code language - Native")
    for lang in list_of_avaibable_languages_codes:
        print(f"{lang} - {get_native_name(lang)}")  
    last_language = input("Set a language code(or input auto): ")
    set_key(find_dotenv(), 'LAST_LANGUAGE', last_language)
else:
    choice = input(f"Do you want to use last language ({last_language})?(y/n): ")
    if choice == 'n':
        print("Available languages:")
        print("Format: Code language - Native")
        for lang in list_of_avaibable_languages_codes:
            print(f"{lang} - {get_native_name(lang)}")
        language = input("Set a language code(or input auto): ")
        set_key(find_dotenv(), 'LAST_LANGUAGE', language)
if language == "auto" or last_language == "auto":
    language = None
else:
    language = last_language
print("Press 'Ctrl + C' to stop program")
files_queue = Queue()
counter = 0



def sending_file():
    while True:
        filename = files_queue.get()
        if filename is None:
            break
        try:
            sf.sending_file(filename=filename, host=SERVER_IP, port=int(SERVER_PORT), client_uuid=UUID, language=language)
        except Exception as e:
            print(f"Failed to send {filename} to server: {e}")
        files_queue.task_done()


# Запуск декількох потоків для відправки файлів
num_worker_threads = 3
threads = []
for _ in range(num_worker_threads):
    thread = Thread(target=sending_file)
    thread.start()
    threads.append(thread)

try:
    while True:
        filename = f"record_{counter}.wav"
        record_audio(f"records/{filename}")
        files_queue.put(filename)
        counter += 1
except Exception as _:
    print(f"Error recording file {filename}!")
finally:
    for _ in range(num_worker_threads):
        files_queue.put(None)
    for thread in threads:
        thread.join()
    if os.path.exists("records"):
        shutil.rmtree("records")