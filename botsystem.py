import discord, aiohttp, asyncio, json, re, random, subprocess, time, timedelta
import multiprocessing as mp

owner = 728289161563340881

ping = {}
p_test = []

regex = re.compile('\d+')

aionet = aiohttp.ClientSession()

def search_id(text):
    match = regex.findall(text)
    return [int(i) for i in match  if len(i) == 18]

def setting(c,p):
    global client, pf
    client, pf = c, p

#便利かなぁと作った
def p_check(member,channel,**permissions):
    permission = discord.Permissions()
    for name in permissions:
        permission.update(**permissions)
    if type(channel) == discord.TextChannel:
        return True
    elif member.id == owner or member.permissions_in(channel) >= permission:
        return True
    return False

def send_check(channel):
    if type(channel) in (discord.DMChannel,discord.GroupChannel):
        return 0
    elif p_check(channel.guild.me,channel,embed_links=True):
        return 0
    elif p_check(guild.me,channel,send_messages=True):
        return 1
    else:
        return 2

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

han = 'abcdefghijklmnopqrstuvwxyz1234567890#%&*/+-=():;!?[],.~^¥$"|+_\\<>`\'{}!?¡¢£¤¥¦§¨©ª«¬®¯°±²³´µ¶·¸¹º»¿¨‐∥…‥‘’“”±×÷≠∞∴℃ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩαβγδεζηθικλμνξοπρστυφχψωАБВГДЕЁЖЗИЙКЛМНОПРСТЩФХЦЧУШЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюяⅠⅡⅢⅣⅤⅥⅦⅧⅨ'

