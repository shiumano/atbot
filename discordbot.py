import discord, time, importlib, os, traceback
import botsystem, restart

local = False
pf = '@'
try:
    token = os.environ['DISCORD_BOT_TOKEN']
except KeyError:
    with open('/storage/emulated/0/token') as file:
        token = file.read()
    local = True

client = discord.Client()
botsystem.setting(client,pf)

@client.event
async def on_ready():
    print(f'{client.user}としてログインしました')

@client.event
async def on_message(message):
    if message.author.discriminator == '0000':
        return

    if message.content == f'{pf}reload' and local:
        try:
            importlib.reload(botsystem)
            await message.channel.send('Reloaded.')
        except Exception as e:
            await message.channel.send(f'Not reloaded : {e}')

    await botsystem.commands(message)
    await botsystem.zatzudan(message)

@client.event
async def on_raw_reaction_add(payload):
    message = await client.get_channel(payload.channel_id).fetch_message(payload.message_id)
    emoji = str(payload.emoji)

    if emoji == '🔄':
        await on_message(message)

@client.event
async def on_error(event,*args,**kwargs):
    print(f'\n{time.ctime().split(" ")[-2]}\nIgnoring exception in {event}')
    if event == 'on_message':
        message = args[0]
        if type(message.channel) == discord.TextChannel:
            channel = message.channel.name
        else:
            channel = message.channel.recipient.name+"'s DMChannel"
        print(f'at : {channel}\nfor : {message.content}')
    elif event == 'on_raw_reaction_add':
        print(f'emoji : {args[0].emoji}')

    traceback.print_exc()

try:
    client.run(token)
except Exception as e:
    print('ログインできませんでした。: ',e)
    restart.restart_program()
