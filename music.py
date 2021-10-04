import discord
from discord.ext import commands
import youtube_dl
import urllib.parse, urllib.request, re
from asyncio import sleep
from queue import Queue

queues = {}
queue = Queue()

def check_queue(ctx, id): #проверка есть ли что-то в очереди
  vc = ctx.voice_client
  FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
  }
  YDL_OPTIONS = {'format':"bestaudio"}

  if queues[id] != []: # проверяет пустая ли очередь
    url = queues[id].pop(0)
    with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
      info = ydl.extract_info(url, download=False)
      url2 = info['formats'][0]['url']
      source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS) #был await
      vc.play(source)

class music(commands.Cog):
  def __init__(self, client):
    self.client = client
  
  @commands.command()
  async def leave(self, ctx):
    global queue
    queue = Queue()
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
      
      if server.id in queues:
        queue.put('https://www.youtube.com/watch?v=' + search_results[0])
        queues[server.id].append(queue.get()) #добавление ссылки в массив очереди
        print("used 1st if")
      else:
        queue.put('https://www.youtube.com/watch?v=' + search_results[0])
        queues[server.id] = [queue.get()]
        print("used 2nd if")

      FFMPEG_OPTIONS = {
      'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
      'options': '-vn'
      }
      YDL_OPTIONS = {'format':"bestaudio"}
      url = queues[server.id].pop(0) 
      print(url)
      vc = ctx.voice_client
      with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(url, download=False)
        url2 = info['formats'][0]['url']
        source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
        vc.play(source, after = lambda x: check_queue(ctx, server.id))

    else: #выполняется всегда после первого входа
      server = ctx.message.guild
      voice_channel = ctx.author.voice.channel 
      vc = ctx.voice_client
      query_string = urllib.parse.urlencode({
        'search_query': search
      })
      htm_content = urllib.request.urlopen(
        'https://www.youtube.com/results?' + query_string
      )
      search_results = re.findall(r'/watch\?v=(.{11})', htm_content.read().decode())
      queue.put('https://www.youtube.com/watch?v=' + search_results[0])
      queues[server.id].append(queue.get()) #добавление ссылки в массив очереди

      ''' FFMPEG_OPTIONS = {
      'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
      'options': '-vn'
      }
      YDL_OPTIONS = {'format':"bestaudio"}
      url = queues[server.id].append()
      await ctx.send(url) 

      with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(url, download=False)
        url2 = info['formats'][0]['url']
        source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
        vc.play(source, after = lambda: check_queue(server.id)) '''

  
      

  @commands.command()
  async def clear(ctx, self):
    server = ctx.message.guild
    queues[server.id] = []
    
def setup(client):
  client.add_cog(music(client))