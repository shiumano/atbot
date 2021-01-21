import discord
import asyncio, json
client = discord.Client(max_messages=10000)
try:
    token = os.environ['DISCORD_BOT_TOKEN']
except KeyError:
    with open('/storage/emulated/0/token') as file:
        token = file.read()
@client.event
async def on_ready():
    print(f'Login as {client.user}')

@client.event
async def on_message(message):
    if message.content.startswith('@run') and message.author.id == 728289161563340881:
        run = 'global func\nasync def func(message):\n'
        for line in message.content[5:].splitlines():
            run += '    '+line+'\n'
        try:
            exec(run)
            ret = await func(message)
            if ret:
                await message.channel.send(ret)
        except Exception as e:
            await message.channel.send(type(e).__name__+': '+str(e))

@client.event
async def on_reaction_add(reaction,user):
    message = reaction.message
    pass

client.run(token)
