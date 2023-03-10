# notion_github_update

## 概要

GitHubの更新通知をDiscordに投げつけるBOTです。<br>
python読める＆python実行できる人向けです。

## 機能
1. Github上のIssue, Issue comment情報をdiscordのforumに反映


## ファイル構造
|ファイル名|内容|
|---|---|
|discordbot.py|メインファイル|
|issue_getter.py|Issue管理を担当するファイル|
|setting.ini|TOKENなどの設定を行うiniファイル|
|time.log|最終更新時刻を記録したファイル|

## 初期設定
### 導入が必要なソフト

このソフトを利用するために以下のソフト類のインストールが必要です。

1. python3のインストール
   [このサイト](https://www.python.jp/install/windows/install.html)を参考にしてください。
   
   **python3.8以上をおすすめします。**（3.7より古いものはライブラリがサポートしていない）
   
2. 各種ライブラリのインストール

   コマンドプロンプト(Win+Rで"ファイル名を指定して実行"をひらいて"cmd"を打ち込んだら出てくると思います）上で以下のコマンドを打ち込んで実行してください。

   ```bash
   $ pip install git+https://github.com/Rapptz/discord.py
   $ pip install PyNaCl
   $ pip install requests
   ```

   
### DircordのBot作成方法について
[このサイト](https://note.com/exteoi/n/nf1c37cb26c41)の**1. Discord上のBotの作成**にある記述を参考にしてください。

   1. https://discord.com/developers/applications を開きます。
   2. 右上にあるNew Applicationを押す。適当な名前を入れてCreateを押します。
   3. 管理画面が開かれる。左のメニューのBotを押し、Add Botを押す。→Yes, do it!を選択（開かれない場合はDeveloper Portalから作成したアプリケーションを選択する）
   4. するとBuild-A-Botのところになんか出てくる。そのTOKENのところにあるCopyを押すとBotのTOKENがコピーできる。**のちに必要となるので保存しておく。**
   5. その下の**PUBLIC BOT, REQUIRES OAUTH2 CODE GRANT**をオフ、**Presence Intent, Server Members Intent, Message Content Intent**という項目をオンにする。(灰色がオフ、青色がオン）**
   6. 左のメニューのOAuth2→URL Generatorを開きます。 SCOPESで**bot, applications.commands**にチェックを入れます。
   7. BOT PERMISSIONSという項目が出てくると思うので**Read Messages/ViewChannels, Send Messages, Embed Links, Add Reactions, Use Slash Commands, Connect, Speak**にチェックを入れてください。
   8. 一番下にあるGENERATED URLにあるリンクを開くとサーバー招待画面が出てくるので、追加したいサーバーを選択して認証します 。

### GitHubのAPI用キー入手方法

1. Setting -> Developer Settings -> Personal access tokens -> Fine-grained tokens
2. **Generate new token**に適当な名前と説明を付けて、access設定をいい感じにしたら完成

## 起動方法

1. 上の導入が必要なソフトをすべてインストールします。

2. このフォルダをわかりやすい場所に置きます。

3. DiscordのBotを作成し、招待します。（すでにチャットルームにBotを招待している場合は省略）

4. setting.iniにアクセストークンなどを設定する（すでに設定していたら省略）

5. コマンドプロンプトを起動します。 (Win+Rで"ファイル名を指定して実行"をひらいて"cmd"を打ち込んだら出てくると思います）

6. チェンジディレクトリでこのフォルダの中身まで移動します。
   cd ディレクトリ名で移動できます。（https://eng-entrance.com/windows-command-cd を参照）例えば以下のようにする。

   ```bash
   $ cd \d A:\discord_bot\notion_github_update
   ```

7. コマンドプロンプトに以下を打ち込み、実行します。

   ```bash
   $ py discordbot.py
   ```

8. おつかれさまでした。

## setting.iniについて

| 設定項目| 説明|
| --- | --- |
| [TOKEN Setting] | BOTトークン  |
| [URL Setting]  | GitHubの各種URL |
| [Room Setting] | 権限ロール (rebootなどが使えるロール)の設定 |
| [FILE Setting] | ログファイルの設定 |

## 追加予定の機能
- プルリクエストの通知
- マージされたときの通知

## AWSメモ
0. [これ](https://dev.classmethod.jp/articles/creation_vpc_ec2_for_beginner_1/)とか[これ](https://dev.classmethod.jp/articles/creation_vpc_ec2_for_beginner_2/)をみながら頑張ってインスタンスを立ち上げる

1. 頑張ってSSH接続する. できない場合は[これ](https://xn--o9j8h1c9hb5756dt0ua226amc1a.com/?p=3583)とか参照

1. [このサイト](https://note.com/gotomaki/n/n8906f784e141)を参照してpython3.8をインストール
```bash
sudo which python3
echo 'alias python=python3.8' >> ~/.bashrc
source ~/.bashrc
sudo amazon-linux-extras enable python3.8
sudo yum install python3.8 -y
sudo which python3.8
echo 'alias python=python3.8' >> ~/.bashrc
 source ~/.bashrc

```
1. [このサイト](https://akizora.tech/amazon-linux-2-pip-install-4925)を参照してpipをインストール
```bash
sudo yum update
sudo yum install python-pip
```
1. gitを導入
```bash
sudo yum install git
```

1. なんか諸々ライブラリインストール

   ```bash
   $ python3.8 -m pip install git+https://github.com/Rapptz/discord.py
   $ python3.8 -m pip install PyNaCl
   $ python3.8 -m pip install requests
   ```

### 
## 更新履歴

- 20230303(かみみや)

  とりあえず動くようになった. 新しいIssueが生成されたら自動通知

- 20230310(かみみや)

  issue commentの更新を追加
