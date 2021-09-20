#подгружать pip install -U discord.py[voice] в ядро
#pip install youtube-dl
#pip install -U ffmpeg
import os
import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord import FFmpegPCMAudio
import youtube_dl
import json

my_secret = os.environ['token']



client = commands.Bot(command_prefix = '-')

@client.event
async def on_ready():
  print('Logged in as {0.user}'.format(client))
  print('~~~~~~~~~~~~~~~~~~')

@client.command()
async def hello(ctx):
  await ctx.send('Hello World!')

''' @client.command(pass_context = True)
async def join(ctx):
  if(ctx.author.voice):
    channel = ctx.message.author.voice.channel
    voice = await channel.connect()
    source = FFmpegPCMAudio('bab.mp3')
    while(True):
      player = voice.play(source)
  else:
    await ctx.send('You are not in a vc!') '''

@client.command(pass_context = True)
async def leave(ctx):
  if(ctx.voice_client):
    await ctx.guild.voice_client.disconnect()
    await ctx.send('I left the vc')
  else:
    await ctx.send('I am not in a vc!')

@client.command(pass_context = True)
async def play(ctx, url:str):
  if(ctx.author.voice):
    channel = ctx.message.author.voice.channel
    voice = await channel.connect()

    ydl_opts = {
      'format': 'bestaudio/best', 'postprocessors':[{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
      }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
      ydl.download([url])
    for file in os.listdir("./"):
      if file.endswith(".mp3"):
        os.rename(file, "song.mp3")

    source = FFmpegPCMAudio('song.mp3')
    player = voice.play(source)
  else:
    await ctx.send('You are not in a vc!')

client.run(my_secret)
