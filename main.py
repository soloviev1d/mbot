#подгружать pip install -U discord.py[voice] в ядро
#pip install youtube-dl
#pip install -U ffmpeg
import os
import discord
from discord.ext import commands
import music



cogs = [music]
#my_secret = os.environ['token']
client = commands.Bot(command_prefix = '!')

for i in range(len(cogs)):
  cogs[i].setup(client)

@client.event
async def on_ready():
  print('Logged in as {0.user}'.format(client))
  print('~~~~~~~~~~~~~~~~~~')

@client.command(pass_context = True)
async def amogus(ctx):
  await ctx.send(file=discord.File('gus.gif'))

#keep_alive.keep_alive()
client.run('ODkzNzY2ODkxNTE1MDIzMzYw.YVgPSA.jc99AlJGpx6N4MuR-MfqXfr76Ew')