import discord, importlib, os
import botsystem, restart

local = False
try:
    token = os.environ['DISCORD_BOT_TOKEN']
    pf = '@'
except KeyError:
    with open('/storage/emulated/0/token') as file:
        token = file.read()
    pf = 'Test@'
    local = True

# heroku時間切れ終わったので
#pf = '@'
#local = True

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
try:
    client.run(token)
except Exception as e:
    print('ログインできませんでした。',e)
    restart.restart_program()
