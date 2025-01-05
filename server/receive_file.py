import socket
# server returned id(hash) user and create folder
# id saves to finish program
# if id is not exist, server return error
# Program client closed, connection closed -> remove folder
# server return text
# client send name file to server or rename received file in server. 

# we can use dict to send a filename, id user
# def recv_file():
#     sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     host = socket.gethostname()
#     port = 1218
#     sock.connect((host, port))
#     sock.send(b"Hello Server!")
#     with open("ReceviedFile.wmv","wb") as file:
#         print("File opened")
#         print("Receiving data...")
#         while True:
#             data = sock.recv(1024)
#             if not data:
#                 break
#             file.write(data)
#     print("Successfully received the file")
#     sock.close()
#     print("Connection Closed")

# recv_file()



import socket
import os
import json
from threading import Thread
from queue import Queue
import shutil # for removing directory
from recognize import recognize_audio
from faster_whisper import WhisperModel


# port = 1218
# sock = socket.socket()
# host = socket.gethostname()
# sock.bind((host, port))
# sock.listen(10)
# print("File Server started....")

# if os.path.exists("records"):
#     shutil.rmtree("records")
# os.makedirs("records", exist_ok=True)


# print("Initializing model...")
# files_queue = Queue()
# # model = WhisperModel("turbo", device="cpu", compute_type="int8")
# model = WhisperModel("large-v3", device="cuda", compute_type="int8")
# print("Model initialized")
print("Starting receive_file.py")
def handle_client(conn=None, addr=None, files_queue=None):
    print(f"Accepted connection from {addr}")

    # Получение метаданных от клиента
    metadata = json.loads(conn.recv(1024).decode())
    filename = metadata["filename"]
    client_uuid = metadata["uuid"]
    language = metadata["language"]
    print(f"Received metadata: {metadata}")

    # Створення папки для клієнта
    client_folder = os.path.join("records", client_uuid)
    os.makedirs(client_folder, exist_ok=True)

    # Получение файла от клиента
    filepath = os.path.join(client_folder, filename)
    with open(filepath, "wb") as file:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            file.write(data)
    print(f"Received file {filename} from client")

    # Добавление файла в очередь на обработку
    files_queue.put((filepath, conn, client_uuid, language))

def process_files(files_queue=None, model=None):
    while True:
        item = files_queue.get()
        if item is None:
            break
        filepath, conn, client_uuid, language = item
        try:
            # recognize_audio([filepath], model, language)
            # Обработка файла (например, конвертация аудио в текст)
            processed_text = recognize_audio(filepath, model, language)
            # Отправка обработанного текста обратно клиенту
            conn.send(processed_text.encode())
            print(f"Sent processed text to client {client_uuid}")
        except Exception as e:
            print(f"Failed to process {filepath}: {e}")
        os.remove(filepath)
        files_queue.task_done()
        conn.close()

# Запуск нескольких потоков для обработки файлов
# num_worker_threads = 3
# threads = []
# for _ in range(num_worker_threads):
#     thread = Thread(target=process_files)
#     thread.start()
#     threads.append(thread)

# try:
#     while True:
#         conn, addr = sock.accept()
#         client_thread = Thread(target=handle_client, args=(conn, addr))
#         client_thread.start()
# finally:
#     # Остановка потоков обработки файлов
#     for _ in range(num_worker_threads):
#         files_queue.put(None)
#     for thread in threads:
#         thread.join()

# sock.close()