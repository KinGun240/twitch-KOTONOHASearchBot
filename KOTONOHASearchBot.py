# Copyright 2024 KinGun
# This software is released under the MIT License, see LICENSE.

from twitchio import Channel, Message
from twitchio.ext import commands
import pygame.mixer
from pykakasi import kakasi

import sys
import os
import pandas as pd
import csv
from shutil import rmtree
import signal
import glob


# バージョン
ver = '1.0.0'

# 固定値
ErrorLogFile = "error.log"
CommentLogFile = "commentLog.csv"
NGwordListFile = "NGwordList.csv"


# 各種初期設定 #####################################
print(f"KOTONOHASearchBot ver is {ver}")

# エラーログのファイル出力
with open(ErrorLogFile, 'a') as errorFile:
    writer = csv.writer(errorFile)
    writer.writerow(['#Start Write'])
    errorFile.close()

# bot用コンフィグ(config.py)の読み込み
import importlib
try:
    sys.path.append(os.path.dirname(sys.argv[0]))
#    sys.path.append(os.path.join(os.path.dirname(__file__), '.'))
    configKOTONOHASearch = importlib.import_module('config')
    print("Read config.py")
    # remove "#" mark ------
    if configKOTONOHASearch.Twitch_ChannelName.startswith('#'):
        print("Find # mark at channel name! I remove '#' from 'config:Twitch_ChannelName'")
        configKOTONOHASearch.Twitch_ChannelName = configKOTONOHASearch.Twitch_ChannelName[1:]
    # remove "oauth:" mark ------
    if configKOTONOHASearch.Bot_OAUTH.startswith('oauth:'):
        print("Find 'oauth:' at OAUTH text! I remove 'oauth:' from 'config:Bot_OAUTH'")
        configKOTONOHASearch.Bot_OAUTH = configKOTONOHASearch.Bot_OAUTH[6:]
except Exception as e:
    print(e)
    print('Please make [config.py] and put it with KOTONOHASearchBot')
    with open(ErrorLogFile, 'a') as errorFile:
        writer = csv.writer(errorFile)
        writer.writerow([e])
        errorFile.close()
    input()  # stop for error!!


# KOTONOHASearchBot用パラメーター(param_KOTONOHOSearchBot.py)の読み込み
try:
    KOTONOHASearchParam = importlib.import_module('param_KOTONOHASearchBot')
    print("Read param_KOTONOHASearchBot.py")
except Exception as e:
    print(e)
    print('Please make [param_KOTONOHASearchBot.py] and put it with KOTONOHASearchBot')
    with open(ErrorLogFile, 'a') as errorFile:
        writer = csv.writer(errorFile)
        writer.writerow([e])
        errorFile.close()
    input()  # stop for error!!


# 内部変数の設定 ----------
# NGワードリストの読み込み
try:
    NGwordList = pd.read_csv(f"./data/{NGwordListFile}")
    print(f"Read {NGwordListFile}")
except Exception as e:
    print(e)
    print(f'Please check [{NGwordListFile}] and put it with data folder')
    with open(ErrorLogFile, 'a') as errorFile:
        writer = csv.writer(errorFile)
        writer.writerow([e])
        errorFile.close()
    input()

# 無視ユーザリストの準備
try:
    IgnoreUserList = [x.strip() for x in KOTONOHASearchParam.IgnoreUsersList]
    IgnoreUserList = [str.lower() for str in IgnoreUserList]
    print(f'IgnoreUserList:{IgnoreUserList}')
except Exception as e:
    print(e)
    print('Please check [param_KOTONOHASearchBot.py] and put it with KOTONOHASearchBot')
    with open(ErrorLogFile, 'a') as errorFile:
        writer = csv.writer(errorFile)
        writer.writerow([e])
        errorFile.close()
    input()

# 無視テキストリストの準備
try:
    IgnoreTextList = [x.strip() for x in KOTONOHASearchParam.IgnoreTextList]
    print(f'IgnoreTextList:{IgnoreTextList}')
except Exception as e:
    print(e)
    print('Please check [param_KOTONOHASearchBot.py] and put it with KOTONOHASearchBot')
    with open(ErrorLogFile, 'a') as errorFile:
        writer = csv.writer(errorFile)
        writer.writerow([e])
        errorFile.close()
    input()

# 音量初期設定
try:
    pygame.mixer.init(frequency=44100)
except Exception as e:
    print(e)
    print('Please check pygame')
    with open(ErrorLogFile, 'a') as errorFile:
        writer = csv.writer(errorFile)
        writer.writerow([e])
        errorFile.close()
    input()


# botクラス #####################################
class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            token="oauth:" + configKOTONOHASearch.Bot_OAUTH,
            client_id="",
            nick=configKOTONOHASearch.Bot_ChannelName,
            prefix=configKOTONOHASearch.BOT_PREFIX,
            initial_channels=[configKOTONOHASearch.Twitch_ChannelName]
        )

    # bot起動時処理 ----------
    async def event_channel_joined(self, channel: Channel):
        print(f"{configKOTONOHASearch.Bot_ChannelName}が監視を始めました")
