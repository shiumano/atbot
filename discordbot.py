import discord,random,os
token=os.environ['DISCORD_BOT_TOKEN']
client=discord.Client()
ch=0
@client.event
async def on_ready():
 print('hello')
@client.event
async def on_message(m):
 global ch
 if m.channel.id==ch:
  while 1:
   await m.channel.send(random.choice(('スマホのスペックってそんなに低いっけ？','スマホを見下すなクソ野郎共','パソコン買う金あればパソコン使うよ')))
   if random.randint(1,10000)==1:
    await m.channel.send('@everyone')
 if m.content=='@spam':
  m.channel.send('Are you sure?')
  ch=m.channel.id
client.run(token)
