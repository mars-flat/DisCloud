import discord
import json
import asyncio
import os

# database directory

db_directory = f"{os.path.dirname(os.getcwd())}\\DisCloud"

# Globally accessible data for all modules to access

# Bot
client = None

'''

Live data from the database
Format:

{ 
    Guild id: { "links": {name: link, ...}, "whitelist": [], "blacklist": [] }, 
    Guild id: { "links": {}, "whitelist": [], "blacklist": [] }
    ...
}

'''

data = {}

'''

stores list pages in batches of 20
Format:

{ 
    Guild id: {
        "links": [[batch], [batch]...], 
        "whitelist": [[batch], [batch]...],
        "blacklist": [[batch], [batch]...],
    }
    
    Guild id: {
        "links": [[batch], [batch]...], 
        "whitelist": [[batch], [batch]...],
        "blacklist": [[batch], [batch]...],
    }
    ...
}

'''

pages = {}

'''

Stores active lists called by guild members
This includes:

link entry lists,
whitelist lists,
blacklist lists

Format:

{ 
    Guild id: {
        "links_lists": [[page, message], [page, message]...], 
        "whitelist_lists": [[page, message], [page, message]...], 
        "blacklist_lists": [[page, message], [page, message]...] 
    }
    Guild id: {
        "links_lists": [[page, message], [page, message]...], 
        "whitelist_lists": [[page, message], [page, message]...], 
        "blacklist_lists": [[page, message], [page, message]...] 
    }
    ...
}

Each category of lists will track the last five active lists of its kind per guild.

'''

active_lists = {}


# Coroutine to track the last 5 lists.


async def track_lists():
    await client.wait_until_ready()
    while not client.is_closed():
        local = active_lists.copy()
        for guild_id in local:
            for list_type in local[guild_id]:
                for element in local[guild_id][list_type]:
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

                            max_page = len(pages[str(message.guild.id)][list_type.replace("_lists", "")])

                            if current_page < 0:
                                current_page = max_page - 1
                            if current_page >= max_page:
                                current_page = 0

                            element[0] = current_page
                            element[1] = message

                            text = "```"
                            for entry in pages[str(message.guild.id)][list_type.replace("_lists", "")][current_page]:
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
                            await element[1].add_reaction("??????")
                            await element[1].add_reaction("??????")

        await asyncio.sleep(3)


# Updates the database with the live dictionary.


async def update_data():
    await client.wait_until_ready()
    while not client.is_closed():
        with open(f"{db_directory}\\db.json", "w") as out:
            json.dump(data, out)

        await asyncio.sleep(5)


# Allocates a section in the database for new servers.


async def setup_guilds():
    await client.wait_until_ready()
    while not client.is_closed():
        for guild in client.guilds:
            if str(guild.id) not in data:
                data[str(guild.id)] = {"links": {}, "whitelist": [], "blacklist": []}

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

    with open(f"{db_directory}\\db.json", "r") as f:
        global data
        data = json.load(f)

    if client is not None:
        for task in tasks:
            client.loop.create_task(task())

