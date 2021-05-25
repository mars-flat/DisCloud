import discord

from . import active_data, whitelist, responder, utils


# Adds the media link to a specified entry name.

async def add_link(message):
    guild_data = active_data.data[str(message.guild.id)]

    if str(message.author.id) not in guild_data["whitelist"]:
        return await utils.permission_denied(message)

    parsed = message.content.split()

    attachment = message.attachments[0] if len(message.attachments) > 0 else None

    if len(parsed) == 3:

        if parsed[1] in guild_data["links"]:
            return await responder.respond(
                message.channel,
                f"An entry with this name already exists.",
                False
            )

        try:
            guild_data["links"][parsed[1]] = str(parsed[2])
            return await responder.respond(
                message.channel,
                f"Successfully added `{parsed[1]}`.",
                False
            )

        except AttributeError:
            return await utils.error_occurred(message)

    elif len(parsed) == 2 and attachment is not None:

        if parsed[1] in guild_data["links"]:
            return await responder.respond(
                message.channel,
                f"An entry with this name already exists.",
                False
            )

        try:
            guild_data["links"][parsed[1]] = str(attachment.url)
            return await responder.respond(
                message.channel,
                f"Successfully added `{parsed[1]}`.",
                False
            )

        except AttributeError:
            return await utils.error_occurred(message)

    else:
        return await utils.bad_arguments(message, intended="~add [name] [link]")


# Removes the specified entry name.


async def remove_link(message):
    guild_data = active_data.data[str(message.guild.id)]

    if str(message.author.id) not in guild_data["whitelist"]:
        return await responder.respond(
            message.channel,
            f"You don't have the permission to run this command.",
            False
        )

    parsed = message.content.split()
    if len(parsed) == 2:
        try:

            if parsed[1] in guild_data["links"]:
                guild_data["links"].pop(parsed[1], None)
                return await responder.respond(
                    message.channel,
                    f"Successfully removed `{parsed[1]}`.",
                    False
                )
            else:
                return await responder.respond(
                    message.channel,
                    f"An entry with this name does not exist.",
                    False
                )

        except Exception:
            return await responder.respond(
                message.channel,
                f"An error occurred trying to remove from the database.",
                False
            )

    else:
        return await responder.respond(
            message.channel,
            f"The command did not give the arguments in the form ~remove [name]",
            False
        )


async def list_links(message):
    if str(message.guild.id) not in active_data.pages:
        active_data.pages[str(message.guild.id)] = {
            "links": [],
            "whitelist": [],
            "blacklist": []
        }

    guild_pages = active_data.pages[str(message.guild.id)]

    guild_pages["links"].clear()
    page = []
    counter = 1
    for entry in active_data.data[str(message.guild.id)]["links"]:
        counter += 1
        page.append(f":{entry}:")
        if counter > 20:
            guild_pages["links"].append(page.copy())

            page.clear()
            counter = 1

    if len(page) > 0:
        guild_pages["links"].append(page)

    queried_page = 0
    parsed = message.content.split()
    if len(parsed) == 2:
        pass
    elif len(parsed) == 3:
        try:
            queried_page = int(parsed[2]) - 1
        except Exception:
            return await responder.respond(
                message.channel,
                f"This page is invalid.",
                False
            )
    else:
        return await responder.respond(
            message.channel,
            f"The command did not give the arguments in the form ~list [type] (page)",
            False
        )

    num_pages = len(guild_pages["links"])
    if num_pages == 0:
        return await responder.respond(
            message.channel,
            f"There are no entries in the list.",
            False
        )

    if queried_page < 0 or queried_page >= num_pages:
        return await responder.respond(
            message.channel,
            f"The page {queried_page + 1} is not valid. "
            f"Please use a number between {1} and {num_pages}",
            False
        )
    else:
        text = "```"
        for entry in guild_pages["links"][queried_page]:
            text += entry + "\n"

        text += "```"

        embed = discord.Embed(
            title="Links",
            description=text,
            colour=discord.Colour.green(),
        )

        embed.set_author(
            name="DisCloud", icon_url=active_data.client.user.avatar_url
        )

        embed.set_footer(text=f"Displaying page {queried_page + 1} of {num_pages}")

        sent_message = await responder.respond(
            message.channel,
            embed
        )

        await sent_message.add_reaction("⬅️")
        await sent_message.add_reaction("➡️")

        if str(message.guild.id) not in active_data.active_lists:
            active_data.active_lists[str(message.guild.id)] = {
                "links_lists": [],
                "whitelist_lists": [],
                "blacklist_lists": []
            }

        if len(active_data.active_lists[str(message.guild.id)]["links_lists"]) + 1 > 5:
            active_data.active_lists[str(message.guild.id)]["links_lists"].pop(0)

        active_data.active_lists[str(message.guild.id)]["links_lists"].append([0, sent_message])
        return
