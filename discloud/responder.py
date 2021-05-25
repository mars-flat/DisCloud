async def respond(recipient, message, embed=True, **kwargs):
    delete_after = kwargs.get("delete_after") if "delete_after" in kwargs else None
    if not embed:
        if delete_after is None:
            destination = await recipient.send(message)
            return destination
        return await recipient.send(message, delete_after=delete_after)

    destination = await recipient.send(embed=message)
    return destination
