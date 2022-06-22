import discord
from discord.ext import commands
import youtube_dl
import urllib.parse, urllib.request, re

queues = {}
from administrative import banned_users

def check_queue(ctx, id):
  vc = ctx.voice_client
  if queues[id] != []: # проверяет пустая ли очередь
    url = queues[id].pop(0)
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
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5 -probesize 256M',
    'options': '-vn -sn -dn'
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
  
  @commands.command(name="leave", description="leaves the voice channel")
  async def leave(self, ctx):
    server = ctx.message.guild
    queues[server.id] = []
    await ctx.voice_client.disconnect()
    await ctx.channel.send("I left vc")
  
  @commands.command(name="pause", description="pauses music")
  async def pause(self, ctx):
    ctx.voice_client.pause() 
    await ctx.channel.send("Paused")

  @commands.command(name="resume", description="resumes playing music")
  async def resume(self, ctx):
    ctx.voice_client.resume()
    await ctx.channel.send("Resumed")

  @commands.command(name="play", description="request music")
  async def play(self,ctx, *, search):
    server = ctx.message.guild
    if ctx.message.author.id in banned_users[server.id]:
      await ctx.reply("xd")
      return False
      
    if ctx.author.voice is None:
      await ctx.send("You are not in a vc")
      return False
      
    if ctx.voice_client is None and True: #вход в гк
      voice_channel = ctx.author.voice.channel
       
      await voice_channel.connect()
      source = await convert_url(search)
      
      if server.id in queues:
        queues[server.id].append(source) #добавление ссылки в массив очереди
      else:
        queues[server.id] = [source]
        
      vc = ctx.voice_client
      vc.play(queues[server.id].pop(0), after = lambda x: check_queue(ctx, server.id))

    else: #выполняется всегда после первого входа
      server = ctx.message.guild
      source = await convert_url(search) 
      vc = ctx.voice_client
      
      if vc.is_playing():
        queues[server.id].append(source) #добавление ссылки в массив очереди
      
      else:
        vc.play(source, after = lambda x: check_queue(ctx, server.id))

  @commands.command(name="skip", description="skips current track")
  async def skip(self, ctx):
    server = ctx.message.guild
    vc = ctx.voice_client  
    vc.stop()
    vc.play(queues[server.id].pop(0), after = lambda x: check_queue(ctx, server.id))    

  
def setup(client):
  client.add_cog(music(client))