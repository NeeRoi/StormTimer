import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime, timedelta

class RandomStormCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_message_time = None
        self.bot.loop.create_task(self.initialize_last_message_time())

async def initialize_last_message_time(self):
    for guild in self.bot.guilds:
        for channel in guild.text_channels:
            if channel.name == 'your-channel-name':
                async for message in channel.history(limit=100):
                    for embed in message.embeds:
                        if 'has purchased Random Storm for $200,000.Their in-game ID is' in embed.description:
                            self.last_message_time = message.created_at
                            return

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.name == 'your-channel-name':
            for embed in message.embeds:
                if 'has purchased Random Storm for $200,000.Their in-game ID is' in embed.description:
                    self.last_message_time = message.created_at
                    next_storm_time, time_difference = self.calculate_next_randomstorm()
                    if time_difference > timedelta(hours=5):
                        embed = discord.Embed(title="Random Storm Update", description=f"Der letzte Random Storm war um {self.last_message_time}. Random Storm hat keinen Kuhldown.", color=0x00ff00) # Green embed
                        await message.channel.send(embed=embed)
                    else:
                        embed = discord.Embed(title="Random Storm Update", description=f"Der letzte Random Storm war um {self.last_message_time}. Der Nächste Random Storm ist um {next_storm_time} wieder verfügbar.", color=0xff0000) # Red embed
                        await message.channel.send(embed=embed)

    @commands.command(name="stormtimer", description="Get the time until the next randomstorm")
    async def stormtimer(self, ctx: commands.Context):
        #Calculate the time until the next randomstorm
        next_storm_time, time_difference = self.calculate_next_randomstorm()
        if time_difference > timedelta(hours=5):
            embed = discord.Embed(title="Random Storm Update", description=f"Der letzte Random Storm war um {self.last_message_time}. Random Storm hat keinen Kuhldown.", color=0x00ff00) # Green embed
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="Random Storm Update", description=f"Der letzte Random Storm war um {self.last_message_time}. Der Nächste Random Storm ist um {next_storm_time} wieder verfügbar.", color=0xff0000) # Red embed
            await ctx.send(embed=embed)

    def calculate_next_randomstorm(self):
        now = datetime.now()
        time_difference = now - self.last_message_time
        next_storm_time = self.last_message_time + timedelta(hours=5)
        return next_storm_time, time_difference

def setup(bot):
    bot.add_cog(RandomStormCog(bot))
