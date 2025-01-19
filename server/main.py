import socket
from dotenv import find_dotenv, load_dotenv, set_key
import shutil
from queue import Queue
from faster_whisper import WhisperModel
from receive_file import handle_client, process_files
from threading import Thread
import os
from create_env import creating_env

load_dotenv(find_dotenv())

creating_env()


IP = os.getenv('IP')
PORT = os.getenv('PORT')
if IP is None or IP == "" or PORT is None or PORT == "":
    choice = input("IP or PORT is not set. Do you want to set it now?(y/n): ")
    match choice:
        case 'y':
            choice2 = input("Do you want to use local ip your computer?(y/n): ")
            match choice2:
                case 'y':
                    IP = socket.gethostname()
                case 'n':
                    IP = input("Enter IP: ")
            PORT = input("Enter PORT: ")
            set_key(find_dotenv(), 'IP', IP)
            set_key(find_dotenv(), 'PORT', PORT)
        case 'n':
            print("Please set IP and PORT in .env file")
            print("Exiting...")
            exit()
print(f"Server starting on IP: {IP}, PORT: {PORT}")
DEVICE = os.getenv('DEVICE')
if DEVICE is None or DEVICE == "":
    choice = input("Do you want to use CPU or CUDA?(cpu/cuda): ")
    match choice:
        case 'cpu':
            DEVICE = 'cpu'
            set_key(find_dotenv(), 'DEVICE', DEVICE)
        case 'cuda':
            DEVICE = 'cuda'
            set_key(find_dotenv(), 'DEVICE', DEVICE)


# Start listening
sock = socket.socket()
sock.bind((IP, int(PORT)))
sock.listen(10)

if os.path.exists("records"):
    shutil.rmtree("records")
os.makedirs("records", exist_ok=True)


print("Initializing model...")
files_queue = Queue()
model = WhisperModel("turbo", device=DEVICE, compute_type="int8")
print("Model initialized")
print("Server started!")
print("Press 'Ctrl+Pause' or 'Ctrl+Break' to stop the server")

num_worker_threads = 3
threads = []
for _ in range(num_worker_threads):
    thread = Thread(target=process_files, args=(files_queue, model))
    thread.start()
    threads.append(thread)

try:
    while True:
        conn, addr = sock.accept()
        client_thread = Thread(target=handle_client, args=(conn, addr, files_queue))
        client_thread.start()
finally:
    # Зупинка потоків обробки файлів
    print("Stopping server...")
    for _ in range(num_worker_threads):
        files_queue.put(None)
    for thread in threads:
        thread.join()
    print("Server stopped")