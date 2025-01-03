import socket
import pygame

SERVER_HOST = '192.168.0.161'
SERVER_PORT = 27007

pygame.mixer.init()
song_path = '../lion.mp3'
pygame.mixer.music.load(song_path)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_HOST, SERVER_PORT))
print(f"Connected to server {SERVER_HOST}:{SERVER_PORT}")

is_playing = False

def toggle_song():
    global is_playing
    if is_playing:
        pygame.mixer.music.stop()
        print("Stopped.")
    else:
        pygame.mixer.music.play()
        print("Playing.")
    is_playing = not is_playing

try:
    while True:
        command = client_socket.recv(1024).decode()
        if command == 'PLAY':
            toggle_song()
        elif command == 'STOP':
            pygame.mixer.music.stop()
            print("Stopped from server.")
except KeyboardInterrupt:
    print("Disconnected.")
finally:
    client_socket.close()
