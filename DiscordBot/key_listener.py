import os
import json
import requests
import threading
from pynput import keyboard

WEBHOOK_URL = os.getenv("WEBHOOK_URL")

if not TOKEN or not WEBHOOK_URL:
    raise ValueError("Укажите WEBHOOK_URL через переменные окружения.")

key_binds = {
    "]": "!play lion",
    "/": "!pause_or_resume"
}

is_paused = False

def on_key_press(key):
    global is_paused
    try:
        if hasattr(key, 'char'):
            char = key.char
            if char == "/" and is_paused:
                send_command("!resume")
                is_paused = False
            elif char == "/" and not is_paused:
                send_command("!pause")
                is_paused = True
            elif char in key_binds:
                send_command(key_binds[char])
    except AttributeError:
        pass

def send_command_via_webhook(command):
    data = {"content": command}
    response = requests.post(WEBHOOK_URL, json=data)
    if response.status_code == 204:
        print(f"Команда '{command}' отправлена через вебхук.")
    else:
        print(f"Ошибка: {response.status_code}, {response.text}")

if __name__ == "__main__":
    print("Клавиатурный слушатель запущен.")
    with keyboard.Listener(on_press=on_key_press) as listener:
        listener.join()
