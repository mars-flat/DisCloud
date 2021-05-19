from active_data import *

import responder


async def info(message):
    embed = discord.Embed(
        title="Help",
        description=f"This is a template for your very own DisCloud. "
                    f"Feel free to customize it however you want! "
                    f"If you ever get stuck you can check out the "
                    f"documentation at <PLACEHOLDER>",
        colour=discord.Colour.green(),
    )

    embed.set_author(
        name="DisCloud", icon_url=client.user.avatar_url
    )

    embed.add_field(name="Commands:", value="\u200b", inline=False)
    embed.add_field(name="`~help`", value="Displays this message.", inline=False)
    embed.add_field(name="`~add [name] [link]`", value="Adds an entry.", inline=False)
    embed.add_field(name="`~remove [name]`", value="Removes an entry.", inline=False)
    embed.add_field(name="`~list (page)`", value=f"Lists entries. Page specification "
                                                 f"is optional.", inline=False)
    embed.add_field(name="`~whitelist [user]`", value=f"Whitelists user for add/remove "
                                                      f"abilities.", inline=False)
    embed.add_field(name="`~unwhitelist [user]`", value="Un-whitelists the user.", inline=False)

    return await responder.respond(message.channel, embed)


async def list_media():
    pass


async def add_media():
    pass


async def remove_media():
    pass


async def check_media(message):
    server_emotes.add(emote.name for emote in message.guild.emojis)
    if message.content.count(":") >= 2:
        count = 0
        for token in message.content.split(":"):
            if token in data["data"]["media"] and token not in server_emotes:
                count += 1
                if count > 3:
                    return await responder.respond(
                        message.channel,
                        f"You may only load 3 entries at once.",
                        False
                    )
                await responder.respond(
                    message.channel,
                    data["data"]["media"][token],
                    False
                )
        return


commands = {
    "~help": info,

    "~list": list_media,

    # requires whitelist
    "~add": add_media,

    # requires whitelist
    "~remove": remove_media,


    # requires administrator
    # "~whitelist": whitelist.whitelist,

    # requires administrator
    # "~unwhitelist": whitelist.unwhitelist,


}


# Function to fire commands if a message has the correct command.
# Called on every message sent.


async def fire_command(message):
    if client is None:
        return

    command = message.content

    check_media(message)

    for key in commands:
        if key in command.lower():
            return await commands[key](message)
