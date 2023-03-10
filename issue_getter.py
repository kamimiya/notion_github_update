import configparser
from asyncio.windows_events import NULL
import discord
from discord.ext import commands
import requests
import json
import re
import datetime
import time
    
class IssueGetter():
    def __init__(self, bot=None):
        # 初期設定 (iniファイルの読み込み)
        ini = configparser.ConfigParser()
        ini.read('./setting.ini', 'UTF-8')
        # アクセストークンの読み取り
        self.github_TOKEN = ini.get('TOKEN Setting', 'github_TOKEN')
        # json受信・送信用のheader
        self.get_header  = {"Authorization": "token " + self.github_TOKEN}
        self.post_header = {'Content-Type': 'application/json'}
        # URLの設定
        self.github_repository_url  = ini.get('URL Setting', 'github_repository_url')
        self.discord_webhook_url    = ini.get('URL Setting', 'discord_webhook_url')
        self.issues_url             = self.github_repository_url + '/issues'
        # bot情報
        self.bot = bot
        # Discord側のフォーラム情報取得
        self.discord_forum_url = ini.get('URL Setting', 'discord_forum_url')
        self.discord_forum_id  = int(ini.get('ROOM Setting', 'discord_forum_id'))
        self.get_forum_info()
        # ファイル設定
        self.log_file = ini.get('FILE Setting', 'log_file')
        # 最終更新時刻
        self.get_last_update_time()
        
    # フォーラムチャンネルで、issue番号に対応するスレッド情報を取得 (【#〇〇】で始まるもの)
    def get_forum_info(self):
        self.thread_dict = {}
        channel = self.bot.get_channel(self.discord_forum_id)
        for thread in channel.threads:
            match = re.match(r"^【#(\d+)", thread.name)
            if match:
                issue_num = int(match.group(1))
                thread_id = thread.id
                self.thread_dict[issue_num] = thread_id
    
    #現在時刻を保存する
    def save_update_time(self):
        self.last_update_time = datetime.datetime.now()
        with open(self.log_file,'w') as f:
            f.write(self.last_update_time.strftime("%Y-%m-%dT%H:%M:%S") + '\n')
            
    #最終更新時刻を呼び出す
    def get_last_update_time(self):
        text = open(self.log_file,'r').read().strip()
        self.last_update_time = datetime.datetime.strptime(text, '%Y-%m-%dT%H:%M:%S')

    #Issue情報を読み取り、対応するスレッドがない場合は作成する
    def post_issue(self):
        #forum情報の更新
        self.get_forum_info()
        issues = requests.get(self.issues_url, headers=self.get_header).json()
        for issue in issues:
            if not issue["number"] in self.thread_dict.keys():
                requests.post(self.discord_webhook_url, json.dumps(self.make_issue_content(issue)), headers=self.post_header)
                print("New Issue is posted!")
        #forum情報の更新(issue_commentに対応するため)
        self.get_forum_info()

    #Issueコメントを反映する
    def post_issue_comment(self):
        for issue_num in self.thread_dict.keys():
            #Issueコメントを取得
            issue_comment_url = self.issues_url + "/" + str(issue_num) + "/comments"
            issue_comments = requests.get(issue_comment_url, headers=self.get_header).json()
            for issue in issue_comments:
                #Issueコメントが投稿された時刻が最終更新時刻よりも新しければ反映(9時間分の時差があるので補正)
                issue_post_time = datetime.datetime.strptime(issue["created_at"], '%Y-%m-%dT%H:%M:%SZ')
                issue_post_time = issue_post_time + datetime.timedelta(hours=9)
                if self.last_update_time < issue_post_time:        
                    issue_post_url = self.discord_webhook_url + "?wait=true&thread_id=" + str(self.thread_dict[issue_num])        
                    requests.post(issue_post_url, json.dumps(self.make_issue_comment_content(issue)), headers=self.post_header)
                    print("New Issue comment is posted!")

    #webhook用のjsonデータの用意(issue comment用)
    def make_issue_comment_content(self, issue_comment):
        # 各種データを入手
        url = 'None' if issue_comment["issue_url"] is None else issue_comment["issue_url"]
        timestamp = 'None' if issue_comment["created_at"] is None else issue_comment["created_at"]
        user = 'None' if issue_comment["user"]["login"] is None else issue_comment["user"]["login"]
        body = 'None' if issue_comment["body"] is None else issue_comment["body"]
        content = {
            'username': 'GitHub通知',
            "embeds": [
                        {
                            "url"           : url,
                            "timestamp"     : timestamp,
                            "color"         : 5620992,
                            "footer": {
                                "text"      : "Github",
                            },
                            "author": {
                                "name"      : "Github",
                                "url"       : "https://github.com/",
                            },
                            "fields": [
                                {
                                    "name"  : "投稿者",
                                    "value" : user,
                                },
                                {
                                    "name"  : "内容",
                                    "value" :body,
                                },
                            ],
                        }
                    ]
        }
        return content

            
    #webhook用のjsonデータの用意(issue用)
    def make_issue_content(self, issue):
        # 各種データを入手
        title = 'None' if issue["title"] is None else "【#"+str(issue["number"])+"】"+issue["title"]
        url = 'None' if issue["html_url"] is None else issue["html_url"]
        timestamp = 'None' if issue["created_at"] is None else issue["created_at"]
        user = 'None' if issue["user"]["login"] is None else issue["user"]["login"]
        milestone = 'None' if issue["milestone"] is None else issue["milestone"]["title"]
        body = 'None' if issue["body"] is None else issue["body"]
        content = {
            'username': 'GitHub通知',
            "embeds": [
                        {
                            "title"         : title,
                            "url"           : url,
                            "timestamp"     : timestamp,
                            "color"         : 5620992,
                            "footer": {
                                "text"      : "Github",
                            },
                            "author": {
                                "name"      : "Github",
                                "url"       : "https://github.com/",
                            },
                            "fields": [
                                {
                                    "name"  : "投稿者",
                                    "value" : user,
                                },
                                {
                                     "name"  : "状態",
                                     "value" :milestone,
                                 },
                                {
                                    "name"  : "内容",
                                    "value" :body,
                                },
                            ],
                        }
                    ],
            "thread_name": title
        }
        return content

class ForumPoster():
    def __init__(self):
        # 接続に必要なオブジェクトを生成
        intents = discord.Intents.all()
        intents.typing = False  # typingは切る
        self.bot = commands.Bot(command_prefix="$", intents=intents)

