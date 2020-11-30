import __main__ as main
import discord, asyncio, json, random, subprocess, time, timedelta
import multiprocessing as mp

owner = 728289161563340881

ping = []
p_test = []

def set_client():
    global client
    client = main.client

#便利かなぁと作った関数
def p_check(member,channel,permission,level=None):
    if type(channel) == discord.TextChannel:
        if member.id == owner or member.permissions_in(channel) >= permission:
            return True

        with open('user_data.json') as file:
            user_dict = json.loads(file.read())
        if level:
            return leveling(member,chanel,level*-1)
    return False

def leveling(user,ch,level):
    bool = False
    write = False
    if type(ch) == discord.DMChannel:
        return False
    with open('user_data.json') as file:
        user_dict = json.loads(file.read())
    a = user_dict.get(str(user.id))
    if a:
        b = a[0].get(str(ch.category_id))
        if b:
            if a[0][str(ch.category_id)] > level:
                (user_dict[str(user.id)]
                          [0]
                          [str(ch.category_id)]) += level
                bool = True
                write = True
        if level > 0:
            if user_dict.get(str(user.id)):
                (user_dict[str(user.id)]
                          [0]
                          [str(ch.category_id)]) = level
            else:
                user_dict[str(user.id)] = [{str(ch.category_id):level},None]
            write = True
    if write:
        with open('user_data.json',mode='w') as file:
            user_json = json.dumps(user_dict,ensure_ascii=False,indent=2)
            file.write(user_json)
    return bool

def greet(time,a,b,c,d,e,f,g):
    if time < 4:
       message = a
    elif time < 7:
       message = b
    elif time < 10:
       message = c
    elif time < 12:
       message = d
    elif time < 17:
       message = e
    elif time < 20:
       message = f
    else:
       message = g
    return message

async def no_embed(message):
    global p_test
    if message in p_test:
        await message.channel.send('謎だぁ')
        dev = await client.fetch_user(owner)
        await dev.send(f'謎現象：{message.content}')
        p_test.remove(message)
    g_owner = await client.fetch_user(message.guild.owner_id)
    try:
        await message.channel.send('おや？これは埋め込みリンク使えないパターンか？？')
    except discord.errors.Forbidden:
        pass
    try:
        await message.channel.send(embed=discord.Embed(description='テストｫｫｫ',colour=0x00bfff))
        await message.channel.send('いや、使えるなぁ………。一応もう一度試そう。')
        test = await message.channel.send(message.content)
        p_test.append(test)
    except discord.errors.Forbidden:
        await message.channel.send(f'おい{g_owner}埋め込み送れないじゃねーかアホじゃねーのか(盛大な暴言)')
        try:
            dev = await message.guild.fetch_member(owner)
            await dev.send(f'おーい、{message.guild}で権限不足なってるー')
        except:
            pass

#サブプロセス用
def screenfetch():
    result = subprocess.run('screenfetch',capture_output=True).stdout.decode()

