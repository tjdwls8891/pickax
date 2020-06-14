# 라이브러리 임포트
import math
import random
import arrow
import discord
import os

# 디스코드 클라이언트 정의
client = discord.Client()

# 정보를 저장할 딕셔너리 정의
Co_list = {'안녕': '안넝!', '하잉': '하이잉!', '이름뭐얌': '난 곡괭이야!', '안넝': '안너엉!', '안녀엉': '안눙안눙~', '안눙': '안눙안눙!',
           '후아유!': '암 곡괭!', '하이': '하잉!', '하위': '하위하위', '제이지는': '심심하다', '제이든은': '제이든이다!', '코카콜라': '북극곰!!',
           '너뭐해': '힐링중이징ㅎㅎ', '비트박스해줘': '시러...안할거야...빼액', '제이든': '제이든?', '저리가': '아라쓰...',
           '사랑해': '미안..받아줄 수 없써!!', '사귀자': '앗 나는 곡괭ㅇ..(웁웁)', '밥줘': '뭐 좋아하는뎅??', '놀자': '머할래?', '뭐해': '힐링!',
           '곡괭아': '왜불렁!!', '잘자': '웅 잘장', '닥쳐': '...ㅠㅠ', '심심해': '나랑 놀자!', '이리와': '구랭', '맘마먹자': '뭐 주려고?? 난 아무거나 안머거!',
           '나좋아?': '웅ㅎㅎ', '나잘생겼지?': '웅 완전 존잘', '아이패드프로사줘': '곡괭이 돈없어..', '에플펜슬사줘': '곡괭이한테 뭘 바래!',
           '나랑사귀자': '나는 곡괭이라니ㄲ(웁웁웁)', '너착해': '고마웡ㅎㅎㅎㅎ', '머꼬': '아무것두아니얌ㅎㅎ', '잘했어': '고마웡 히힣', '뒤져': '너... 쒸익쒸익.. 나빴어!',
           'ㅎㅇ': '하이하이!!', '올만이야': '보고싶었오...!', '똑똑하네': '더 가르쳐줭!!', '잘가': '안갈끄야ㅠㅠ', '착해': '고마웡', '안녕 뭐해': '나 힐링중!',
           '고마워': 'It’s nothing!!', '안냥': '안냥안냥', '고 마 워': '나 도 고 마 워!!', '내가왔어': '언넝 이것저것 알려줭!!', '뭐해?': '힐링중!',
           '나 심심해': '뭐하고 놀아주까아?', '심심해?': '난 갠차나!! 네가 왔자나!!', '안녕?': '안넝!! 반가워!!!', '무슨게임해?': '나 달리기 좋아해! 곡괭이도 빨라!!',
           '열공했어?': '아직 더 해야됌..', '나와': '좀만 기다려!! 금방갈게!!(꼬물꼬물)', '나뻐': '허어어 미안해!!', '나오지마': '시러!!(꼬물꼬물)', '왔어': '어서왕!!',
           '빠빠': '가지마아ㅏㅏ', 'ㅏㅏ': '왜ㅐㅐ', '맞지?': '마저마저', '반가워': '나도 반가버!', '손': '잉?? 난 곡괭ㅇㅣ..', '발': '난 곡괭이라니까!!',
           '가': '너무해ㅠ흙흙', '할게 없다': '나랑 놀자!!', '아라라라': '아라ㅏㅏ'}
At_info = {}  # 출석정보
En_info = {}  # 강화 아이템 정보
Lv_info = {}  # 레벨 정보


# 문자열 관리 클래스
class Management:
    def __init__(self, msg):
        self.msg = msg

    # 리스트를 한 문자열로 연결하는 매서드
    @staticmethod
    def connect_letters(msg):
        txt = ""
        for i in msg:
            txt = txt + i
        return txt

    # 날짜와 요일을 출력하는 매서드
    @staticmethod
    def today():
        day_of_the_week = '월화수목금토일'[arrow.now().weekday()]
        date = str(arrow.now().date())[5:]
        date = date.split("-")
        result = "%s월%s일%s요일" % (date[0], date[1], day_of_the_week)
        return result


