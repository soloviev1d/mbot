import os
import discord
from discord.ext import commands
import music


cogs = [music]
my_secret = os.environ['tokentest']
client = commands.Bot(command_prefix = '!')

for i in range(len(cogs)):
  cogs[i].setup(client)

@client.event
async def on_ready():
  print('Logged in as {0.user}'.format(client))
  print('~~~~~~~~~~~~~~~~~~')
  #channel = client.get_channel(id = 888827334503858199)
 # channel.send("{command_prefix}setup") # :))

@client.command(pass_context = True)
async def amogus(ctx):
  await ctx.send(file=discord.File('gus.gif'))






#keep_alive.keep_alive()
client.run(my_secret)