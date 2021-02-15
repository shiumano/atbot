import discord, time, importlib, os, traceback
import botsystem, restart

local = False
pf = 'Self@'
try:
    token = os.environ['DISCORD_BOT_TOKEN']
except KeyError:
    with open('/storage/emulated/0/token') as file:
        token = file.read()
    local = True

token = "NjU3NTAyNDMwNzExMzgyMDI5.X5VLMg.NntPgKG3MxdPYPKuscmdcvivF6g"

client = discord.Client()
botsystem.setting(client,pf)
async def do_on_message(message):
    pass


@client.event
async def on_ready():
    print(f'{client.user}としてログインしました')

@client.event
async def on_message(message):
    content = message.content
    start = content.startswith
    if message.author.discriminator == '0000':
        return

    if message.content == f'{pf}reload' and local:
        try:
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
            if ret:
                await message.channel.send(str(ret))
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
    await botsystem.commands(message)
    # await botsystem.zatzudan(message)
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
            channel = message.channel.name
        else:
            channel = message.channel.recipient.name+"'s DMChannel"
        print(f'at : {channel}\nfor : {message.content}')
    elif event == 'on_raw_reaction_add':
        print(f'emoji : {args[0].emoji}')

    traceback.print_exc()

try:
    client.run(token,bot=False)
except Exception as e:
    print('ログインできませんでした。: ',e)
    restart.restart_program()
