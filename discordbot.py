import discord, importlib, os
import botsystem

try:
    token = os.environ['DISCORD_BOT_TOKEN']
    pf = '@'
except KeyError:
    with open('/storage/emulated/0/token') as file:
        token = file.read()
    pf = 'Test@'

client = discord.Client()
botsystem.set_client()

@client.event
async def on_ready():
    print(f'{client.user}としてログインしました')

@client.event
async def on_message(message):
    if message.author.discriminator == '0000':
        return

    if message.content == f'{pf}reload' and pf == 'Test@':
        try:
            importlib.reload(botsystem)
            await message.channel.send('Reloaded.')
        except Exception as e:
            await message.channel.send(f'Not reloaded : {e}')

    await botsystem.commands(message,pf)
    await botsystem.zatzudan(message)
client.run(token)
