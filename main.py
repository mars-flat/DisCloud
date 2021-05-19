from discloud import active_data, commands
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

    await commands.fire_command(message)

active_data.init(bot)
bot.run(settings.token)