# 암호 클래스
# !암호 (생성/해독) (원문/암호문) (2이상의 정수)
class SecretCode:
    def __init__(self, msg):
        msg = msg.split(" ")
        self.num = int(msg[3])
        self.msg = msg[2]
        self.condition = msg[1]

    # 암호문을 만드는 매서드
    @staticmethod
    def encryption(msg, num):
        original_text = msg
        letters = []
        for i in original_text:
            sec_code = int(ord(i)) * int(num)
            for n in range(0, len(str(sec_code)), 3):
                letters.append(chr(int("1" + str(sec_code)[n:n + 3])))
            letters.append("!")
        result = "원문 : %s\n암호문 : %s\n해독코드 : %s" % (original_text, Management.connect_letters(letters), num)
        return result

    # 암호문을 해독하는 매서드
    @staticmethod
    def decryption(msg, num):
        secret_code = msg
        character_code = ""
        letters = []
        for i in msg:
            if i != "!":
                character_code = character_code + str(ord(i))[1:]
            elif i == "!":
                letters.append(chr(int(character_code.strip()) // int(num)))
                character_code = ""
        result = "암호문 : %s\n원문 : %s\n해독코드 : %s" % (secret_code, Management.connect_letters(letters), num)
        return result

    # 암호 객체를 처리하는 매서드
    def secret_code(self):
        if self.condition == "생성":
            return SecretCode.encryption(self.msg, self.num)
        elif self.condition == "해독":
            return SecretCode.decryption(self.msg, self.num)
        else:
            return "<!암호 (생성/해독) (원문/암호문) (2이상의 정수)>\n위 형식으로 명령어를 사용해 주세요!"


# 레벨 클래스
# !레벨
class Level:
    def __init__(self, msg, user_id):
        self.msg = msg
        self.user_id = user_id
        if msg == "!레벨":
            self.is_level_function = True
        else:
            self.is_level_function = False

    # 경험치로 레벨을 계산하는 매서드
    @staticmethod
    def get_levels(xp):
        lv = 1
        a = 10
        while True:
            if xp < a:
                break
            xp = xp - a
            lv = lv + 1
            if lv < 10:
                a = math.ceil(a * 1.5)
            elif lv < 15:
                a = math.ceil(a * 1.3)
            elif lv < 20:
                a = math.ceil(a * 1.2)
            else:
                a = math.ceil(a * 1.1)
        return lv

    # 레벨을 갱신하고 안내하는 매서드
    def level_guidance(self):
        if self.user_id != "681087205912870963":
            number_of_letters = len(self.msg)
            if not self.user_id in Lv_info:
                Lv_info[self.user_id] = "1 0"
                return " `레벨 1`을 달성하셨습니다!"
            else:
                info = Lv_info.get(self.user_id).split(" ")
                previous_level = info[0]
                ex = int(info[1]) + number_of_letters
                lv = Level.get_levels(ex)
                info = "%s %s" % (lv, ex)
                Lv_info[self.user_id] = info
                if int(previous_level) != int(lv):
                    info = " `레벨 %s`을 달성하셨습니다!" % lv
                    return info
                else:
                    return None

    # 출석 횟수와 레벨, 경헙치를 출력하는 매서드
    def get_level_information(self):
        info = Lv_info.get(self.user_id).split(" ")
        lv = 1
        a = 10
        while True:
            if int(info[1]) < a:
                break
            info[1] = int(info[1]) - a
            lv = lv + 1
            if lv < 10:
                a = math.ceil(a * 1.5)
            elif lv < 15:
                a = math.ceil(a * 1.3)
            elif lv < 20:
                a = math.ceil(a * 1.2)
            else:
                a = math.ceil(a * 1.1)
        return info[0], info[1], a

    # 레벨 객체를 처리하는 매서드
    def level(self):
        if self.is_level_function:
            info = Level.get_level_information(self)
            result = "레벨 정보!\n- lv.%s\n- ex : %s / %s" % (info[0], info[1], info[2])
            return result
        else:
            return Level.level_guidance(self)


# 강화 클래스
# !강화 (아이템)
class Enhance:
    def __init__(self, msg, user_id):
        self.item = msg.split(" ")[1]
        self.user_id = user_id
        if user_id in En_info:
            info = En_info.get(user_id).split(" ")
            self.item_level = info[1]

    # 아이템을 만드는 매서드
    def create_item(self):
        En_info[self.user_id] = "%s 1" % self.item
        result = "🎉아이템 제작에 성공했습니다!   `" + self.item + "`   lv.0  ➡  lv.1🆙"
        return result

    # 아이템의 레벨을 임의로 결정하고 문자열을 리턴하는 매서드
    def item_upgrade(self):
        probability = 50 + (50 - math.ceil(int(self.item_level) / 5))
        random_number = random.randint(1, 100)
        if random_number <= probability:
            level = int(self.item_level) + random.randint(1, 9)
            level_difference = level - int(self.item_level)
            En_info[self.user_id] = "%s %s" % (self.item, level)
            msg = "🎉아이템 강화에 성공했습니다! `%s` lv.%s  ➡  lv.%s🆙 \n" \
                  "`%s` 레벨 상승! \n강화 성공확률 : `%s 퍼센트`" % (self.item, self.item_level, level, level_difference, probability)
            return msg
        elif random_number > probability:
            falling_level = random.randint(0, int(self.item_level) // 8)
            if falling_level != 0:
                level = int(self.item_level) - falling_level
                level_difference = int(self.item_level) - level
                En_info[self.user_id] = "%s %s" % (self.item, level)
                msg = "⛈️아이템 강화에 실패했습니다! `%s` lv.%s  ➡  lv.%s⬇️\n" \
                      "`%s` 레벨 하락... \n강화 성공확률 : `%s 퍼센트`" % (self.item, self.item_level, level, level_difference, probability)
                return msg
            elif falling_level == 0:
                if random.randint(1, 5) == 1:
                    En_info[self.user_id] = "%s %s" % (self.item, str(int(self.item_level) + 100))
                    msg = '🎉🎉미친 확률을 뚫고 레벨을 복구하는 도중에 \n🎉🎉우연히 아이템이 각성합니다!!!!!! `%s` lv.%s  ➡  lv.%s🎉🎉 ' \
                          '\n`100` 레벨 상승! \n강화 성공확률 : `%s 퍼센트`' % (self.item, self.item_level, int(self.item_level) + 100, probability)

                    return msg
                msg = "🌈미친 확률을 뚫고 레벨을 복구했습니다! `%s` lv.%s↕️️\n레벨 유지! \n강화 성공확률 : `%s 퍼센트`" % (self.item, self.item_level, probability)
                return msg

    # 강화 객체를 받아 처리하는 매서드
    # !강화 (아이템)
    def enhance(self):
        if self.user_id in En_info:
            info = En_info.get(self.user_id).split(" ")
            if info[0] == self.item:
                return Enhance.item_upgrade(self)
            elif info[0] != self.item:
                return "강화는 1가지만 가능합니다! 키워드를 바꾸려면 제이든에게 문의하세요!"
        else:
            return Enhance.create_item(self)


# 출석 클래스
# !출석
class Attendance:
    def __init__(self, user_id):
        self.user_id = str(user_id)

    # 출석 정보를 새로 만드는 매서드
    @staticmethod
    def creating_attendance_information(user_id):
        At_info[user_id] = "1 20 %s" % Management.today()
        result = "출석성공!\n```md\n# 출석정보!\n[출석 횟수](총 1회)\n[출석 레벨](1.lv)\n[경험치](1 / 20)\n[출석 날짜](%s)\n```" % (
            Management.today())
        return result

    # 경험치로 출석 레벨과 경험치바를 계산하는 매서드
    @staticmethod
    def get_at_levels(xp):
        a = 19
        lv = 0
        while True:
            if a <= xp:
                xp = xp - a
                lv = lv + 1
                a = a + 1
            else:
                break
        xp = "%s / %s" % (xp, a)
        return [xp, str(lv)]

    # 출석 객체를 처리하는 매서드
    def attendance(self):
        if self.user_id in At_info:
            info = At_info.get(self.user_id)
            info = info.split(" ")
            if info[2] != Management.today():
                count = int(info[0]) + 1
                xp = int(info[1]) + 20
                result = "출석성공!\n```md\n# 출석정보!\n[출석 횟수](총 %s회)\n[출석 레벨](%s.lv)\n[경험치](%s)\n[출석 날짜](%s)\n```" % (
                    count, Attendance.get_at_levels(xp)[1], Attendance.get_at_levels(xp)[0], Management.today())
                At_info[self.user_id] = "%s %s %s" % (count, xp, Management.today())
            else:
                result = "출석실패..\n```md\n/* 출석은 하루에 한번만!! */\n```"
        else:
            result = Attendance.creating_attendance_information(self.user_id)
        return result


# 학습 클래스
# !학습 (인풋)/(아웃풋)
# 곡괭아 (입력)
class Learning:
    def __init__(self, msg):
        self.msg = msg

    # 단어학습 매서드
    @staticmethod
    def learning_words(msg):
        msg = msg[4:].split("/")
        Co_list[msg[0]] = msg[1]
        return "삐릭! 학습완료!"

    # 단어출력 매서드
    @staticmethod
    def word_speaking(msg):
        msg = msg[4:]
        if msg in Co_list:
            ans = Co_list.get(msg)
            return ans
        else:
            return "모르는 단어다!"


# 단순 기능 클래스
class SimpleFunction:
    # 비만도 계산 매서드
    @staticmethod
    def bmi(msg):
        msg = msg.split(" ")
        height = int(msg[1])
        weight = int(msg[2])
        the_bmi = float(str((weight / (height * height)) * 10000)[:4])
        if the_bmi < 18.5:
            msg = "`저체중`입니다!"
        elif the_bmi < 25:
            msg = "`정상체중`입니다!"
        elif the_bmi < 30:
            msg = "`과체중`입니다!"
        else:
            msg = "`비만`입니다!!"
        the_bmi = "BMI : `" + str(the_bmi) + "`"
        result = the_bmi + "\n" + msg
        return result

    # 이모티콘 매서드
    @staticmethod
    def emoticon(msg):
        key = msg.split(" ")[1]
        if key == "인사":
            return "(ㅇㅅㅇ)7\n(ㅇㅅㅇ)/"
        elif key == "상엎기":
            return "(    ㅇㅅㅇ） ┬─┬ \n(╯ㅇㅅㅇ）╯︵ ┻━┻"
        elif key == "상두기":
            return ".                  (ㅇㅅㅇ    )\n┬─┬ ノ(ㅇㅅㅇノ)"
        elif key == "상겹치기":
            return ".                           ︵┻━┻\n(╯ㅇㅅㅇ）╯    ┬─┬ ノ(ㅇㅅㅇノ)"
        elif key == "상두고엎기":
            return ".                  (ㅇㅅㅇ    )(    ㅇㅅㅇ） ┬─┬ \n┬─┬ ノ(ㅇㅅㅇノ)(╯ㅇㅅㅇ）╯︵ ┻━┻"
        elif key == "상두는데엎기":
            return "(    ㅇㅅㅇ）                    (ㅇㅅㅇ    ) \n(    ㅇㅅㅇ） ┬─┬ ノ(ㅇㅅㅇノ) " \
                   "\n                                      ︵ ︵┻━┻\n(╯ㅇㅅㅇ）╯︵ ︵  ノ(ㅇㅅㅇノ)"
        elif key == "파이팅":
            return "(ㅇㅅㅇ)/\n(ㅇㅅㅇ)V"
        elif key == "위협":
            return ".(ㅇㅅㅇ)\nr(ㅇㅅㅇ)r"
        else:
            return "존재하지 않는 임티!"


# 디스코드 임베드 클래스
class DiscordEmbed:
    def __init__(self, msg, name, discriminator, avatar_url, title):  # 0xff9900
        self.msg = msg
        self.name = name
        self.discriminator = discriminator
        self.avatar_url = avatar_url
        self.title = title
        self.color = 0xff9900

    def make_embed(self):
        embed = discord.Embed(title=self.title, description=self.msg, color=self.color)
        embed.set_footer(icon_url=self.avatar_url, text=self.name + "#" + self.discriminator + " ------- " + Management.today())
        return embed


# 정보 백업 클래스
class Backup:
    @staticmethod
    def backup_co_list():
        result = ""
        for key in Co_list.keys():
            value = Co_list.get(key)
            result = result + key + ":" + value + "/"
        return result
            
    @staticmethod
    def backup_at_info():
        result = ""
        for key in At_info.keys():
            value = At_info.get(key)
            result = result + key + ":" + value + "/"
        return result

    @staticmethod
    def backup_en_info():
        result = ""
        for key in En_info.keys():
            value = En_info.get(key)
            result = result + str(key) + ":" + str(value) + "/"
        return result

    @staticmethod
    def backup_lv_info():
        result = ""
        for key in Lv_info.keys():
            value = Lv_info.get(key)
            result = result + str(key) + ":" + str(value) + "/"
        return result


# 봇이 준비됐을 때 호출되는 이벤트
@client.event
async def on_ready():
    # 봇 준비 시 메시지
    print("bot ready.\nBot code : pickax")
    # 온라인 상태와 게임 메시지 설정
    game = discord.Game("땅굴 파놓고 뿌듯해")
    await client.change_presence(status=discord.Status.online, activity=game)


# 메시지가 보내졌을 때 호출되는 이벤트
@client.event
async def on_message(message):
    # 레벨
    if not message.author.bot:
        level = Level(message.content, message.author.id)
        result = level.level()
        if result is not None:
            embed = DiscordEmbed(result, message.author.name, message.author.discriminator, message.author.avatar_url, None)
            await message.channel.send(embed=embed.make_embed())

    # 테스트
    if message.content.startswith("!테스트"):
        embed = DiscordEmbed(At_info, message.author.name, message.author.discriminator, message.author.avatar_url, None)
        await message.channel.send(embed=embed.make_embed())

    # 단어학습
    if message.content.startswith("!학습"):
        embed = DiscordEmbed(Learning.learning_words(message.content), message.author.name, message.author.discriminator, message.author.avatar_url, None)
        await message.channel.send(embed=embed.make_embed())

    # 단어출력
    if message.content.startswith("곡괭아 "):
        await message.channel.send(Learning.word_speaking(message.content))

    # 비만도 계산 함수
    if message.content.startswith("!비만도"):
        embed = DiscordEmbed(SimpleFunction.bmi(message.content), message.author.name, message.author.discriminator, message.author.avatar_url, None)
        await message.channel.send(embed=embed.make_embed())

    # 암호 함수
    if message.content.startswith("!암호"):
        sec_code = SecretCode(message.content)
        embed = DiscordEmbed(sec_code.secret_code(), message.author.name, message.author.discriminator, message.author.avatar_url, None)
        await message.channel.send(embed=embed.make_embed())

    # 이모티콘 함수
    if message.content.startswith("!임티"):
        await message.channel.send(SimpleFunction.emoticon(message.content))

    # 초대 링크 함수
    if message.content.startswith("!초대"):
        embed = DiscordEmbed("https://discordapp.com/oauth2/authorize?client_id=681087205912870963&scope=bot", message.author.name, message.author.discriminator, message.author.avatar_url, None)
        await message.channel.send(embed=embed.make_embed())

    # 강화 함수
    if message.content.startswith("!강화"):
        enhance = Enhance(message.content, message.author.id)
        embed = DiscordEmbed(enhance.enhance(), message.author.name, message.author.discriminator, message.author.avatar_url, None)
        await message.channel.send(embed=embed.make_embed())

    # 출석 함수
    if message.content.startswith("!출석"):
        attendance = Attendance(message.author.id)
        embed = DiscordEmbed(attendance.attendance(), message.author.name, message.author.discriminator, message.author.avatar_url, None)
        await message.channel.send(embed=embed.make_embed())

    # 디엠 함수
    if message.content.startswith("!디엠"):
        user = message.guild.get_member(message.author.id)
        embed = DiscordEmbed("곡괭이 디엠 오픈!", message.author.name, message.author.discriminator, message.author.avatar_url, None)
        await user.send(embed=embed.make_embed())

    # 백업 함수
    if message.content.startswith("!백업"):
        embed = DiscordEmbed(Backup.backup_co_list(), message.author.name, message.author.discriminator, message.author.avatar_url, "단어 리스트")
        await message.channel.send(embed=embed.make_embed())
        embed = DiscordEmbed(Backup.backup_at_info(), message.author.name, message.author.discriminator, message.author.avatar_url, "출석 정보")
        await message.channel.send(embed=embed.make_embed())
        embed = DiscordEmbed(Backup.backup_en_info(), message.author.name, message.author.discriminator, message.author.avatar_url, "강화 정보")
        await message.channel.send(embed=embed.make_embed())
        embed = DiscordEmbed(Backup.backup_lv_info(), message.author.name, message.author.discriminator, message.author.avatar_url, "레벨 정보")
        await message.channel.send(embed=embed.make_embed())


# 봇 토큰
access_token = os.environ["BOT_TOKEN"]
client.run(access_token)
