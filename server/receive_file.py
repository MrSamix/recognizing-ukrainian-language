import os
import json
from recognize import recognize_audio
print("Starting receive_file.py")
def handle_client(conn=None, addr=None, files_queue=None):
    print(f"Accepted connection from {addr}")

    # Отримання метаданих від клієнта
    metadata = json.loads(conn.recv(1024).decode())
    filename = metadata["filename"]
    client_uuid = metadata["uuid"]
    language = metadata["language"]
    print(f"Received metadata: {metadata}")

    # Створення папки для клієнта
    client_folder = os.path.join("records", client_uuid)
    os.makedirs(client_folder, exist_ok=True)

    # Отримання файлу від клієнта
    filepath = os.path.join(client_folder, filename)
    with open(filepath, "wb") as file:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            file.write(data)
    print(f"Received file {filename} from client")

    # Додавання файлу в чергу для обробки
    files_queue.put((filepath, conn, client_uuid, language))

def process_files(files_queue=None, model=None):
    while True:
        item = files_queue.get()
        if item is None:
            break
        filepath, conn, client_uuid, language = item
        try:
            processed_text = recognize_audio(filepath, model, language)
            # Відправка обробленого тексту клієнту
            conn.send(processed_text.encode())
            print(f"Sent processed text to client {client_uuid}")
        except Exception as e:
            print(f"Failed to process {filepath}: {e}")
        os.remove(filepath)
        files_queue.task_done()
        conn.close()