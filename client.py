import socket
import os

SERVER_IP = "127.0.0.1"
PORT = 5000

# Folder containing files on client side
CLIENT_FOLDER = "client_files"

if not os.path.exists(CLIENT_FOLDER):
    os.makedirs(CLIENT_FOLDER)


def send_message(sock, message):
    sock.send(message.encode())


def receive_message(sock):
    return sock.recv(1024).decode()


# Create TCP socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to server
client.connect((SERVER_IP, PORT))

print("=================================")
print("     FILE TRANSFER CLIENT")
print("=================================")

# Authentication

message = receive_message(client)

if message == "USERNAME":

    username = input("Enter username: ")
    send_message(client, username)


message = receive_message(client)

if message == "PASSWORD":

    password = input("Enter password: ")
    send_message(client, password)


# Check login
result = receive_message(client)

if result == "LOGIN_SUCCESS":

    print("\nLogin successful!")

else:

    print("\nInvalid username or password.")
    client.close()
    exit()


# Main menu

while True:

    print("\n========== MENU ==========")
    print("1. Upload File")
    print("2. Download File")
    print("3. Exit")
    print("==========================")

    choice = input("Enter your choice: ")

    send_message(client, choice)

    # Upload
    if choice == "1":

        filename = input("Enter filename to upload: ")

        filepath = os.path.join(CLIENT_FOLDER, filename)

        if not os.path.exists(filepath):

            print("File does not exist in client_files folder.")
            continue

        send_message(client, filename)

        response = receive_message(client)

        if response == "READY":

            with open(filepath, "rb") as file:

                while True:

                    data = file.read(4096)

                    if not data:
                        break

                    client.send(data)

            client.send(b"EOF")

            result = receive_message(client)

            if result == "UPLOAD_SUCCESS":
                print("File uploaded successfully!")


    # Download
    elif choice == "2":

        filename = input("Enter filename to download: ")

        send_message(client, filename)

        response = receive_message(client)

        if response == "FILE_NOT_FOUND":

            print("File not found on server.")

        elif response == "FILE_FOUND":

            # Tell server we are ready
            send_message(client, "READY")

            filepath = os.path.join(CLIENT_FOLDER, filename)

            with open(filepath, "wb") as file:

                while True:

                    data = client.recv(4096)

                    if data == b"EOF":
                        break

                    file.write(data)

            print("File downloaded successfully!")


    # Exit
    elif choice == "3":

        print("Disconnected from server.")
        break

    else:

        print("Invalid choice.")


client.close()