#メイン
async def commands(message):
    lpf = len(pf)

    content = message.content
    start = content.startswith
    author = message.author
    channel = message.channel
    guild = message.guild

    p = send_check(channel)

    if p == 2:
        return

    # elif content == f'{pf}test':
    #     await channel.send(f'{pf}reply')

    elif start(f'{pf}info user'):
        id = int(content[10+lpf:])
        user = await client.fetch_user(id)
        colour = str(user.default_avatar)
        colour = eval(f'discord.Colour.{colour}()'.replace('gray','grayple'))
        if user.bot:
            u_b = 'BOT'
        else:
            u_b = 'ユーザー'
        data = discord.Embed(title=f'{u_b}情報',colour=colour)
        data.add_field(name='名前',value=user)
        data.add_field(name='作成日時',value=timedelta.utc2jst(user.created_at).strftime('%Y/%m/%d %H:%M:%S'))
        data.add_field(name='情報カード',value=f'[@{user.name}](https://www.discordapp.com/users/{user.id})')
        data.add_field(name='アイコン',value='\u200c')
        data.set_image(url=user.avatar_url)

        if p == 0:
            await channel.send(embed=data)
        else:
            text = data.title+'\n>>> '
            for field in data.fields:
                text += field.name+'```\n'+field.value+'\n```\n'
            text += data.image.url
            await channel.send(text)

    elif start(f'{pf}info server'):
        id = int(content[12+lpf:])
        server = client.get_guild(id)
        owner = await client.fetch_user(server.owner_id)
        data = discord.Embed(title='サーバー情報',colour=owner.colour)
        data.add_field(name='名前',value=server.name)
        data.add_field(name='オーナー',value=f'{owner}({owner.id})')
        data.add_field(name='ブーストレベル',value=server.premium_subscription_count)
        data.add_field(name='作成日時',value=timedelta.utc2jst(server.created_at).strftime('%Y/%m/%d %H:%M:%S'))
        data.add_field(name='BOT導入日時',value=timedelta.utc2jst(server.me.joined_at).strftime('%Y/%m/%d %H:%M:%S'))
        data.add_field(name='アイコン',value='\u200c')
        data.set_image(url=server.icon_url)

        if p == 0:
            await channel.send(embed=data)
        else:
            text = data.title+'\n>>> '
            for field in data.fields:
                text += field.name+'```\n'+field.value+'\n```\n'
            text += data.image.url
            await channel.send(text)

    elif start(f'{pf}emoji'):
        if content == f'{pf}emoji':
            mes = await channel.send('リアクションを追加してください')
            def check(reaction,user):
                return user == author and reaction.message == mes
            reaction, user = await client.wait_for('reaction_add',check=check)
            await mes.edit(content=reaction.emoji.url)

        elif content[6+lpf:] == 'anime':
            emojis = [emoji for emoji in await guild.fetch_emojis() if emoji.animated]
            mes = await channel.send('絵文字を選択してください')
            for emoji in emojis:
                await mes.add_reaction(emoji)
            def check(reaction,user):
                return user == author and reaction.message == mes
            reaction, user = await client.wait_for('reaction_add',check=check)
            await mes.edit(content=reaction.emoji.url)

        else:
            send = ''
            for id in search_id(content[6+lpf:]):
                send += f'https://cdn.discordapp.com/emojis/{id}.png\n'
            await channel.send(send)


    elif start(f'{pf}timer'):
        set_time = int(content[6+lpf:])
        if set_time < 0:
            await channel.send('マイナスは指定できません。')
        else:
            await channel.send(f'タイマーを{set_time}秒に設定しました')
            async with channel.typing():
                await asyncio.sleep(set_time)
            await channel.send(f'{set_time}秒経過しました')

    elif start(f'{pf}death'):
        arg = content[6+lpf:]
        test = message.clean_content[6+lpf:]
        length = 0
        lines = []
        for line in test.splitlines():
            l = 0
            for s in line:
                if s in han:
                    l += 0.4
                else:
                    l += 1
            l += (len(line.split(' '))-1)/5
            lines.append(l)
            if l > length:
                length = l
        content = '＿'+ '人'*(int(length+0.5)+2) +'＿\n'
        index = 0
        for line in arg.splitlines():
            l = lines[index]
            if l < length:
                s = (length-l)/2
                space = '　'*int(s) + ' '*int((s-int(s))*5)
                line = space + line + space
            content += '＞　' + line + '　＜\n'
            index += 1
        content += '￣' + 'Y^'*(int((int(length)+2)*0.88+0.5)) + 'Y￣'
        await channel.send(content)

    elif start(f'{pf}clear'):
        if content == f'{pf}clear':
            count = 49999
            collect = False
            buttons = ('⭕','❌')
        else:
            count = int(content[6+lpf:])-1
            collect = True
            buttons = ('⭕','❌','⬇️','⬆️')
        if p_check(author,channel,manage_messages=True):
            if len(buttons) == 4:
                kakunin = await channel.send('プレビューの読み込み中……')
                messages = await channel.history(limit=count + 201).flatten()
                messages.remove(kakunin)
                if len(messages) < count:
                    preview = messages[-1]
                    count = len(messages)-1
                else:
                    preview = messages[count]
                embed = discord.Embed(title=f'{count+1}個前のメッセージ',description=preview.content,colour=0x00bfff)
                if p == 0:
                    await kakunin.edit(content='削除しますか？',embed=embed)
                else:
                    text = f'__削除しますか？__\n{count+1}個前のメッセージ\n>>> {embed.description}'
                    await kakunin.edit(content=text)

            else:
                kakunin = await channel.send('チャンネル内のメッセージを消去しますか？')
            for button in buttons:
                await kakunin.add_reaction(button)
            def check(reaction, user):
                return user == author and reaction.message == kakunin

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
                        await channel.purge(limit=count+2)
                        ask = False
                    if str(reaction) in ('⬇️','⬆️'):
                        if str(reaction) == '⬇️' and count != 0:
                            count -= 1
                        elif str(reaction) == '⬆️' and count+1 != len(messages):
                            count += 1
                        preview = messages[count]
                        embed.title = f'{count+1}個前のメッセージ'
                        embed.description = preview.content
                        if p == 0:
                            await kakunin.edit(embed=embed)
                        else:
                            text = f'__削除しますか？__\n{count+1}個前のメッセージ\n>>> {embed.description}'
                            await kakunin.edit(content=text)
                        try:
                            await reaction.remove(user)
                        except:
                            pass
                        timeout = False

    #熊野神社でお祈りしてきた
    elif content == f'{pf}omikuji':
        kekka = random.choice(('大吉','吉','小吉','凶','大凶'))
        await channel.send(kekka)

    elif content == f'{pf}temp':
        async with aionet.get('https://trigger.macrodroid.com/d41cedd3-ad3f-4ffa-a61e-acbae4733937/temp'):
            pass
        def check(message):
            return channel.id == 797752252965322803
        try:
            mes = await client.wait_for('message',check=check,timeout=20.)
            await channel.send(mes.content)
        except:
            pass

    elif content == f'{pf}help':
        help = discord.Embed(title='コマンド',colour=0x00bfff)
        help.add_field(name=f'{pf}emoji ''([{<emojis>}|anime])',value='絵文字のURLを取得します。')
        help.add_field(name=f'{pf}info [user|server] <ID>',value='サーバー情報|ユーザー情報を表示します。\n自分の情報を出すとメモを追加できます。')
        help.add_field(name=f'{pf}clear (<count>)',value='チャンネル内のメッセージを一括削除します。\n[メッセージの管理]の権限が必要です。')
        help.add_field(name=f'{pf}ping',value='BOTの応答速度を計測します。')
        help.add_field(name=f'{pf}death <string>',value='突然の死を生成します')
        if p == 0:
            await channel.send(embed=help)
        else:
            text = data.title+'\n>>> '
            for field in data.fields:
                text += field.name+'```\n'+field.value+'\n```\n'
            await channel.send(text)

    elif start(f'{pf}ping'):
        global ping
        now = time.time() - 32400
        mes = await channel.send('テスト中……')
        ping[mes] = (message.created_at.timestamp(),now)

    now = time.time()
    await asyncio.sleep(5)
    if message in ping.keys():
        ping_now = ping[message]
        mestime = message.created_at.timestamp()
        delta_re = str((ping_now[1] - ping_now[0])*1000)
        delta_se = str((mestime - ping_now[1])*1000)
        delta_all = str((mestime - ping_now[0])*1000)
        latency = str(client.latency*1000)
        result = discord.Embed(title='Pong',colour=0x00bfff)
        result.add_field(name='受信',value=f'{delta_re[:6]}ms')
        result.add_field(name='送信',value=f'{delta_se[:6]}ms')
        result.add_field(name='全体',value=f'{delta_all[:6]}ms')
        result.add_field(name='レイテンシ',value=f'{latency[:6]}ms')
        print('最初',ping_now[0])
        print('受信',ping_now[1])
        print('送信',mestime)
        if p == 0:
            await message.edit(content=None,embed=result)
        else:
            await message.edit(content=f'Ping : {delta_all[:6]}ms\n'
                                       f'Latency : {latency[:6]}ms')
        ping.pop(message)

