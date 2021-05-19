from . import active_data
from . import responder


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

async def list_whitelist():
    pass