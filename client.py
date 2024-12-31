import socket
import pygame

# Настройки клиента
SERVER_HOST = '79.137.184.21'  # IP-адрес сервера
SERVER_PORT = 8000       # Порт сервера

# Инициализация аудиосистемы
pygame.mixer.init()
song_path = 'lion.mp3'
pygame.mixer.music.load(song_path)

# Подключение к серверу
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_HOST, SERVER_PORT))
print(f"✅ Подключено к серверу {SERVER_HOST}:{SERVER_PORT}")

# Функция для управления воспроизведением
is_playing = False

def toggle_song():
    global is_playing
    if is_playing:
        pygame.mixer.music.stop()
        print("⏹️ Песня остановлена.")
    else:
        pygame.mixer.music.play()
        print("🎵 Песня начала воспроизводиться.")
    is_playing = not is_playing

# Получение команд от сервера
try:
    while True:
        command = client_socket.recv(1024).decode()
        if command == 'PLAY':
            toggle_song()
        elif command == 'STOP':
            pygame.mixer.music.stop()
            print("⏹️ Остановлено по команде сервера.")
except KeyboardInterrupt:
    print("🚪 Отключение от сервера.")
finally:
    client_socket.close()
