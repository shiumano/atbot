import __main__ as main
import discord, asyncio, json, re, random, subprocess, time, timedelta
import multiprocessing as mp

owner = 728289161563340881

ping = []
p_test = []

regex = re.compile('\d+')
def search_id(text):
    match = regex.findall(text)
    return [int(i) for i in match]

def set_client():
    global client
    client = main.client

#便利かなぁと作った
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
    if type(ch) in (discord.DMChannel,discord.GroupChannel):
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
    if time <= 4:
       message = a
    elif time <= 7:
       message = b
    elif time <= 10:
       message = c
    elif time <= 12:
       message = d
    elif time <= 17:
       message = e
    elif time <= 20:
       message = f
    else:
       message = g
    return message

#あるなら教えてクレメンス
class any:
    def __init__(self,*args):
        self.list = list(args)
    def rem(self,value):
        self.list.remove(value)
    def add(self,value):
        self.list.append(value)

    def __eq__(self,other):
        for value in self.list:
           if value == other:
               return True
        return False
    def __ne__(self,other):
        for value in self.list:
            if value == other:
                return False
        return True

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
                    return author == user and str(reaction.emoji) == '🖋️' and reaction.message == mes

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

    if message.content.startswith(f'{pf}emoji'):
        if message.content == f'{pf}emoji':
            mes = await message.channel.send('リアクションを追加してください')
            def check(reaction,user):
                return user == message.author and reaction.message == mes
            reaction, user = await client.wait_for('reaction_add',check=check)
            await mes.edit(content=reaction.emoji.url)

        else:
            send = ''
            for id in search_id(message.content[6+lpf:]):
                send += f'https://cdn.discordapp.com/emojis/{id}.png\n'
        await message.channel.send(send)


    if message.content.startswith(f'{pf}timer'):
        set_time = int(message.content[6+lpf:])
        await message.channel.send(f'タイマーを{set_time}秒に設定しました')
        async with message.channel.typing():
            await asyncio.sleep(set_time)
        await message.channel.send(f'{set_time}秒経過しました')

    if message.content.startswith(f'{pf}say'):
        if leveling(message.author,message.channel,1000):
            await message.channel.send(message.content[4+lpf:])
        else:
            await message.channel.send('自分で言えよアホ')

    if message.content.startswith(f'{pf}clear'):
        if message.content == f'{pf}clear':
            count = 49999
            collect = False
            buttons = ('⭕','❌')
        else:
            count = int(message.content[6+lpf:])-1
            collect = True
            buttons = ('⭕','❌','⬇️','⬆️')
        if p_check(message.author,message.channel,discord.Permissions().update(manage_messages=True),15000):
            if len(buttons) == 4:
                kakunin = await message.channel.send('プレビューの読み込み中……')
                messages = await message.channel.history(limit=count + 201).flatten()
                messages.remove(kakunin)
                if len(messages) < count:
                    preview = messages[-1]
                    count = len(messages)-1
                else:
                    preview = messages[count]
                embed = discord.Embed(title=f'{count+1}個前のメッセージ',description=preview.content,colour=0x00bfff)
                await kakunin.edit(content='削除しますか？',embed=embed)
            else:
                kakunin = await message.channel.send('チャンネル内のメッセージを消去しますか？')
            for button in buttons:
                await kakunin.add_reaction(button)
            def check(reaction, user):
                return user == message.author and reaction.message == kakunin

            ask = True
            timeout = True
            while ask:
                if timeout:
                    wait = 20.0
                else:
                    wait = 60.0
                try:
                    reaction, user = await client.wait_for('reaction_add', timeout=wait, check=check)

                except:
                    await kakunin.edit(content='削除しますか？\n取り消しました。',embed=None)
                    try:
                        await message.clear_reactions()
                    except:
                        pass
                    ask = False
                else:
                    if str(reaction) == '❌':
                        await kakunin.edit(content='削除しますか？\n取り消しました',embed=None)
                        try:
                            await message.clear_reactions()
                        except:
                            pass
                        ask = False
                    if str(reaction) == '⭕':
                        await message.channel.purge(limit=count+2)
                        ask = False
                    if str(reaction) in ('⬇️','⬆️'):
                        if str(reaction) == '⬇️' and count != 0:
                            count -= 1
                        elif str(reaction) == '⬆️' and count+1 != len(messages):
                            count += 1
                        preview = messages[count]
                        embed.title = f'{count+1}個前のメッセージ'
                        embed.description = preview.content
                        await kakunin.edit(embed=embed)
                        try:
                            await reaction.remove(user)
                        except:
                            pass
                        timeout = False

    if message.content == f'{pf}help':
        help = discord.Embed(title='コマンド',colour=0x00bfff)
        help.add_field(name=f'{pf}emoji''({emoji})',value='絵文字のURLを取得します。')
        help.add_field(name=f'{pf}search [user|server] <ID>',value='サーバー情報|ユーザー情報を表示します。\n自分の情報を出すとメモを追加できます。')
        help.add_field(name=f'{pf}clear (count)',value='チャンネル内のメッセージを一括削除します。\n[メッセージの管理]の権限が必要です。')
        help.add_field(name=f'{pf}ping',value='BOTの応答速度を計測します。')
        try:
            await message.channel.send(embed=help)
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
            elif 'おやすみ' in message.content:
                send = greet(mestime.hour,
                             '寝よう。な？',
                             '今かよ',
                             '徹夜かい？',
                             f'今{mestime.hour}時だけど………え？()',
                             'おひるです。',
                             '早寝っすねー\nいいと思いますよ',
                             'おやすみー')
                await message.channel.send(send)

    if message.content.endswith('NULL') and len(message.content) < 20 and len(message.content.splitlines()) == 1:
        def check(msg):
            return msg.channel == message.channel
        try:
            mes = await client.wait_for('message',check=check,timeout=30)
            if len(mes.content) < 10:
                await message.channel.send(f'{pf}death {mes.content}')
        except:
            pass

print('読み込み完了')
