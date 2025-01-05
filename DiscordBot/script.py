import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
bot = commands.Bot(command_prefix='!', intents=intents)

TOKEN = 'MTMyNDc1MDIyNTExNzU0ODU4NA.GIJpj8.48Z95jOwBTNEY75WRnEcO4kctlFf85fy5GgZko'

# @bot.command()
# async def echo(ctx, *args):
#     await ctx.send(' '.join(args))

@bot.event
async def on_message(message):
    if message.author == bot.user:
        await bot.process_commands(message)
        return
    #
    # if message.webhook_id:
    #     await bot.process_commands(message)
    #     return
    #
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
    if ctx.voice_client is None:
        await ctx.send('Use "join" command to connect to VC.')
        return

    sound_file = f'./sounds/{sound}.mp3'

    if os.path.isfile(sound_file):
        discord.opus.load_opus('/opt/homebrew/lib/libopus.dylib')
        ctx.voice_client.stop()
        ctx.voice_client.play(discord.FFmpegPCMAudio(sound_file, options='-loglevel quiet'))
        await ctx.send(f'Playing: **{sound}**')
    else:
        await ctx.send('There is no such file in directory.')

bot.run(TOKEN)