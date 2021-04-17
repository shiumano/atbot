import discord
import aiohttp
import asyncio
import async_google_trans_new
import platform
import psutil
import re
import random
import sys
import time
import timedelta
import youtube_dl
# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

owner = 728289161563340881

ping = {}
p_test = []

regix = re.compile('\d+')

aionet = aiohttp.ClientSession()

def search_id(text):
    match = regex.findall(text)
    return [int(i) for i in match  if len(i) == 18]

def setting(c):
    global client
    client = c

#便利かなぁと作った
def p_check(member,channel,**permissions):
    permission = discord.Permissions()
    permission.update(**permissions)

    if member.id == owner or member.permissions_in(channel) >= permission:
        return True
    else:
        return False

def send_check(channel):
    if type(channel) in (discord.DMChannel,discord.GroupChannel):
        return 2
    elif p_check(channel.guild.me,channel,embed_links=True):
        return 2
    elif p_check(channel.guild.me,channel,send_messages=True):
        return 1
    else:
        return 0

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

def str2datetime(arg,args):
    date = ''
    time_ = ''
    count = len(arg.split('/'))
    if count == 3:
        date = '%Y/%m/%d'
        index = argv.index(arg)
        time__ = argv[index+1]
        if ':' in time__:
            count = len(time__.split(':'))
            if count == 4:
                time_ = ' %H:%M:%S:%f'
                arg += argv.pop(index+1)
            elif count == 3:
                time_ = ' %H:%M:%S'
                arg += argv.pop(index+1)
            elif count == 2:
                try:
                    int(time__.split(':')[0])
                except ValueError:                                                                    pass
                else:
                    time_ = ' %H:%M'
                    arg += argv.pop(index+1)
            else:
                try:
                    int(time__)
                except ValueError:
                    pass
                else:
                    time_ = ' %H'
                    arg += argv.pop(index+1)
    elif count == 2:
        date = '%Y/%m'
    elif count == 1:
        date = '%Y'
    try:
        datetime_ = datetime.datetime.strptime(arg,date+time_)
    except ValueError:
        pass
    argv.remove(arg)
    return datetime_

