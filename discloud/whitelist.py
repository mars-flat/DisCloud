import discord
from . import active_data, responder


async def whitelist(message):
    if not message.author.guild_permissions.administrator:
        return await responder.respond(
            message.channel,
            f"You don't have the permission to run this command.",
            False
        )

    parsed = message.content.split()
    if len(parsed) == 2:
        a = parsed[1]
        a = a.replace("<", "")
        a = a.replace(">", "")
        a = a.replace("!", "")
        a = a.replace("@", "")

        try:

            if a not in active_data.data[str(message.guild.id)]["whitelist"]:
                active_data.data[str(message.guild.id)]["whitelist"].append(a)
                return await responder.respond(
                    message.channel,
                    f"Successfully added `{a}` to the whitelist.",
                    False
                )
            else:
                return await responder.respond(
                    message.channel,
                    f"`{a}` is already whitelisted.",
                    False
                )

        except Exception:
            return await responder.respond(
                message.channel,
                f"An error occurred trying to add to the database.",
                False
            )

    else:
        return await responder.respond(
            message.channel,
            f"The command did not give the arguments in the form `~whitelist [user]`",
            False
        )


# un-whitelists users.


async def unwhitelist(message):
    if not message.author.guild_permissions.administrator:
        return await responder.respond(
            message.channel,
            f"You don't have the permission to run this command.",
            False
        )

    parsed = message.content.split()
    if len(parsed) == 2:
        a = parsed[1]
        a = a.replace("<", "")
        a = a.replace(">", "")
        a = a.replace("!", "")
        a = a.replace("@", "")

        try:
            if a in active_data.data[str(message.guild.id)]["whitelist"]:
                active_data.data[str(message.guild.id)]["whitelist"].remove(a)
                return await responder.respond(
                    message.channel,
                    f"Successfully removed `{a}` from the whitelist.",
                    False
                )
            else:
                return await responder.respond(
                    message.channel,
                    f"`{a}` is not in the whitelist.",
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
            f"The command did not give the arguments in the form `~unwhitelist [user]`",
            False
        )


async def list_whitelist(message):
    if str(message.guild.id) not in active_data.pages:
        active_data.pages[str(message.guild.id)] = {
            "links": [],
            "whitelist": [],
            "blacklist": []
        }

    active_data.pages[str(message.guild.id)]["whitelist"].clear()
    page = []
    counter = 1
    for entry in active_data.data[str(message.guild.id)]["whitelist"]:
        counter += 1
        page.append(f"{entry}")
        if counter > 20:
            active_data.pages[str(message.guild.id)]["whitelist"].append(page.copy())
            page.clear()
            counter = 1

    if len(page) > 0:
        active_data.pages[str(message.guild.id)]["whitelist"].append(page)

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
            f"The command did not give the arguments in the form ~list (page)",
            False
        )

    num_pages = len(active_data.pages[str(message.guild.id)]["whitelist"])
    if num_pages == 0:
        return await responder.respond(
            message.channel,
            f"There are no entries in the list.",
            False
        )

    if queried_page < 0 or queried_page >= len(active_data.pages[str(message.guild.id)]["whitelist"]):
        return await responder.respond(
            message.channel,
            f"The page {queried_page + 1} is not valid. "
            f"Please use a number between {1} and {num_pages}",
            False
        )
    else:
        text = "```"
        for entry in active_data.pages[str(message.guild.id)]["whitelist"][queried_page]:
            text += entry + "\n"

        text += "```"

        embed = discord.Embed(
            title="Media List",
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

        if len(active_data.active_lists[str(message.guild.id)]["whitelist_lists"]) + 1 > 5:
            active_data.active_lists[str(message.guild.id)]["whitelist_lists"].pop(0)

        active_data.active_lists[str(message.guild.id)]["whitelist_lists"].append([0, sent_message])

        return
