from . import responder


async def permission_denied(message):
    return await responder.respond(
        message.channel,
        f"You don't have the permission to run this command.",
        False
    )


async def error_occurred(message):
    return await responder.respond(
        message.channel,
        f"An error occurred trying to add to the database.",
        False
    )


async def bad_arguments(message, **kwargs):
    intended = kwargs.get("intended") if "intended" in kwargs else None
    return await responder.respond(
        message.channel,
        f"The command did not give the arguments in the form `{intended}`",
        False
    )