async def zatzudan(message):
    luck = random.randint(1,10)

    content = message.content
    author = message.author
    channel = message.channel
    guild = message.guild

    if author.id == 749960734049304627:  # 勝手に連携
        if luck < 3:
            if 'Googleアシスタント' in content:
                async for mes in channel.history(limit=5):
                    if mes.channel == channel and 'www.google.com' in mes.content:
                        await channel.send('<@749960734049304627>さんでしゃばらないで')
                        break

    elif author != client.user:
        mestime = timedelta.utc2jst(message.created_at)
        if author.bot:
            luck = random.randint(1,25)
        if luck < 5:
            if 'おはよう' in content:
                send = greet(mestime.hour,
                             'ド深夜',
                             '眠ぃ',
                             'おはよー',
                             'おそよう',
                             '昼過ぎてるぞ………',
                             'もう夜なんだが………',
                             '今日1日何してた')
                await channel.send(send)
            elif 'こんにちは' in content:
                send = greet(mestime.hour,
                             '生活リズムがよくないと思うんだ',
                             'んみゃ？こんちゃっす………',
                             'こんにちは',
                             'Good Afternoon',
                             'こんにちは………\nふぁぁ(あくび)',
                             '夜だぜ',
                             'お  や  す  み')
                await channel.send(send)
            elif 'おやすみ' in content:
                send = greet(mestime.hour,
                             '寝よう。な？',
                             '今かよ',
                             '徹夜かい？',
                             f'今{mestime.hour}時だけど………え？()',
                             'おひるです。',
                             '早寝っすねー\nいいと思いますよ',
                             'おやすみー')
                await channel.send(send)

    if message.reference and luck < 10:
        await channnel.send('そうだよ(便乗')

    if content.endswith('？') and luck < 3 and len(content) < 20 and len(content.splitlines()) == 1:
        def check(msg):
            return msg.channel == channel
        try:
            mes = await client.wait_for('message',check=check,timeout=30.)
            if len(mes.content) < 10:
                com = await channel.send(f'{pf}death {mes.content}')
                await com.delete()
        except:
            pass

print(f'{time.ctime().split(" ")[-2]} 読み込み完了')
