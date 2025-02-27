import discord
import os
import json
import requests
import threading
import platform

from discord.ext import commands
from pynput import keyboard

SYSTEM_OS = platform.system()

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
bot = commands.Bot(command_prefix='!', intents=intents)

try:
    with open('config.json') as config_file:
        config = json.load(config_file)

    TOKEN = config.get('DISCORD_TOKEN')
    WEBHOOK_URL = config.get('WEBHOOK_URL')

    if not TOKEN or not WEBHOOK_URL:
        raise ValueError("Укажите DISCORD_TOKEN и WEBHOOK_URL в config.json")

except Exception as e:
    raise ValueError(f"Ошибка при загрузке конфигурации: {str(e)}")

is_playing = False
is_paused = False

@bot.command()
async def echo(ctx, *args):
    await ctx.send(' '.join(args))

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.webhook_id:
        ctx = await bot.get_context(message)
        await bot.invoke(ctx)
        return

    await bot.process_commands(message)

@bot.command()
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
        await ctx.send(f"Подключился к: {channel.name}")
    else:
        await ctx.send("Вы должны находиться в голосовом канале.")

@bot.command()
async def leave(ctx):
    if ctx.voice_client and ctx.voice_client.is_connected():
        await ctx.voice_client.disconnect()
        await ctx.send("Отключился от голосового канала.")
    else:
        await ctx.send("Не подключен к голосовому каналу.")

@bot.command()
async def play(ctx, sound: str):
    global is_playing, is_paused

    if ctx.voice_client is None:
        await ctx.send('Сначала используйте команду "join", чтобы подключить бота к голосовому каналу.')
        return

    sound_file = f'./sounds/{sound}.mp3'

    try:
        if is_playing:
            ctx.voice_client.stop()
            is_playing = False
            is_paused = False
            await ctx.send("Остановлено.")
        elif os.path.isfile(sound_file):
            if SYSTEM_OS == "Windows":
                ffmpeg_path = "C:\\ffmpeg-master-latest-win64-gpl\\bin\\ffmpeg.exe"
                executable_option = {"executable": ffmpeg_path}
            else:
                opus_path = "/opt/homebrew/lib/libopus.dylib"
                discord.opus.load_opus(opus_path)
                executable_option = {}

            ctx.voice_client.stop()
            ctx.voice_client.play(
                discord.FFmpegPCMAudio(sound_file, options='-loglevel quiet', **executable_option)
            )
            is_playing = True
            is_paused = False
            await ctx.send(f"Воспроизводится: **{sound}**")
        else:
            await ctx.send("Файл не найден.")
    except Exception as e:
        await ctx.send(f"Ошибка: {str(e)}")

@bot.command()
async def pause(ctx):
    global is_paused
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.pause()
        is_paused = True
        await ctx.send("Пауза")
    else:
        await ctx.send("Сейчас ничего не воспроизводится.")

@bot.command()
async def resume(ctx):
    global is_paused
    if ctx.voice_client and is_paused:
        ctx.voice_client.resume()
        is_paused = False
        await ctx.send("Возобновлено")
    else:
        await ctx.send("Нечего возобновлять.")

def on_key_press(key):
    try:
        if key.char == ']':
            send_command_via_webhook("!play lion")
        elif key.char == '/':
            if is_paused:
                send_command_via_webhook("!pause")
            else:
                send_command_via_webhook("!resume")
    except AttributeError:
        pass

def send_command_via_webhook(command):
    data = {"content": command}
    response = requests.post(WEBHOOK_URL, json=data)
    if response.status_code == 204:
        print(f"Команда '{command}' отправлена через вебхук.")
    else:
        print(f"Ошибка: {response.status_code}, {response.text}")

def start_keyboard_listener():
    with keyboard.Listener(on_press=on_key_press) as listener:
        listener.join()

listener_thread = threading.Thread(target=start_keyboard_listener, daemon=True)
listener_thread.start()

bot.run(TOKEN)