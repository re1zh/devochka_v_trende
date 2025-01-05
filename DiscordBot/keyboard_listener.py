import requests
from pynput import keyboard

TOKEN = 'MTMyNDc1MDIyNTExNzU0ODU4NA.GIJpj8.48Z95jOwBTNEY75WRnEcO4kctlFf85fy5GgZko'
CHANNEL_ID = '1324965853363703848'
PLAY_COMMAND = '!play lion'

WEBHOOK_URL = 'https://discord.com/api/webhooks/1324971072155684904/QolT7eIOS7NUmF7jF80aOWhN4ZSSGs2vi_8sPEun_V28jiQolvpp1QhBFhy-LEZ5pkZc'

def send_message_to_discord(message):
    url = f'https://discord.com/api/v10/channels/{CHANNEL_ID}/messages'
    headers = {
        'Authorization': f'Bot {TOKEN}',
        'Content-Type': 'application/json'
    }
    payload = {'content': message}

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        print('Command sent successfully')
    else:
        print(f'Error: {response.status_code}, {response.text}')


def send_message_via_webhook(message):
    payload = {
        'content': message,
    }
    response = requests.post(WEBHOOK_URL, json=payload)

    if response.status_code == 204:
        print('Command sent through Webhook')
    else:
        print(f'Error: {response.status_code}, {response.text}')

def on_press(key):
    try:
        if key.char == 'm':
            print('Sending !play command')
            # send_message_to_discord(PLAY_COMMAND)
            send_message_via_webhook(PLAY_COMMAND)
    except AttributeError:
        return f'Error: {AttributeError}'

with keyboard.Listener(on_press=on_press) as listener:
    listener.join()