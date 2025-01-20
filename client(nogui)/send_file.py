import socket
import json
import keyboard as kb


def write_text(text): # написання тексту в спец. полі
    kb.write(text, delay=0.1)

def sending_file(filename, host, port, client_uuid, language=None, YourArea=False):
    # Підключення до сервера
    sock = socket.socket()
    try:
        sock.connect((host, port))
    except socket.error as e:
        raise Exception(f"Could not connect to server: {e}")


    # Відправка метаданих (UUID, назва файлу та мови розпізнавання) на сервер
    metadata = {
        "uuid": client_uuid,
        "filename": filename,
        "language": language
    }
    sock.send(json.dumps(metadata).encode())

    # Відправка файлу на сервер
    with open(f"records/{filename}", "rb") as file:
        while True:
            data = file.read(1024)
            if not data:
                break
            sock.send(data)
    # print(f"Sent file {filename} to server") # for debug

    # Закриття відправлення файлу
    sock.shutdown(socket.SHUT_WR)

    # Отримання тексту від сервера
    processed_text = sock.recv(1024).decode()
    if not processed_text == "" or processed_text is None:
        if YourArea:
            write_text(processed_text)
        else:
            print(processed_text)
    #print(f"Received processed text from server: {processed_text}") # for debug

    sock.close()


