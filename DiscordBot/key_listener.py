import json
import requests
import threading
from pynput import keyboard

with open("config.json") as f:
    config = json.load(f)

WEBHOOK_URL = config.get("WEBHOOK_URL")

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

def send_command(command):
    payload = {"content": command}
    r = requests.post(WEBHOOK_URL, json=payload)
    print(f"Отправлено: {command}, статус: {r.status_code}")

if __name__ == "__main__":
    print("Клавиатурный слушатель запущен.")
    with keyboard.Listener(on_press=on_key_press) as listener:
        listener.join()