#        await channel.send(configKOTONOHASearch.Twitch_ChannelName, f"/color {configKOTONOHASearch.TextColor}")
        await channel.send(f"{configKOTONOHASearch.Bot_ChannelName}が監視を始めました")

        # 書き込み開始のファイル出力
        if KOTONOHASearchParam.IsSaveCommentsFile:
            with open(CommentLogFile, 'a') as commentsFile:
                writer = csv.writer(commentsFile)
                writer.writerow(['#Start Write Comments'])
                commentsFile.close()
            print(f'{CommentLogFile}にコメント保存を開始します')


    # メッセージ受信時処理 ----------
    async def event_message(self, message: Message):
        # ユーザー・メッセージチェック処理 ----------
        # ボットの発言は無視する
        if message.echo:
            return

        # メッセージがコマンドであれば、ここで処理を終了
        if message.content.startswith(configKOTONOHASearch.BOT_PREFIX):
            await self.handle_commands(message)
            return

        # データ取得 ----------
        IsNGword = False
        user = message.author.name
        name = message.author.display_name
        msg = message.content
        uptime = (pd.Timestamp(message.timestamp, unit='s', tz='UTC')
                ).tz_convert('Asia/Tokyo')
        print(f'\nTIME:{uptime}\nUSER:{user}\nNAME:{name}\nMSG:{msg}')

        # 無視リスト処理 ----------
        # ユーザーが無視ユーザーリストに含まれる場合は処理終了
        if user in IgnoreUserList:
            print(f'{user} matched IgnoreUserList')
            return

        # メッセージが無視テキストリストに含まれる場合は処理終了
        for word in IgnoreTextList:
            if word in msg:
                print(f'{msg} matched IgnoreTextList')
                return

        # NGワード処理 ----------
        # 句読点などの消去
        msg = msg.replace("、","")
        msg = msg.replace("。","")
        msg = msg.replace("！","")
        msg = msg.replace("？","")

        #NGワードチェック
        ng_word_list = []
        self.kakasi= kakasi()
        results  = self.kakasi.convert(msg)
        text = "".join([x["hira"] for x in results])
        print(f' -> hiragana_mesage:{text}')
        for index, row in NGwordList.iterrows():
            for word in row:
                if word in text and word != "":
                    #print('\033[35m'+f'{word.upper()}'+'\033[0m')
                    ng_word_list.append(f'{word.upper()}' + '->' + NGwordList.at[index, 'Key'])
                    print(f' -> NGword:{word.upper()}')
        if ng_word_list:
            IsNGword = True

        # 音声・メッセージ処理 ----------
        # 各フラグ状態に応じてメッセージ出力
        try:
            if KOTONOHASearchParam.IsReplyWrongUser and IsNGword:
                out_text = f'{name}:' + ", ".join(ng_word_list)
                await message.channel.send("/me " + out_text)
                print(f'BotMessage:{out_text}')

        except Exception as e:
            print('message send error')
            with open(ErrorLogFile, 'a') as errorFile:
                writer = csv.writer(errorFile)
                writer.writerow([e])
                errorFile.close()

        # 各フラグ状態に応じて音声出力
        try:
            if KOTONOHASearchParam.IsPlaySoundNGword and IsNGword:
                volume = setLimit(KOTONOHASearchParam.NGwordVolume, 0, 100) / 100.0
                playSoundpg(f"./sound/{KOTONOHASearchParam.NGwordSound}", volume)
                print(f'BotSound:{KOTONOHASearchParam.NGwordSound}')

        except Exception as e:
            print('sound error: Please check [config.py] and sound folder...')
            with open(ErrorLogFile, 'a') as errorFile:
                writer = csv.writer(errorFile)
                writer.writerow([e])
                errorFile.close()

        # その他処理 ----------
        # コメントログ保存処理:タイムスタンプ、ユーザー名、コメント内容
        try:
            if KOTONOHASearchParam.IsSaveCommentsFile:
                with open(CommentLogFile, 'a') as commentsFile:
                    writer = csv.writer(commentsFile)
                    writer.writerow([uptime, user, msg])
                    commentsFile.close()
        except Exception as e:
            print(f'file error: [{CommentLogFile}] can not save...')
            with open(ErrorLogFile, 'a') as errorFile:
                writer = csv.writer(errorFile)
                writer.writerow([e])
                errorFile.close()


# 汎用関数 #####################################
# pygameを利用して音を鳴らす ----------
def playSoundpg(filename, volume):
    if filename:
        if not volume:
            volume = 1.0
        pygame.mixer.music.load(filename)
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play()


# 入力値を上限・下限の飽和値に制限する -------------
def setLimit(input, min, max):
    if input < min:
        return min
    if input > max:
        return max
    return input


#####################################
# 最後のクリーンアップ処理 -------------
def cleanup():
    print("!!!Clean up!!!")

    # Cleanup処理いろいろ

    # time.sleep(1)
    print("!!!Clean up Done!!!")


#####################################
# sig handler  -------------
def sig_handler(signum, frame) -> None:
    sys.exit(1)


#####################################
# _MEI cleaner  -------------
# Thanks to Sadra Heydari
# @ https://stackoverflow.com/questions/57261199/
#   python-handling-the-meipass-folder-in-temporary-folder
def CLEANMEIFOLDERS():
    try:
        base_path = sys._MEIPASS

    except Exception:
        base_path = os.path.abspath(".")

    base_path = base_path.split("\\")
    base_path.pop(-1)
    temp_path = ""
    for item in base_path:
        temp_path = temp_path + item + "\\"

    mei_folders = [f for f in glob.glob(temp_path + "**/", recursive=False)]
    for item in mei_folders:
        if item.find('_MEI') != -1 and item != sys._MEIPASS + "\\":
            rmtree(item)


# メイン処理 ###########################
def main():
    signal.signal(signal.SIGTERM, sig_handler)

    try:
        # 以前に生成された _MEI フォルダを削除する
        CLEANMEIFOLDERS()

        # bot起動
        bot = Bot()
        bot.run()

    except Exception as e:
        input()  # stop for error!!

    finally:
        signal.signal(signal.SIGTERM, signal.SIG_IGN)
        signal.signal(signal.SIGINT, signal.SIG_IGN)
        cleanup()
        signal.signal(signal.SIGTERM, signal.SIG_DFL)
        signal.signal(signal.SIGINT, signal.SIG_DFL)


if __name__ == "__main__":
    sys.exit(main())