#メイン
async def commands(message,pf):
    lpf = len(pf)
    #if message.content == f'{pf}test':
    #    await message.channel.send('@reply')

    if message.content.startswith(f'{pf}search user'):
        id = int(message.content[12+lpf:])
        user = await client.fetch_user(id)
        colour = str(user.default_avatar)
        if colour == 'blurple':
            colour = discord.Colour.blurple()
        elif colour == 'grey':
            colour = discord.Colour.greyple()
        elif colour == 'green':
            colour = discord.Colour.green()
        elif colour == 'orange':
            colour = discord.Colour.orange()
        elif colour == 'red':
            colour = discord.Colour.red()
        if user.bot:
            u_b = 'BOT'
        else:
            u_b = 'ユーザー'
        with open('user_data.json') as file:
            user_dict = json.loads(file.read())
        data = discord.Embed(title=f'{u_b}情報',colour=colour)
        data.add_field(name='名前',value=user)
        data.add_field(name='作成日時',value=timedelta.utc2jst(user.created_at).strftime('%Y/%m/%d %H:%M:%S'))
        if user_dict.get(str(user.id)):
            if user_dict[str(user.id)][1]:
                data.add_field(name='メモ',value=user_dict[str(user.id)][1])
        data.add_field(name='アイコン',value='\u200c')
        data.set_image(url=user.avatar_url)
        mes = None
        try:
            mes = await message.channel.send(embed=data)
        except discord.errors.Forbidden:
            await no_embed(message)
        if mes:
            if message.author == user:
                await mes.add_reaction('🖋️')
                def check(reaction, author):
                    return author == user and str(reaction.emoji) == '🖋️'

                try:
                    reaction, user = await client.wait_for('reaction_add',timeout=10.0, check=check)
                except asyncio.TimeoutError:
                    await mes.clear_reaction('🖋️')
                else:
                    def check(m):
                        return m.author == user and m.channel == message.channel
                    await message.channel.send('メモを入力してください。(60秒以内)')

                    try:
                        msg = await client.wait_for('message', timeout=60.0, check=check)
                    except asyncio.TimeoutError:
                        await mes.clear_reaction('🖋️')
                        await message.channel.send('タイムアウトしました。')
                    else:
                        if user_dict[str(user.id)]:
                            user_dict[str(user.id)][1] = msg.content
                        else:
                            user_dict[str(user.id)] = [{},msg.content]
                        with open('user_data.json',mode='w') as file:
                            user_json = json.dumps(user_dict,ensure_ascii=False, indent=2)
                            file.write(user_json)
                        await message.channel.send('メモを設定しました。')


    if message.content.startswith(f'{pf}search server'):
        id = int(message.content[14+lpf:])
        server = client.get_guild(id)
        owner = await client.fetch_user(server.owner_id)
        data = discord.Embed(title='サーバー情報',colour=owner.colour)
        data.add_field(name='名前',value=server.name)
        data.add_field(name='オーナー',value=f'{owner}({owner.id})')
        data.add_field(name='ブーストレベル',value=server.premium_tier)
        data.add_field(name='作成日時',value=timedelta.utc2jst(server.created_at).strftime('%Y/%m/%d %H:%M:%S'))
        data.add_field(name='BOT導入日時',value=timedelta.utc2jst(server.me.joined_at).strftime('%Y/%m/%d %H:%M:%S'))
        data.add_field(name='アイコン',value='\u200c')
        data.set_image(url=server.icon_url)
        try:
            await message.channel.send(embed=data)
        except discord.errors.Forbidden:
            await no_embed(message)

    if message.content.startswith(f'{pf}say'):
        if leveling(message.author,message.channel,1000):
            await message.channel.send(message.content[4+lpf:])
        else:
            await message.channel.send('自分で言えよアホ')

    if message.content == f'{pf}clear':
        if p_check(message.author,message.channel,discord.Permissions().update(manage_messages=True),15000):
            kakunin = await message.channel.send('削除しますか？')
            await kakunin.add_reaction('⭕')
            await kakunin.add_reaction('❌')
            def check(reaction, user):
                return user == message.author

            ask = True
            while ask:
                try:
                    reaction, user = await client.wait_for('reaction_add', timeout=10.0, check=check)

                except:
                    await kakunin.edit(content='削除しますか？\n取り消しました。')
                    ask = False
                else:
                    if str(reaction) == '❌':
                        await kakunin.edit(content='削除しますか？\n取り消しました')
                        ask = False
                    if str(reaction) == '⭕':
                        await message.channel.purge(limit=50000)
                        ask = False

    if message.content == f'{pf}help':
        embed=discord.Embed(title='コマンド',colour=0x00bfff)
        embed.add_field(name=f'{pf}search [user|server] <ID>',value='サーバー情報|ユーザー情報を表示します。')
        embed.add_field(name=f'{pf}clear',value='チャンネル内のメッセージを一括削除します。\n[メッセージの管理]の権限が必要です。')
        embed.add_field(name=f'{pf}ping',value='BOTの応答速度を計測します。')
        try:
            await message.channel.send(embed=embed)
        except discord.errors.Forbidden:
            await no_embed(message)

    if message.content == f'{pf}ping':
        global ping
        mes = await message.channel.send('テスト中……')
        ping.append(mes)

    now = time.time()
    await asyncio.sleep(5)
    if message in ping:
        delta = str((now - message.created_at.timestamp())/1000)
        latency = str(main.client.latency*1000)
        await message.edit(content=f'Ping : {delta[:6]}ms\n'
                                f'Latency : {latency[:6]}ms')
        ping.remove(message)

async def zatzudan(message):
    if message.author != client.user:
        leveling(message.author,message.channel,len(message.content)/2)
        mestime = timedelta.utc2jst(message.created_at)
        luck = random.randint(1,10)
        if luck < 5:
            if 'おはよう' in message.content:
                send = greet(mestime.hour,
                             'ド深夜',
                             '眠ぃ',
                             'おはよー',
                             'おそよう',
                             '昼過ぎてるぞ………',
                             'もう夜なんだが………',
                             '今日1日何してた')
                await message.channel.send(send)
            elif 'こんにちは' in message.content:
                send = greet(mestime.hour,
                             '生活リズムがよくないと思うんだ',
                             'んみゃ？こんちゃっす………',
                             'こんにちは',
                             'Good Afternoon',
                             'こんにちは………\nふぁぁ(あくび)',
                             '夜だぜ',
                             'お  や  す  み')
                await message.channel.send(send)
            elif 'こんばんは' in message.content:
                send = greet(mestime.hour,
                             '寝よう。な？',
                             '今かよ',
                             '徹夜かい？',
                             f'今{mestime.hour}時だけど………え？()',
                             'おひるです。',
                             '早寝っすねー\nいいと思いますよ',
                             'おやすみー')
                await message.channel.send(send)

print('読み込み完了')
