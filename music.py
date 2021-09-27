import discord
from discord.ext import commands
import youtube_dl

import urllib.parse, urllib.request, re
from asyncio import sleep

class music(commands.Cog):
  def __init__(self, client):
    self.client = client
  
  @commands.command()
  async def playurl(self, ctx, url):
    if ctx.author.voice is None:
      await ctx.send("You are not in a vc")
    voice_channel = ctx.author.voice.channel
    if ctx.voice_client is None:
      await voice_channel.connect()
      FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
      YDL_OPTIONS = {'format':"bestaudio"}
      vc = ctx.voice_client
      with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
          info = ydl.extract_info(url, download=False)
          url2 = info['formats'][0]['url']
          source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
          vc.play(source)
          while vc.is_playing():
            await sleep(600)
          await vc.disconnect()
    else:
      ctx.voice_client.stop()
      FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
      YDL_OPTIONS = {'format':"bestaudio"}
      vc = ctx.voice_client
      with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
          info = ydl.extract_info(url, download=False)
          url2 = info['formats'][0]['url']
          source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
          vc.play(source)
          while vc.is_playing():
            await sleep(600)
          await vc.disconnect()
  @commands.command()
  async def leave(self, ctx):
    await ctx.voice_client.disconnect()
    await ctx.channel.send("I left vc")
  
  @commands.command()
  async def pause(self, ctx):
    ctx.voice_client.pause()
    await ctx.channel.send("Paused")

  @commands.command()
  async def resume(self, ctx):
    ctx.voice_client.resume()
    await ctx.channel.send("Resumed")
  
  @commands.command()
  async def play(self,ctx, *, search):
    if ctx.author.voice is None:
      await ctx.send("You are not in a vc")
    voice_channel = ctx.author.voice.channel
    if ctx.voice_client is None:
      await voice_channel.connect()
      query_string = urllib.parse.urlencode({
      'search_query': search
      })
      htm_content = urllib.request.urlopen(
      'https://www.youtube.com/results?' + query_string
      )
      search_results = re.findall(r'/watch\?v=(.{11})', htm_content.read().decode()) #1000-7?
      FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
      YDL_OPTIONS = {'format':"bestaudio"}
      vc = ctx.voice_client
      url = 'https://www.youtube.com/watch?v=' + search_results[0]
      with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
          info = ydl.extract_info(url, download=False)
          url2 = info['formats'][0]['url']
          source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
          vc.play(source)
          while vc.is_playing():
            await sleep(600)
          await vc.disconnect()
    else:
      ctx.voice_client.stop()
      query_string = urllib.parse.urlencode({
      'search_query': search
      })
      htm_content = urllib.request.urlopen(
      'https://www.youtube.com/results?' + query_string
      )
      search_results = re.findall(r'/watch\?v=(.{11})', htm_content.read().decode()) #1000-7?
      FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
      YDL_OPTIONS = {'format':"bestaudio"}
      vc = ctx.voice_client
      url = 'https://www.youtube.com/watch?v=' + search_results[0]
      with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
          info = ydl.extract_info(url, download=False)
          url2 = info['formats'][0]['url']
          source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
          vc.play(source)
          while vc.is_playing():
            await sleep(600)
          await vc.disconnect()

def setup(client):
  client.add_cog(music(client))