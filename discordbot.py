import discord
from discord.ext import tasks, commands
import asyncio
from issue_getter import IssueGetter
import configparser

# 接続に必要なオブジェクトを生成
intents = discord.Intents.all()
intents.typing = False  # typingは切る
bot = commands.Bot(command_prefix="$", intents=intents)

# アクセストークンの読み取り
ini = configparser.ConfigParser()
ini.read('./setting.ini', 'UTF-8')
discord_TOKEN = ini.get('TOKEN Setting', 'discord_TOKEN')

# 起動メッセージ
@bot.event
async def on_ready():
    global issue_getter
    issue_getter = IssueGetter(bot)
    print('起動しました')
    # Issue情報の更新
    issue_getter.post_issue()
    issue_getter.post_issue_comment()
    # 最終更新時刻を更新
    issue_getter.save_update_time()

## Git情報の読み取り (60s毎に更新)
@tasks.loop(seconds=60)
async def loop():
    global issue_getter
    #if(bot):
    try:
        # Issueコメントの更新
        issue_getter.post_issue()
        issue_getter.post_issue_comment()
        # 最終更新時刻を更新
        issue_getter.save_update_time()
    except:
        pass

# Botの起動とDiscordサーバーへの接続
async def main():
    async with bot:
        loop.start()
        await bot.start(discord_TOKEN)
        
try:
    asyncio.run(main())
except Exception as e:
        print("エラーが発生しました：", e)
