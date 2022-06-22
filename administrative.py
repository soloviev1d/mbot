import discord
from discord.ext import commands

banned_users = {}
super_users = {}

class administrative(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command(name="block", description="Blocks user from playing music")
    async def block(self, ctx, user: discord.User):
        if ctx.message.author.id == 304651000889737217 or ctx.message.author in super_users:
            server = ctx.message.guild

            if server.id in banned_users:
                banned_users[server.id].append(user.id)
            else:
                banned_users[server.id] = [user.id]


            await ctx.send(f"Banned user {user} from playing music")
        else:
            await ctx.reply("You are not a super user")


    @commands.command(name="unblock", description="Returns permission to user for playing music")
    async def unblock(self,ctx, user: discord.User):
        if ctx.message.author.id == 304651000889737217 or ctx.message.author in super_users:
            server = ctx.message.guild
            if server.id not in banned_users:
                banned_users[server.id] = []

            if user.id not in banned_users[server.id]:
                await ctx.send(f"{user} isn't banned")
                return False

            if True:
                for i in range(len(banned_users[server.id])):

                    if banned_users[server.id][i] == user.id:
                        banned_users[server.id][i] = None
                        await ctx.send(f"Permission returned to {user} for playing music")

        else:
            await ctx.reply("You are not a super user")


    @commands.command(name="op", description="Gives user permission to block others")
    async def op(self,ctx,user: discord.User):
        if ctx.message.author.id == 304651000889737217 or ctx.message.author in super_users:
            server = ctx.message.guild

            if server.id in super_users:
                super_users[server.id].append(user.id)
            else:
                super_users[server.id] = [user.id]

            await ctx.send(f"{user} is now a super user")
        
        else:
            await ctx.reply("You are not a super user")

    @commands.command(name="deop", description="Withdraws user's permission to block others")
    async def deop(self,ctx,user: discord.User):
        server = ctx.message.guild

        if server.id not in super_users:
            super_users[server.id] = []

        if user.id not in super_users[server.id]:
            await ctx.send(f"{user} isn't a super user")

        if ctx.message.author.id == 304651000889737217 or ctx.message.author in super_users:
            server = ctx.message.guild

            for i in range(len(super_users[server.id])):

                if super_users[server.id][i] == user.id:
                    super_users[server.id][i] = None
                    await ctx.send(f"Deopped {user}")
                
        else:
            await ctx.reply("You are not a super user")



def setup(client):
        client.add_cog(administrative(client))