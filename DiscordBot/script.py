import discord
import os
import json
import requests
import threading

from discord.ext import commands
from pynput import keyboard

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
bot = commands.Bot(command_prefix='!', intents=intents)

try:
    with open('config.json') as config_file:
        config = json.load(config_file)

    TOKEN = config.get('DISCORD_TOKEN')
    WEBHOOK_URL = config.get('WEBHOOK_URL')
except not TOKEN or not WEBHOOK_URL:
    raise ValueError("Укажите DISCORD_TOKEN и WEBHOOK_URL в config.json")

is_playing = False

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
        await ctx.send(f"Connected to: {channel.name}")
    else:
        await ctx.send("You should be in VC.")

@bot.command()
async def leave(ctx):
    if ctx.voice_client and ctx.voice_client.is_connected():
        await ctx.voice_client.disconnect()
        await ctx.send("Disconnected from VC.")
    else:
        await ctx.send("Not connected to VC.")

@bot.command()
async def play(ctx, sound: str):
    global is_playing

    if ctx.voice_client is None:
        await ctx.send('Use "join" command to connect to VC.')
        return

    sound_file = f'./sounds/{sound}.mp3'

    try:
        if is_playing:
            ctx.voice_client.stop()
            is_playing = False
            await ctx.send("Stopped.")
        elif os.path.isfile(sound_file):
            # Если ваша система не Windows, то раскомментируйте строку ниже и введите свой путь до библиотеки libopus
            # discord.opus.load_opus()
            ctx.voice_client.stop()
            ctx.voice_client.play(
                discord.FFmpegPCMAudio(sound_file
                    , options='-loglevel quiet'
                    # Если ваша система Windows, то введите путь до файла ffmpeg.exe
                    , executable="c:\\ffmpeg-master-latest-win64-gpl\\bin\\ffmpeg.exe")
            )
            is_playing = True
            await ctx.send(f"Playing: **{sound}**")
        else:
            await ctx.send("File not found.")
    except Exception as e:
        await ctx.send(f"Error: {str(e)}")

def on_key_press(key):
    try:
        # Введите свою клавишу для триггера команды
        if key.char == 'm':
            # Введите свою песню из директории sounds
            send_command_via_webhook("!play lion")
    except AttributeError:
        pass

def send_command_via_webhook(command):
    data = {"content": command}
    response = requests.post(WEBHOOK_URL, json=data)
    if response.status_code == 204:
        print(f"Command '{command}' sent through webhook.")
    else:
        print(f"Error: {response.status_code}, {response.text}")

def start_keyboard_listener():
    with keyboard.Listener(on_press=on_key_press) as listener:
        listener.join()

listener_thread = threading.Thread(target=start_keyboard_listener, daemon=True)
listener_thread.start()

bot.run(TOKEN)