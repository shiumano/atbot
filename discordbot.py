import discord, importlib, os
import botsystem

try:
    token = os.environ['DISCORD_BOT_TOKEN']
    local = False
except KeyError:
    with open('/storage/emulated/0/DiscordBOT/token') as file:
        token = file.read()
    local = True

client = discord.Client()
botsystem.set_client()

@client.event
async def on_ready():
    print(f'{client.user}としてログインしました')

@client.event
async def on_message(message):
    if message.content == '@reload' and local:
        try:
            importlib.reload(botsystem)
            await message.channel.send('Reloaded.')
        except Exception as e:
            await message.channel.send(f'Not reloaded : {e}')
    await botsystem.commands(message)
    await botsystem.zatzudan(message)
client.run(token)
