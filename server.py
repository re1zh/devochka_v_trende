import socket
from pynput import keyboard
import threading

HOST = '0.0.0.0'
PORT = 27007

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()

print(f"Server started {HOST}:{PORT}")

clients = []

def broadcast(message):
    for client in clients:
        try:
            client.send(message.encode())
        except:
            clients.remove(client)

def accept_clients():
    while True:
        client, addr = server_socket.accept()
        print(f"Client connected: {addr}")
        clients.append(client)

threading.Thread(target=accept_clients, daemon=True).start()

def on_press(key):
    try:
        if key.char == 'm':
            broadcast('PLAY')
            print("Command: PLAY")
        if key == keyboard.Key.esc:
            broadcast('STOP')
            print("Command: STOP")
            return False
    except AttributeError:
        pass

print("Press M - Play/Stop. Esc - to exit")

# Запуск слушателя клавиатуры
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()

server_socket.close()
