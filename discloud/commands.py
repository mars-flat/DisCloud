from . import active_data, whitelist, responder, files, utils
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
    embed.add_field(
        name="~open [filename 1] (filename 2) (filename 3)",
        value="Opens files with given names.",
        inline=False)
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
    "links": files.list_links,
    "whitelist": whitelist.list_whitelist
}


async def filter_lists(message):
    parsed = utils.tokenize(message.content, " ")
    list_type = parsed[1] if 2 <= len(parsed) <= 3 else "links"

    if list_type in list_types:
        return await list_types[list_type](message)
    return await responder.respond(
        message.channel,
        f"That is not a valid list type.",
        False
    )


async def open_file(message):
    parsed = utils.tokenize(message.content.replace("~open ", ""), " ")
    counter = 0
    for token in parsed:
        counter += 1
        if token in active_data.data[str(message.guild.id)]["links"]:
            if counter > 3:
                return await responder.respond(
                    message.channel,
                    f"You may only load 3 entries at once.",
                    False,
                    delete_after=5
                )
            await responder.respond(
                message.channel,
                active_data.data[str(message.guild.id)]["links"][token],
                False
            )


commands = {
    "~help": info,

    "~list": filter_lists,

    "~open": open_file,

    # requires whitelist
    "~add": files.add_link,

    # requires whitelist
    "~remove": files.remove_link,

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

    for key in commands:
        if key in command.lower():
            return await commands[key](message)
