from . import responder


async def permission_denied(message):
    return await responder.respond(
        message.channel,
        f"You don't have the permission to run this command.",
        False,
        delete_after=5
    )


async def error_occurred(message):
    return await responder.respond(
        message.channel,
        f"An error occurred trying to add to the database.",
        False,
        delete_after=5
    )


async def bad_arguments(message, **kwargs):
    intended = kwargs.get("intended") if "intended" in kwargs else None
    return await responder.respond(
        message.channel,
        f"The command did not give the arguments in the form `{intended}`",
        False,
        delete_after=5
    )


def tokenize(string, exp):
    return [token for token in string.split(exp)]
