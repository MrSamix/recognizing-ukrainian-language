from faster_whisper import WhisperModel
from record import record_audio
from threading import Thread
from queue import Queue
from dotenv import load_dotenv, find_dotenv, set_key
import os
import send_file as sf
import keyboard
import uuid
import socket

load_dotenv(find_dotenv())
SERVER_IP = os.getenv('SERVER_IP')
SERVER_PORT = os.getenv('SERVER_PORT')

UUID = os.getenv('UUID')

if UUID is None:
    UUID = str(uuid.uuid4())
    set_key(find_dotenv(), 'UUID', UUID)

if SERVER_IP is None or SERVER_PORT is None:
    choice = input("SERVER_IP or SERVER_PORT is not set. Do you want to set it now?(y/n): ")
    if choice == 'y':
        choice2 = input("Use local ip your computer?(y/n): ")
        if choice2 == 'y':
            SERVER_IP = socket.gethostname() # localhost???
        else:
            SERVER_IP = input("Enter SERVER_IP: ")
        SERVER_PORT = input("Enter SERVER_PORT: ")
        set_key(find_dotenv(), 'SERVER_IP', SERVER_IP)
        set_key(find_dotenv(), 'SERVER_PORT', SERVER_PORT)
    else:
        print("Please set SERVER_IP and SERVER_PORT in .env file")
        print("Exiting...")
        exit()


model = WhisperModel("turbo", device="cpu", compute_type="int8")
# Set a language
print("Available languages:")
print(model.supported_languages)
language = ""
last_language = os.getenv('LAST_LANGUAGE')
if last_language is None:
    last_language = input("Set a language(or input auto): ") # for server
    set_key(find_dotenv(), 'LAST_LANGUAGE', last_language)
else:
    choice = input(f"Do you want to use last language ({last_language})?(y/n): ")
    if choice == 'n':
        language = input("Set a language(or input auto): ")
        set_key(find_dotenv(), 'LAST_LANGUAGE', language)
if language == "auto" or last_language == "auto": # не передавати на сервер тоді
    language = None
print("Press 'esc' to stop recording")
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
            print(f"Failed to send {filename}: {e}")
        files_queue.task_done()


# Запуск нескольких потоков для отправки файлов
num_worker_threads = 3
threads = []
for _ in range(num_worker_threads):
    thread = Thread(target=sending_file)
    thread.start()
    threads.append(thread)

try:
    while not keyboard.is_pressed('esc'):
        filename = f"record_{counter}.wav"
        record_audio(filename)
        files_queue.put(filename)
        counter += 1
finally:
    for _ in range(num_worker_threads):
        files_queue.put(None)
    for thread in threads:
        thread.join()