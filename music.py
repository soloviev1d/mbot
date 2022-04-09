import discord
from discord.ext import commands
import youtube_dl
import urllib.parse, urllib.request, re

queues = {}
counters = {}
loop_switch = False

def check_queue(ctx, id):
  vc = ctx.voice_client
  if loop_switch == False:
    try:
      url = queues[id][counters[id][0]]
      counters[id][0] += 1 #чутка переделать чтобы не поймать аут оф ренж, добавить условие с луп свитчом
      vc.play(url, after = lambda x: check_queue(ctx, id))
    except IndexError:
      ctx.channel.send("Queue ended")
  else:
    try:
      url = queues[id][counters[id][0]]
      counters[id][0] += 1 #чутка переделать чтобxaы не поймать аут оф ренж, добавить условие с луп свитчом #нахуя?????
      vc.play(url, after = lambda x: check_queue(ctx, id))
    except IndexError:
      counters[id][0]=0
      vc.play(url, after = lambda x: check_queue(ctx, id))


async def convert_url(search):
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
  with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
    info = ydl.extract_info(url, download=False)
    url2 = info['formats'][0]['url']
    source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
  return source
    
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
      server = ctx.message.guild
      voice_channel = ctx.author.voice.channel
       
      await voice_channel.connect()
      source = await convert_url(search)
      
      if server.id in queues:
        queues[server.id].append(source) #добавление ссылки в массив очереди
      else:
        counters[server.id][0] = 0
        queues[server.id] = [source]
        
      vc = ctx.voice_client
      next = queues[server.id][counters[server.id][0]]
      print(f"{next}~~~~~~~~~~~")
      vc.play(next, after = lambda x: check_queue(ctx, server.id))

    else: #выполняется всегда после первого входа
      server = ctx.message.guild
      source = await convert_url(search) 
      vc = ctx.voice_client
      
      if vc.is_playing():
        queues[server.id].append(source) #добавление ссылки в массив очереди
      
      else:
        vc.play(source, after = lambda x: check_queue(ctx, server.id))

  @commands.command()
  async def skip(self, ctx):
    server = ctx.message.guild
    vc = ctx.voice_client  
    vc.stop()
    counters[server.id][0] += 1
    try:
      vc.play(queues[server.id][counters[server.id][0]], after = lambda x: check_queue(ctx, server.id))
    except IndexError:
      counters[server.id] = 0
      await ctx.channel.send("Last track in queue jumping to first")
      vc.play(queues[server.id][counters[server.id][0]], after = lambda x: check_queue(ctx, server.id))

  @commands.command()
  async def loop(self, ctx):
    global loop_switch
    if loop_switch == False:
      loop_switch = True
      await ctx.channel.send("Now looping the queue")
    else:
      loop_switch = False
      await ctx.channel.send("Stopped looping the queue")
      
def setup(client):
  client.add_cog(music(client))