#メイン
async def commands(message,pf):
    lpf = len(pf)

    content = message.content
    argv = content.split()
    command = argv[0]
    argc = len(argv)
    author = message.author
    channel = message.channel
    send = channel.send
    guild = message.guild

    if argv[-1] == 'text':
        p = 1
    else:
        p = send_check(channel)

    if p == 0:
        can_send = [ch for ch in guild.text_channels() if send_check(ch)]
        if len(can_send) == 0:
            text = (f'{guild.name}には送信できるチャンネルが無いようです……\n'
                     'サーバーの管理者に連絡するかDMでご利用ください。')
        else:
            text = f'{channel.mention}ではご利用になれません。\n'
            for ch in can_send:
                text += ch.mention + '\n'
            text += 'こちらのチャンネルでご利用ください。'
        try:
            await author.send(text)
        except:
            pass

    if argv[-1] == 'dm':
        send = author.send

    # elif content == f'{pf}test':
    #     await channel.send(f'{pf}reply')

    elif command == f'{pf}info':
        if argc == 1:
            await send(f'モードを指定してください。\n`{pf}info help`で使用方法を確認できます。')
        elif argv[1] == 'user':
            try:
                id = int(argv[2])
                user = await client.fetch_user(id)
            except IndexError:
                await send('IDを指定してください')
            except ValueError:
                await send('IDは数字で指定してください')
            except discord.errors.NotFound:
                await send('ユーザーが見つかりませんでした')
            else:
                colour = str(user.default_avatar)
                colour = eval(f'discord.Colour.{colour}()'.replace('grey','greyple'))
                if user.bot:
                    u_b = 'BOT'
                else:
                    u_b = 'ユーザー'
                data = discord.Embed(title=f'{u_b}情報',colour=colour)
                data.add_field(name='名前',value=user)
                data.add_field(name='作成日時',value=timedelta.utc2jst(user.created_at).strftime('%Y/%m/%d %H:%M:%S'))
                data.add_field(name='情報カード',value=f'[@{user.name}](https://www.discordapp.com/users/{user.id})')
                data.add_field(name='アイコン',value='\u200c',inline=True)
                data.set_image(url=user.avatar_url)

                if p == 2:
                    await send(embed=data)
                else:
                    text = data.title+'\n>>> '
                    for field in data.fields:
                        text += field.name+'```\n'+field.value+'\n```\n'
                    text = text[:-10]+'\n'+data.image.url
                    await send(text)

        elif argv[1] == 'server':
            server = None
            try:
                id = int(argv[2])
                server = client.get_guild(id)
                g = True

            except IndexError:
                server = guild
                print(1)

            except ValueError:
                try:
                    invite = await client.fetch_invite(argv[2])
                except discord.errors.NotFound:
                    await send('IDは数字で指定してください')
                else:
                    server = invite.guild
                    g = False

            if server is None:
                await send('サーバーが見つかりませんでした。')
            else:
                data = discord.Embed(title='サーバー情報',colour=0x00bfff)
                data.add_field(name='名前',value=server.name)
                data.add_field(name='作成日時',value=timedelta.utc2jst(server.created_at).strftime('%Y/%m/%d %H:%M:%S'))
                if g:
                    owner = await client.fetch_user(server.owner_id)
                    data.add_field(name='オーナー',value=f'{owner}({owner.id})')
                    data.add_field(name='ブーストレベル',value=server.premium_subscription_count)
                    data.add_field(name='BOT導入日時',value=timedelta.utc2jst(server.me.joined_at).strftime('%Y/%m/%d %H:%M:%S'))
                else:
                    data.add_field(name='サーバーID',value=server.id)
                    if invite.inviter is not None:
                        data.add_field(name='招待者',value=invite.inviter)
                    data.add_field(name='メンバー人数',value=invite.approximate_member_count)
                data.add_field(name='アイコン',value='\u200c',inline=True)
                data.set_image(url=server.icon_url)

                if p == 2:
                    await send(embed=data)
                else:
                    text = data.title+'\n>>> '
                    for field in data.fields:
                        text += field.name+'```\n'+field.value+'\n```\n'
                    text = text[:-10]+'\n'+data.image.url
                    await send(text)

        elif argv[1] == 'help':
            help = discord.Embed(title=f'{pf}info --- 使用方法',colour=0x00bfff)
            help.add_field(name=f'{pf}info user <ID>',value='IDで指定したユーザーの情報を表示します。')
            help.add_field(name=f'{pf}info server <ID|URL>',value='IDまたはURLで指定したサーバーの情報を表示します。')

            if p == 2:
                await send(embed=help)
            else:
                text = help.title + '\n>>> ```'
                for field in help.fields:
                    text += field.name+'```\n'+field.value+field.value+'\n```\n'
                text = text[:-4]
                await send(text)


    elif command == f'{pf}emoji':
        if argc == 1:
            mes = await send('リアクションを追加してください')
            def check(reaction,user):
                return user == author and reaction.message == mes
            reaction, user = await client.wait_for('reaction_add',check=check)
            await mes.edit(content=reaction.emoji.url)

        elif argv[1] == 'anime':
            emojis = [emoji for emoji in await guild.fetch_emojis() if emoji.animated]
            mes = await send('絵文字を選択してください')
            for emoji in emojis:
                await mes.add_reaction(emoji)
            def check(reaction,user):
                return user == author and reaction.message == mes
            reaction, user = await client.wait_for('reaction_add',check=check)
            await mes.edit(content=reaction.emoji.url)

        else:
            url = ''
            for id in argv[1:]:
                url += f'https://cdn.discordapp.com/emojis/{id.split(":")[2][:-1]}.png\n'
            await send(url)


    elif command == f'{pf}timer':
        set_time = float(argv[1])
        if set_time <= 0:
            await send('0以下は指定できません。')
        else:
            await send(f'タイマーを{set_time}秒に設定しました')
            async with channel.typing():
                await asyncio.sleep(set_time)
            await channel.send(f'{set_time}秒経過しました')

    elif command == f'{pf}death':
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
        await send(content)

    elif command == f'{pf}clear':
        if argc == 1:
            count = 49999
            collect = False
            buttons = ('⭕','❌')
        else:
            count = int(argv[1])-1
            collect = True
            buttons = ('⭕','❌','⬇️','⬆️')
        if p_check(author,channel,manage_messages=True):
            if len(buttons) == 4:
                kakunin = await send('プレビューの読み込み中……')
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
                kakunin = await send('チャンネル内のメッセージを消去しますか？')
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
    elif command == f'{pf}omikuji':
        kekka = random.choice(('大吉','吉','小吉','凶','大凶'))
        await send(kekka)

    elif command == f'{pf}trans':
        translator = async_google_trans_new.google_translator()
        lang = argv[1]
        text = message.content[9+lpf:]
        result = await translator.translate(text,lang)
        embed = discord.Embed(title='翻訳結果',description=result,colour=0x00bfff)

        if p == 2:
            await send(embed=embed)
        else:
            text='翻訳結果\n>>>' + result
            await send(text)

    elif command == f'{pf}history':
        argv.pop(0)
        keys = {'count':50000,
                'from':[],
                'mentions':[],
                'has':{'kind':[],'type':[],'set':'and'},
                'befor':None,
                'during':None,
                'after':None,
                'in':None}
        parsed_args = []
        for arg in argv:
            if arg.startswith('count:'):
                keys['count'] = int(arg[6:])
                parsed_args.append(arg)
            elif arg.startswith('from:'):
                if '<@' in arg:
                    keys['from'].append(client.fetch_user(arg[7:-1]))
                else:
                    keys['from'].append(arg[5:])
                parsed_args.append(arg)
            elif arg.startswith('mentions:'):
                if '<@' in arg:                                                   keys['mentions'].append(client.fetch_user(arg[11:-1]))
                else:
                    keys['mentions'].append(arg[9:])
                parsed_args.append(arg)
            elif arg.startswith('has:'):
                kind = arg[4:].lower()
                if kind in ('リンクで検索','link'):
                    keys['has']['kind'].append('link')
                elif kind in ('埋め込みを検索','embed'):
                    keys['has']['kind'].append('embed')
                elif kind in ('ファイルを検索','file'):
                    keys['has']['kind'].append('file')
                elif kind in ('動画を検索','movie'):
                    keys['has']['kind'].append('movie')
                elif kind in ('画像を検索','picture'):
                    keys['has']['kind'].append('picture')
                elif kind in ('音声付きを検索','sound'):
                    keys['has']['kind'].append('sound')
                elif kind.startswith('.'):
                    keys['has']['type'].append(kind)
                elif kind == ':or':
                    keys['has']['set'] = 'or'
                parsed_args.append(arg)
            elif arg.startswith('befor:'):
                keys['befor'] = str2datetime(arg,argv)
                parsed_args.append(arg)
            elif arg.startswith('during'):
                keys['during'] = str2datetime(arg,argv)
                parsed_args.append(arg)
            elif arg.startswith('after'):
                keys['after'] = str2datetime(arg,argv)
                parsed_args.append(arg)
            elif arg.startswith('in'):
                keys['in'] = message.channel
                parsed_args.append(arg)
        await send(keys)



    elif command == f'{pf}system':
        data = discord.Embed(title='システム情報',colour=0x00bfff)
        data.add_field(name='Pythonバージョン',value=sys.version)
        data.add_field(name='Discord.pyバージョン',value=discord.__version__)
        data.add_field(name='OS',value=platform.platform())
        data.add_field(name='CPU使用率',value=f'{psutil.cpu_percent()}%')
        data.add_field(name='BOT起動時刻',value=timedelta.time2jt(psutil.boot_time()))
        if p == 2:
            await send(embed=data)
        else:
            text = data.title+'\n>>> '
            for field in data.fields:
                text += field.name+'```\n'+field.value+'\n```\n'
            await send(text)

    elif command == f'{pf}voice':
        if argv[1] == 'join':
            if author.voice is None:
                await send("あなたはボイスチャンネルに接続していません。")
            else:
                # ボイスチャンネルに接続する
                await author.voice.channel.connect()
                await send("接続しました。")

        elif argv[1] == 'leave':
            if guild.voice_client is None:
                await send("接続していません。")
            else:
                # 切断する
                await guild.voice_client.disconnect()
                await send("切断しました。")

        elif argv[1] == 'play':
            if guild.voice_client is None:
                await send("接続していません。")
            else:
                mes = await send('ロード中………')
                player = await YTDLSource.from_url(argv[2], loop=client.loop)

                # 再生する
                await guild.voice_client.play(player)
                await mes.edit(content='{} を再生します。'.format(player.title))

        elif argv[1] == '':
            1

    elif command == f'{pf}help':
        help = discord.Embed(title='コマンド',colour=0x00bfff)
        help.add_field(name=f'{pf}emoji ''([{<emojis>}|anime])',value='絵文字のURLを取得します。')
        help.add_field(name=f'{pf}info [user|server] <ID>',value='サーバー情報|ユーザー情報を表示します。')
        help.add_field(name=f'{pf}clear (<count>)',value='チャンネル内のメッセージを一括削除します。\n[メッセージの管理]の権限が必要です。')
        help.add_field(name=f'{pf}ping',value='BOTの応答速度を計測します。')
        help.add_field(name=f'{pf}timer <seconds>',value='指定した秒数のあとメッセージを送信します。')
        help.add_field(name=f'{pf}death <string>',value='突然の死を生成します')
        if p == 2:
            await send(embed=help)
        else:
            text = help.title+'\n>>> '
            for field in help.fields:
                text += field.name+'```\n'+field.value+'\n```\n'
            await send(text)

    elif command == f'{pf}ping':
        global ping
        now = time.time() - 32400
        mes = await send('テスト中……')
        ping[mes] = (message.created_at.timestamp(),now)


