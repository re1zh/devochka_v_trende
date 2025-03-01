import discord
import os
import json
import requests
import threading
import platform

from discord.ext import commands
from pynput import keyboard

from database import SessionLocal, Song

SYSTEM_OS = platform.system()

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
bot = commands.Bot(command_prefix='!', intents=intents)

key_binds = {}

@bot.command()
async def bindkey(ctx, key: str, song_name: str):
    db = SessionLocal()
    song = db.query(Song).filter(Song.name == song_name).first()
    db.close()

    if not song:
        await ctx.send(f"Песня '{song_name}' не найдена в базе данных.")
        return

    key_binds[key] = song_name
    await ctx.send(f"Клавиша `{key}` теперь воспроизводит `{song_name}`.")

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
async def addsong(ctx, name: str, path: str):
    db = SessionLocal()
    existing_song = db.query(Song).filter(Song.name == name).first()

    if existing_song:
        await ctx.send(f"Песня '{name}' уже есть в базе данных.")
    else:
        song = Song(name=name, path=path)
        db.add(song)
        db.commit()
        await ctx.send(f"Песня '{name}' добавлена в базу данных.")
    db.close()

@bot.command()
async def delsong(ctx, name: str):
    db = SessionLocal()
    song = db.query(Song).filter(Song.name == name).first()

    if song:
        db.delete(song)
        db.commit()
        await ctx.send(f"Песня '{name}' удалена.")
    else:
        await ctx.send(f"Песня '{name}' не найдена.")
    db.close()

@bot.command()
async def listsongs(ctx):
    db = SessionLocal()
    songs = db.query(Song).all()
    db.close()

    if not songs:
        await ctx.send("В базе данных нет песен.")
    else:
        song_list = "\n".join([f"{song.name}" for song in songs])
        await ctx.send(f"Доступные песни:\n{song_list}")

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
async def play(ctx, name: str):
    global is_playing, is_paused

    if ctx.voice_client is None:
        await ctx.send("Сначала используйте `!join`, чтобы подключить бота к голосовому каналу.")
        return

    db = SessionLocal()
    song = db.query(Song).filter(Song.name == name).first()
    db.close()

    if not song:
        await ctx.send(f"Песня '{name}' не найдена в базе данных.")
        return

    try:
        if ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            is_playing = False
            is_paused = False
            await ctx.send("Остановлено.")

        is_paused = False

        if os.path.isfile(song.path):
            if SYSTEM_OS == "Windows":
                ffmpeg_path = "C:\\ffmpeg-master-latest-win64-gpl\\bin\\ffmpeg.exe"
                executable_option = {"executable": ffmpeg_path}
            else:
                opus_path = "/opt/homebrew/lib/libopus.dylib"
                discord.opus.load_opus(opus_path)
                executable_option = {}

            ctx.voice_client.play(
                discord.FFmpegPCMAudio(song.path, options='-loglevel quiet', **executable_option)
            )
            is_playing = True
            await ctx.send(f"Воспроизводится: **{name}**")
        else:
            await ctx.send("Файл не найден. Проверьте путь.")

    except Exception as e:
        await ctx.send(f"Ошибка: {str(e)}")

@bot.command()
async def pause(ctx):
    global is_paused, is_playing

    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.pause()
        is_paused = True
        is_playing = False
        await ctx.send("Музыка на паузе.")
    else:
        await ctx.send("Сейчас ничего не играет.")

@bot.command()
async def resume(ctx):
    global is_paused, is_playing

    if ctx.voice_client and is_paused:
        ctx.voice_client.resume()
        is_paused = False
        is_playing = True
        await ctx.send("Музыка продолжает играть.")
    else:
        await ctx.send("Нечего возобновлять.")


def on_key_press(key):
    try:
        if hasattr(key, 'char') and key.char in key_binds:
            send_command_via_webhook(f"!play {key_binds[key.char]}")
        elif key.char == '/':
            send_command_via_webhook("!pause" if is_playing else "!resume")
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