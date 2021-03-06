from mcstatus import MinecraftServer as mcserver
import discord
import asyncio
from datetime import datetime

# Config Vars -------------------------------------------------------------------------------------------------------------------
# set public_ip to the ip people will connect to, if this is hosted on the same server it'll just use whatever localhost will be
ip = "SERVER IP HERE"
public_ip = ip
modpack_name = "All the Mods 3 Remix"
status_interval = 10
channel_id = "CHANNEL ID HERE"
botToken = "BOT TOKEN HERE"
# -------------------------------------------------------------------------------------------------------------------------------

server = mcserver.lookup(ip)
status = server.status()
client = discord.Client()

def get_status():
    server = mcserver.lookup(ip)
    status = server.status()
    print(f"[{datetime.now().time()}] {status.players.online}/{status.players.max} Players online | {public_ip} | {modpack_name}")
    return discord.Game(f"{status.players.online}/{status.players.max} Players online | {public_ip} | {modpack_name}")

def get_players():
    try:
        query = server.query()
    except Exception:
        return "Error retrieving server query, enable queries in server.properties"
    return query.players.names

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('mcbot plist'):
        print(f"[{datetime.now().time()}] Request for player list by: " + message.author.display_name)
        await client.wait_until_ready()
        plist = get_players()
        channel = client.get_channel(int(channel_id))

        str_plist = "Players Online:\n```\n"
        for p in plist: str_plist += p + "\n"
        str_plist += "```"
        if plist == []: str_plist = "No one is online currently"
        await channel.send(str_plist)

@client.event
async def on_ready():
    print('------------')
    print(f'Logged in as "{client.user.name}"')
    print('id: ', client.user.id)
    print('------------')
    # check server status on N second intervals
    client.loop.create_task(status_task(status_interval))

async def status_task(n):
    while True:
        await client.change_presence(status=discord.Status.online, activity=get_status())
        await asyncio.sleep(n)
        await client.change_presence(status=discord.Status.online, activity=get_status())
        await asyncio.sleep(n)

client.run(botToken)