async def zatzudan(message,pf):
    luck = random.randint(1,10)

    content = message.content
    start = content.startswith
    author = message.author
    channel = message.channel
    send = channel.send
    guild = message.guild

    p = send_check(channel)

    if p == 0:
        return '正直言って論外だよね'

    if author.id == 749960734049304627:  # 勝手に連携
        if luck < 3:
            if 'Googleアシスタント' in content:
                async for mes in channel.history(limit=5):
                    if mes.channel == channel and 'www.google.com' in mes.content:
                        await send('<@749960734049304627>さんでしゃばらないで')
                        break

    elif author != client.user:
        mestime = timedelta.utc2jst(message.created_at)
        if author.bot:
            luck = random.randint(1,25)
        if luck < 5:
            if 'おはよう' in content:
                text = greet(mestime.hour,
                             'ド深夜',
                             '眠ぃ',
                             'おはよー',
                             'おそよう',
                             '昼過ぎてるぞ………',
                             'もう夜なんだが………',
                             '今日1日何してた')
                await send(text)
            elif 'こんにちは' in content:
                text = greet(mestime.hour,
                             '生活リズムがよくないと思うんだ',
                             'んみゃ？こんちゃっす………',
                             'こんにちは',
                             'Good Afternoon',
                             'こんにちは………\nふぁぁ(あくび)',
                             '夜だぜ',
                             'お  や  す  み')
                await send(text)
            elif 'おやすみ' in content:
                text = greet(mestime.hour,
                             '寝よう。な？',
                             '今かよ',
                             '徹夜かい？',
                             f'今{mestime.hour}時だけど………え？()',
                             'おひるです。',
                             '早寝っすねー\nいいと思いますよ',
                             'おやすみー')
                await send(text)

    if message.reference and luck < 3:
        await send('そうだよ(便乗')

    if content.endswith('？') and luck < 3 and len(content) < 20 and len(content.splitlines()) == 1:
        def check(msg):
            return msg.channel == channel
        try:
            mes = await client.wait_for('message',check=check,timeout=30.)
            if len(mes.content) < 10:
                com = await send(f'{pf}death {mes.content}')
                await com.delete()
        except:
            pass

    if 'ｱﾋｬ' in message.content:
            if luck < 7:
                await message.channel.send('( ﾟ∀ﾟ)ｱﾋｬ')
            else:
                await message.channel.send('飽きた()')

    await asyncio.sleep(5)
    if message in ping.keys():
        ping_now = ping[message]
        mestime = message.created_at.timestamp()
        delta_re = str((ping_now[1] - ping_now[0])*1000)
        delta_se = str((mestime - ping_now[1])*1000)
        delta_all = str((mestime - ping_now[0])*1000)
        latency = str(client.latency*1000)
        result = discord.Embed(title='Pong',colour=0x00bfff)
        ## サーバー時間とクライアント時間揃ってないから
        # result.add_field(name='受信',value=f'{delta_re[:6]}ms')
        # result.add_field(name='送信',value=f'{delta_se[:6]}ms')
        result.add_field(name='Ping',value=f'{delta_all[:6]}ms')
        result.add_field(name='レイテンシ',value=f'{latency[:6]}ms')
        if p == 2:
            await message.edit(content=None,embed=result)
        else:
            await message.edit(content=f'Ping : {delta_all[:6]}ms\n'
                                       f'Latency : {latency[:6]}ms')
        ping.pop(message)

print(f'{time.ctime().split(" ")[-2]} 読み込み完了')
