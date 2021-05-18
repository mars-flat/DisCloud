from discloud import *

import discord
import settings

bot = discord.Client()


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="DisCloud"))
    print("Initialized " + bot.user.name)


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    pass

bot.run(settings.token)
