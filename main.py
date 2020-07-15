# 라이브러리 임포트
import arrow
import discord
import random

# 디스코드 클라이언트 정의
client = discord.Client()


# 문자열 관리 클래스
class Management:
    # 문자열 공백 제거 매서드
    @staticmethod
    def remove_spaces(msg):
        msg = Management.connect_letters(msg.split(" "))
        return msg

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
        result = "%s월 %s일 %s요일" % (date[0], date[1], day_of_the_week)
        return result


# 암호 클래스
# !암호 (생성/해독) (원문/암호문) (2이상의 정수)
class SecretCode:
    def __init__(self, msg):
        msg = msg[4:].split("/")
        self.num = int(msg[2])
        self.msg = msg[1]
        self.condition = msg[0]

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

    # 랜덤 수 매서드
    @staticmethod
    def random_number(top_num, btm_num):
        result = random.randint(int(btm_num), int(top_num))
        return result


# 디스코드 임베드 클래스
class DiscordEmbed:
    def __init__(self, msg, message, title):
        self.msg = msg
        self.name = message.author.name
        self.discriminator = message.author.discriminator
        self.avatar_url = message.author.avatar_url
        self.title = title
        self.color = 0x9999ff

    def make_embed(self):
        embed = discord.Embed(title=self.title, description=self.msg, color=self.color)
        embed.set_footer(icon_url=self.avatar_url,
                         text=self.name + "#" + self.discriminator + " ------- " + Management.today())
        return embed


# 봇이 준비됐을 때 호출되는 이벤트
@client.event
async def on_ready():
    # 봇 준비 시 메시지
    print("bot ready.\nBot code : Cloud")
    # 온라인 상태와 게임 메시지 설정
    game = discord.Game("모양 만들기")
    await client.change_presence(status=discord.Status.online, activity=game)


# 메시지가 보내졌을 때 호출되는 이벤트
@client.event
async def on_message(message):
    # 명령어(임베드 메시지)
    if not message.author.bot:
        # 이스터에그
        if message.content.startswith("юѠ!ߌ!ѓѐ!эԀ!ݢ¬!"):
            embed = DiscordEmbed("와... 대단하네..ㄷㄷㄷ", message, "이스터에그 발견..!")
            await message.channel.send(embed=embed.make_embed())

        # 테스트
        if message.content.startswith("!테스트"):
            embed = DiscordEmbed(message.content, message, "테스트")
            await message.channel.send(embed=embed.make_embed())

        # 날짜 출력 함수
        if message.content.startswith("!날짜"):
            embed = DiscordEmbed(Management.today() + "!", message, "오늘 날짜는!")
            await message.channel.send(embed=embed.make_embed())

        # 비만도 계산 함수
        if message.content.startswith("!비만도"):
            embed = DiscordEmbed(SimpleFunction.bmi(message.content), message, "당신은")
            await message.channel.send(embed=embed.make_embed())

        # 암호 함수
        if message.content.startswith("!암호"):
            sec_code = SecretCode(message.content)
            embed = DiscordEmbed(sec_code.secret_code(), message, None)
            await message.channel.send(embed=embed.make_embed())

        # 이모티콘 함수
        if message.content.startswith("!임티"):
            await message.channel.send(SimpleFunction.emoticon(message.content))

        # 초대 링크 함수
        if message.content.startswith("!초대"):
            embed = DiscordEmbed("https://discord.com/oauth2/authorize?client_id=732469734846627880&scope=bot", message, "초대 링크!")
            await message.channel.send(embed=embed.make_embed())

        # 디엠 함수
        if message.content.startswith("!디엠"):
            user = message.guild.get_member(message.author.id)
            embed = DiscordEmbed(None, message, "디엠 오픈!!")
            await user.send(embed=embed.make_embed())

        # 랜덤 함수
        if message.content.startswith("!랜덤"):
            msg = message.content.split(" ")
            result = random.randint(int(msg[1]), int(msg[2]))
            embed = DiscordEmbed(str(result) + "!!", message, "결과는??")
            await message.channel.send(embed=embed.make_embed())

    # 단순 메시지
    if not message.author.bot:
        if message.content == "구름아":
            await message.channel.send("???")

                      
# 봇 토큰
access_token = os.environ["BOT_TOKEN"]
client.run(access_token)
