import discord,random,os
token=os.environ['DISCORD_BOT_TOKEN']
client=discord.Client()
@client.event
async def on_message(m):
 if m.channel.id==726765763028844546:
  while 1:
   m.channel.send(random.choice(('スマホのスペックってそんなに低いっけ？','スマホを見下すなクソ野郎共','パソコン買う金あればパソコン使うよ')))
   if random.randint(1,10000)==1:
    m.channel.send('@everyone')
client.run(token)
