import discord
from discord.ext import commands
import youtube_dl
import urllib.parse, urllib.request, re

queues = {}

def check_queue(ctx, id):
  vc = ctx.voice_client
  if queues[id] != []: # проверяет пустая ли очередь
    url = queues[id].pop(0)
    print(url)
    vc.play(url, after = lambda x: check_queue(ctx, id))

class music(commands.Cog):
  def __init__(self, client):
    self.client = client
  
  @commands.command()
  async def leave(self, ctx):
    server = ctx.message.guild
    queues[server.id] = []
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
    
    if ctx.voice_client is None: #вход в гк
      vc = ctx.voice_client
      server = ctx.message.guild
      voice_channel = ctx.author.voice.channel 

      await voice_channel.connect()
      query_string = urllib.parse.urlencode({
        'search_query': search
      })
      htm_content = urllib.request.urlopen(
        'https://www.youtube.com/results?' + query_string
      )
      search_results = re.findall(r'/watch\?v=(.{11})', htm_content.read().decode())

      FFMPEG_OPTIONS = {
      'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
      'options': '-vn'
      }
      YDL_OPTIONS = {'format':"bestaudio"}
      url = 'https://www.youtube.com/watch?v=' + search_results[0]
      print(url)
      vc = ctx.voice_client
      with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(url, download=False)
        url2 = info['formats'][0]['url']
        source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
        
      if server.id in queues:
        queues[server.id].append(source) #добавление ссылки в массив очереди
        print("used 1st if")
      else:
        queues[server.id] = [source]
        print("used 2nd if")

      vc.play(queues[server.id].pop(0), after = lambda x: check_queue(ctx, server.id))

    else: #выполняется всегда после первого входа
      server = ctx.message.guild
      voice_channel = ctx.author.voice.channel 

      query_string = urllib.parse.urlencode({
        'search_query': search
      })
      htm_content = urllib.request.urlopen(
        'https://www.youtube.com/results?' + query_string
      )
      search_results = re.findall(r'/watch\?v=(.{11})', htm_content.read().decode())

      FFMPEG_OPTIONS = {
      'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
      'options': '-vn'
      }
      YDL_OPTIONS = {'format':"bestaudio"}  
      url = 'https://www.youtube.com/watch?v=' + search_results[0]
      vc = ctx.voice_client
      
      if vc.is_playing():
        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
          info = ydl.extract_info(url, download=False)
          url2 = info['formats'][0]['url']
          source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
        queues[server.id].append(source) #добавление ссылки в массив очереди
      
      else:
        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
          info = ydl.extract_info(url, download=False)
          url2 = info['formats'][0]['url']
          source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
          vc.play(source, after = lambda x: check_queue(ctx, server.id))
      

  @commands.command()
  async def clear(ctx, self):
    server = ctx.message.guild
    queues[server.id] = []
    
def setup(client):
  client.add_cog(music(client))