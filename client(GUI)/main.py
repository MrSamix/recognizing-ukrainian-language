from queue import Queue
from dotenv import load_dotenv, find_dotenv, set_key
from record import record_audio
from list_of_microphones import return_id_microphone
import os
import shutil
import send_file as sf
from tkinter import messagebox
from threading import Thread
from list_of_languages import get_code_by_native_name
import keyboard as kb
import uuid

import callback_handler

recording = False

load_dotenv(find_dotenv())

UUID = os.getenv('UUID')
if UUID is None or UUID == "":
    UUID = str(uuid.uuid4())
    set_key(find_dotenv(), "UUID", UUID)

SERVER_IP = os.getenv('SERVER_IP')
SERVER_PORT = os.getenv('SERVER_PORT')
language = os.getenv('LAST_LANGUAGE')

if language == "Auto":
    language = None
else:
    language = get_code_by_native_name(language)

mic = os.getenv('LAST_MIC')
mic = return_id_microphone(mic)

def initilizing(): # if user edit .env file, this function will update variables
    global language, mic, SERVER_IP, SERVER_PORT
    import screens.settings as settings
    
    language = settings.language
    if language == "Auto":
        language = None
    else:
        language = get_code_by_native_name(language)
    mic = return_id_microphone(settings.mic)
    SERVER_IP = settings.server_ip
    SERVER_PORT = settings.server_port


files_queue = Queue()
counter = 0

def starts_recording():
    global files_queue
    files_queue = Queue()
    if os.path.exists("records"):
        shutil.rmtree("records")
    os.mkdir("records")
    global recording
    recording = True

def stops_recording():
    global recording
    recording = False


def record():
    global recording
    global counter
    global mic
    while recording:
        try:
            record_audio(int(mic), f"records/record_{counter}.wav")
            files_queue.put(f"record_{counter}.wav")
            counter += 1
        except:
            stops_recording()
            messagebox.showerror("Error","Помилка запису, запис зупинено!")
            if not callback_handler.is_error_handling():
                callback_handler.set_error_handling(True)
                error_callback = callback_handler.get_error_callback()
                if error_callback:
                    error_callback()
        if not recording:
            shutil.rmtree("records")



def start_threads():
    thread_record = Thread(target=record)
    thread_send = Thread(target=sending_file)
    thread_record.start()
    thread_send.start()
    return thread_record, thread_send

def stop_threads():
    stops_recording()
    files_queue.put(None)


def write_text(text):
    kb.write(text, delay=0.1)


def sending_file():
    while True:
        filename = files_queue.get()
        if filename is None:
            break
        try:
            text = sf.sending_file(filename=filename, host=SERVER_IP, port=int(SERVER_PORT), client_uuid=UUID, language=language)
            kb.write(text=text)
        except Exception as e:
            messagebox.showerror("Error", "Помилка з відправкою файлу на сервер. Будь ласка перевірте інтернет підключення або статус серверу! Розпізнавання зупинено!")
            stop_threads()
            if not callback_handler.is_error_handling():
                callback_handler.set_error_handling(True)
                error_callback = callback_handler.get_error_callback()
                if error_callback:
                    error_callback()
        if os.path.exists("records"):
            os.remove(f"records/{filename}")
        files_queue.task_done()