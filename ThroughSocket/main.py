import pygame
from pynput import keyboard

pygame.mixer.init()
song_path = '../lion.mp3'
pygame.mixer.music.load(song_path)

is_playing = False

def toggle_song():
    global is_playing
    if is_playing:
        pygame.mixer.music.stop()
        print("stopped")
    else:
        pygame.mixer.music.play()
        print("playing")
    is_playing = not is_playing

def on_press(key):
    try:
        if key.char == 'm':
            toggle_song()
    except AttributeError:
        if key == keyboard.Key.esc:
            print("exit")
            return False


print("m - play/stop. esc - exit")

# Запуск слушателя клавиатуры
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
