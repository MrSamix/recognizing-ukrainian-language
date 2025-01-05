# def sendfile(filename = "tmp_audio.wav", testing = False):
#     import socket
#     #port = 12345
#     port = 1218
#     sock = socket.socket()
#     host = socket.gethostname()
#     sock.bind((host,port))
#     sock.listen(5)
#     print("Server started and listening....")

#     while True:
#         conn, addr = sock.accept()
#         print(f"Got connection from {addr}")
#         data = conn.recv(1024)
#         print(f"Server recieved: {data}")
#         with open(filename, "rb") as file:
#             data = file.read(1024)
#             while data:
#                 conn.send(data)
#                 print(f"sent {data!r}")
#                 data = file.read(1024)
#         print("Done sending")
#         conn.close()
#     sock.shutdown(1)
#     sock.close()

# sendfile("old_records/record.wav", testing=True)



# import socket
# ONE_CONNECTION_ONLY =(True)
# filename = "file.txt"
# port =1218
# sock = socket.socket()
# host = socket.gethostname()
# sock.bind((host,port))
# sock.listen(10)
# print("File Server started....")
# while True:
#     conn, addr = sock.accept()
#     print(f"Accepted connection from {addr}")
#     data = conn.recv(1024)
#     print(f"Server received {data}")
#     with open (filename,"rb") as file:
#         data = file.read(1024)
#         while data:
#             conn.send(data)
#             print(f"Sent {data!r}")
#             data = file.read(1024)
#     print("File sent complete.")
#     conn.close()
#     if(ONE_CONNECTION_ONLY):
#         break
# sock.shutdown(1)
# sock.close()


import socket
import os
import json


def sending_file(filename, host, port, client_uuid, language=None):
    # filename = "record.wav"
    # port = 1218
    sock = socket.socket()
    # host = socket.gethostname()
    try:
        sock.connect((host, port))
    except socket.error as e:
        raise Exception(f"Could not connect to server: {e}")
    # sock.connect((host, port))

    # Отримання UUID від сервера
    # client_uuid = sock.recv(1024).decode()
    # print(f"Received UUID {client_uuid} from server")


    # Отправка метаданных (UUID и название файла) на сервер
    metadata = {
        "uuid": client_uuid,
        "filename": filename,
        "language": language
    }
    sock.send(json.dumps(metadata).encode())

    # Відправка файлу на сервер
    with open(filename, "rb") as file:
        while True:
            data = file.read(1024)
            if not data:
                break
            sock.send(data)
    print(f"Sent file {filename} to server")

    # Закрытие отправки данных
    sock.shutdown(socket.SHUT_WR)

    # Отримання обробленого тексту від сервера
    processed_text = sock.recv(1024).decode()
    print(f"Received processed text from server: {processed_text}")

    sock.close()