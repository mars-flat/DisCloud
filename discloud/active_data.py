import discord
import json
import asyncio
import os

# database directory

db_directory = os.path.dirname(os.getcwd())

# Globally accessible data for all modules to access

# Bot
client = None

'''

Live data from the database
Format:

{ 
    [Guild id]: { "links": {}, "whitelist": [], "blacklist": [] }, 
    [Guild id]: { "links": {}, "whitelist": [], "blacklist": [] }
    ...
}

'''

data = {}

'''

stores list pages in batches of 20
Format:

{ 
    "links": [[batch], [batch]...], 
    "whitelist": [[batch], [batch]...],
    "blacklist": [[batch], [batch]...],

}

'''

pages = {
    "links": [],
    "whitelist": [],
    "blacklist": []
}

'''

Stores active lists called by guild members
This includes:

link entry lists,
whitelist lists,
blacklist lists

Format:

{ 
    "links_lists": [[page, message], [page, message]...], 
    "whitelist_lists": [[page, message], [page, message]...], 
    "blacklist_lists": [[page, message], [page, message]...] 
}

Each category of lists will track the last five active lists of its kind.

'''

active_lists = {
    "links_lists": [],
    "whitelist_lists": [],
    "blacklist_lists": []
}

'''

stores server emotes as a set
Prevents conflicts with in-server emotes

'''

server_emotes = set()


# Coroutine to track the last 5 lists.


async def track_lists():
    await client.wait_until_ready()
    while not client.is_closed():
        local = active_lists.copy()
        for list_type in local:
            for element in local[list_type]:

                current_page = element[0]
                message = element[1]

                # Checks if the message containing the list has been deleted

                try:
                    message = await message.channel.fetch_message(message.id)

                except Exception:

                    # Removes the entry from the list

                    if element in active_lists[list_type]:
                        active_lists[list_type].remove(element)
                    continue

                if len(message.reactions) >= 2:
                    previous_page = message.reactions[0]
                    next_page = message.reactions[1]

                    if previous_page.count > 1 or next_page.count > 1:
                        if previous_page.count > 1:
                            current_page -= 1
                        if next_page.count > 1:
                            current_page += 1

                        max_page = len(pages[list_type.replace("_lists", "")])

                        if current_page < 0:
                            current_page = max_page - 1
                        if current_page >= max_page:
                            current_page = 0

                        element[0] = current_page
                        element[1] = message

                        text = "```"
                        for entry in pages[list_type.replace("_lists", "")][current_page]:
                            text += entry + "\n"

                        text += "```"

                        embed = discord.Embed(
                            title="Media List",
                            description=text,
                            colour=discord.Colour.green(),
                        )

                        embed.set_author(
                            name="DisCloud", icon_url=client.user.avatar_url
                        )

                        embed.set_footer(text=f"Displaying page {current_page + 1} of {max_page}")

                        await element[1].clear_reactions()
                        await element[1].edit(embed=embed)
                        await element[1].add_reaction("⬅️")
                        await element[1].add_reaction("➡️")

        await asyncio.sleep(3)


# Updates the database with the live dictionary.


async def update_data():
    await client.wait_until_ready()
    while not client.is_closed():
        print(data)
        with open(f"{db_directory}/db.json", "w") as out:
            json.dump(data, out)

        await asyncio.sleep(10)


# Allocates a section in the database for new servers.


async def setup_guilds():
    await client.wait_until_ready()
    while not client.is_closed():
        for guild in client.guilds:
            if guild.id not in data:
                data[guild.id] = {"links": {}, "whitelist": [], "blacklist": []}

        await asyncio.sleep(10)


# list of coroutine tasks


tasks = [
    update_data,
    track_lists,
    setup_guilds
]


# Initialization for database and coroutines.


def init(who):
    global client
    client = who

    with open(f"{db_directory}/db.json", "r") as f:
        global data
        data = json.load(f)

    if client is not None:
        for task in tasks:
            client.loop.create_task(task())

