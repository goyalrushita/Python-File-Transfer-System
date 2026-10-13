import socket
import os

HOST = "0.0.0.0"
PORT = 5000

# Basic authentication
USERNAME = "admin"
PASSWORD = "1234"

# Folder where server stores files
SERVER_FOLDER = "server_files"

if not os.path.exists(SERVER_FOLDER):
    os.makedirs(SERVER_FOLDER)


def send_message(conn, message):
    conn.send(message.encode())


def receive_message(conn):
    return conn.recv(1024).decode()


def receive_file(conn, filename):
    filepath = os.path.join(SERVER_FOLDER, os.path.basename(filename))

    with open(filepath, "wb") as file:
        while True:
            data = conn.recv(4096)

            if data == b"EOF":
                break

            file.write(data)

    print("File received:", filename)


def send_file(conn, filename):
    filepath = os.path.join(SERVER_FOLDER, os.path.basename(filename))

    if not os.path.exists(filepath):
        send_message(conn, "FILE_NOT_FOUND")
        return

    send_message(conn, "FILE_FOUND")

    # Wait for client confirmation
    conn.recv(1024)

    with open(filepath, "rb") as file:
        while True:
            data = file.read(4096)

            if not data:
                break

            conn.send(data)

    conn.send(b"EOF")

    print("File sent:", filename)


# Create TCP socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind server to IP and port
server.bind((HOST, PORT))

# Listen for clients
server.listen(5)

print("=================================")
print("     FILE TRANSFER SERVER")
print("=================================")
print("Server started...")
print("Waiting for client...")
print("Port:", PORT)

while True:

    conn, address = server.accept()

    print("\nClient connected:", address)

    # Authentication
    send_message(conn, "USERNAME")

    username = receive_message(conn)

    send_message(conn, "PASSWORD")

    password = receive_message(conn)

    if username == USERNAME and password == PASSWORD:
        send_message(conn, "LOGIN_SUCCESS")

        print("Login successful:", username)

    else:
        send_message(conn, "LOGIN_FAILED")

        print("Login failed")

        conn.close()
        continue

    # Client menu
    while True:

        choice = receive_message(conn)

        if choice == "1":

            # Upload
            filename = receive_message(conn)

            send_message(conn, "READY")

            receive_file(conn, filename)

            send_message(conn, "UPLOAD_SUCCESS")

        elif choice == "2":

            # Download
            filename = receive_message(conn)

            send_file(conn, filename)

        elif choice == "3":

            print("Client disconnected.")
            break

        else:
            send_message(conn, "INVALID")

    conn.close()