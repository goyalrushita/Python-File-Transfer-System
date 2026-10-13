# Python-Based Client-Server File Transfer System

## Overview
A Python-based file transfer application that allows a client
to upload and download files through a server using TCP sockets.

## Features
- TCP socket communication
- Basic username and password authentication
- File upload from client to server
- File download from server to client
- Automatic creation of storage directories

## Technologies Used
- Python
- Socket module
- OS module
- TCP protocol

## Project Structure
- client.py: Client application
- server.py: Server application
- client_files/: Client-side file storage
- server_files/: Server-side file storage

## How to Run

1. Install Python 3.
2. Open a terminal in the project directory.
3. Start the server:

   python server.py

4. Open another terminal.
5. Start the client:

   python client.py

## Authentication
The current demonstration version uses credentials
configured in server.py.

## Future Improvements
- Secure password storage
- Encrypted communication
- Improved file transfer reliability
- Graphical user interface
- Multiple simultaneous clients
