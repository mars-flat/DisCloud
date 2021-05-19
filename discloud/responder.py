async def respond(recipient, message, embed=True):
    if not embed:
        destination = await recipient.send(message)
        return destination

    destination = await recipient.send(embed=message)
    return destination
