import discord, asyncio, time, importlib, os, traceback
import botsystem, restart

local = False
prefix = 'Test@'
prefixes = {}

try:
    token = os.environ['DISCORD_BOT_TOKEN']
except KeyError:
    # with open('/data/data/com.termux/files/home/token') as file:
    with open('/storage/emulated/0/token') as file:
        token = file.read()
    local = True

#intents = discord.Intents.all()

client = discord.Client() #intents=intents)
botsystem.setting(client)

async def do_on_message(message):
    pass

@client.event
async def on_ready():
    print(f'{client.user}としてログインしました')

@client.event
async def on_message(message):
    if type(message.channel) == discord.TextChannel:
        pf = prefixes.get(message.guild.id)
    else:
        pf = prefixes.get(message.channel.id)
    if pf is None:
        pf = prefix
    content = message.content
    start = content.startswith
    if message.author.discriminator == '0000':
        return

    if message.content == f'{pf}reload' and local:
        try:
            await botsystem.aionet.close()
            importlib.reload(botsystem)
            await message.channel.send('Reloaded.')
        except Exception as e:
            await message.channel.send(f'Not reloaded : {e}')

    if start(f'{pf}run') and message.author.id == 728289161563340881:
        content = content[4+len(pf):]
        run = ('global func\n'
                'async def func(message):\n')
        for line in content.splitlines():
            run += f'    {line}\n'
        try:
            exec(run)
            ret = await func(message)
            await message.channel.send(ret.__class__.__repr__(ret))
        except Exception as e:
             tb_now = e.__traceback__
             send = '--Error--\n'
             back = 0
             while tb_now:
                 line = tb_now.tb_lineno
                 filename = tb_now.tb_frame.f_code.co_filename
                 if filename == '<string>':
                     code = run.splitlines()[line-1]
                 else:
                     with open(filename) as f:
                         code = f.readlines()[line-1]
                 send += f'file "{filename}" line {line}\n```py\n{code}\n```'
                 tb_now = tb_now.tb_next
             send += f'{e.__class__.__name__}: {e}'
             await message.channel.send(send)

    if message.content.startswith(pf):
        await botsystem.commands(message,pf)
    await botsystem.zatzudan(message,pf)
    await do_on_message(message)

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
            channel = f'{message.channel.guild} / {message.channel.name} ({message.channel.id})'
        else:
            channel = message.channel.recipient.name+f"'s DMChannel ({message.channel.id})"
        print(f'at : {channel}\nfor : {message.content}')
    elif event == 'on_raw_reaction_add':
        print(f'emoji : {args[0].emoji}')

    traceback.print_exc()

try:
    client.run(token)
    asyncio.run(botsystem.aionet.close())
except Exception as e:
    print('ログインできませんでした。: ',e)
    asyncio.run(botsystem.aionet.close())
    restart.restart_program()
