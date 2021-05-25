from . import active_data, whitelist, responder, links
import discord


async def info(message):
    embed = discord.Embed(
        title="Help",
        description=f"This is a template for your very own DisCloud. "
                    f"Feel free to customize it however you want! "
                    f"If you ever get stuck you can check ~out the "
                    f"documentation at <PLACEHOLDER>",
        colour=discord.Colour.green(),
    )

    embed.set_author(
        name="DisCloud", icon_url=active_data.client.user.avatar_url
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


list_types = {
    "links": links.list_links,
    "whitelist": whitelist.list_whitelist
}


async def filter_lists(message):
    parsed = message.content.split()
    list_type = parsed[1] if 2 <= len(parsed) <= 3 else "links"
    if list_type in list_types:
        return await list_types[list_type](message)
    return await responder.respond(
        message.channel,
        f"That is not a valid list type.",
        False
    )


async def check_links(message):
    server_emotes = set(emote.name for emote in message.guild.emojis)
    if message.content.count(":") >= 2:
        count = 0
        for token in message.content.split(":"):
            if token in active_data.data[str(message.guild.id)]["links"] and token not in server_emotes:
                count += 1
                if count > 3:
                    return await responder.respond(
                        message.channel,
                        f"You may only load 3 entries at once.",
                        False
                    )
                await responder.respond(
                    message.channel,
                    active_data.data[str(message.guild.id)]["links"][token],
                    False
                )
        return


commands = {
    "~help": info,

    "~list": filter_lists,

    # requires whitelist
    "~add": links.add_link,

    # requires whitelist
    "~remove": links.remove_link,

    # requires administrator
    "~whitelist": whitelist.whitelist,

    # requires administrator
    "~unwhitelist": whitelist.unwhitelist,

}


# Function to fire commands if a message has the correct command.
# Called on every message sent.


async def fire_command(message):
    if active_data.client is None:
        return

    command = message.content
    await check_links(message)

    for key in commands:
        if key in command.lower():
            return await commands[key](message)
