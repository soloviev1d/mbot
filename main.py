#подгружать pip install -U discord.py[voice] в ядро
#pip install youtube-dl
#pip install -U ffmpeg
import os
import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
import youtube_dl
import json
import urllib.parse, urllib.request, re
import keep_alive

my_secret = os.environ['token']
client = commands.Bot(command_prefix = '-')

@client.event
async def on_ready():
  print('Logged in as {0.user}'.format(client))
  print('~~~~~~~~~~~~~~~~~~')

@client.command(pass_context = True)
async def leave(ctx):
  if(ctx.voice_client):
    await ctx.guild.voice_client.disconnect()
    await ctx.send('I left the vc')
  else:
    await ctx.send('I am not in a vc!')

@client.command(pass_context = True)
async def play(ctx, *,search):
  if(ctx.author.voice):
    channel = ctx.message.author.voice.channel
    voice = await channel.connect()
    query_string = urllib.parse.urlencode({
      'search_query': search
    })
    htm_content = urllib.request.urlopen(
      'https://www.youtube.com/results?' + query_string
    )
    search_results = re.findall(r'/watch\?v=(.{11})', htm_content.read().decode()) #1000-7?
    ydl_opts = {
      'format': 'bestaudio/best', 'postprocessors':[{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
      }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
      ydl.download(['https://www.youtube.com/watch?v=' + search_results[0]])
    for file in os.listdir("./"):
      if file.endswith(".mp3"):
        os.rename(file, "song.mp3")
    source = FFmpegPCMAudio('song.mp3')
    player = voice.play(source)
  else:
    await ctx.send('You are not in a vc!')



keep_alive.keep_alive()
client.run(my_secret)