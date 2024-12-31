import socket
from pynput import keyboard
import threading

# Настройки сервера
HOST = '79.137.184.21'  # Принимает подключения от всех адресов
PORT = 8000      # Порт для подключения клиентов

# Инициализация сокета
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()

print(f"🚀 Сервер запущен на {HOST}:{PORT}")

clients = []

# Функция для отправки команд клиентам
def broadcast(message):
    for client in clients:
        try:
            client.send(message.encode())
        except:
            clients.remove(client)

# Принятие клиентов
def accept_clients():
    while True:
        client, addr = server_socket.accept()
        print(f"✅ Подключен клиент: {addr}")
        clients.append(client)

# Запуск потока для принятия клиентов
threading.Thread(target=accept_clients, daemon=True).start()

# Обработка нажатий клавиш
def on_press(key):
    try:
        if key.char == 'm':  # Клавиша 'M'
            broadcast('PLAY')
            print("🎵 Отправлена команда: PLAY")
        if key == keyboard.Key.esc:  # Клавиша 'Esc'
            broadcast('STOP')
            print("⏹️ Отправлена команда: STOP")
            return False  # Завершает слушатель
    except AttributeError:
        pass

# Инструкция для пользователя
print("Нажмите 'M' для воспроизведения/остановки музыки у всех клиентов. Для выхода нажмите 'Esc'.")

# Запуск слушателя клавиатуры
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()

server_socket.close()
