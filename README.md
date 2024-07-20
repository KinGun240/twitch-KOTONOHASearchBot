# 概要
Twitchのチャット欄のコメントに含まれるNGワードを監視するBotです。  
つまりアレです。  
NGワードを察知すると、発言者へのリプライと、音声を流します。
**音声はbotを起動しているPC上で鳴るので、必要に応じて配信に取り込むようにして下さい。**  

# 導入手順
## 事前準備
1. Bot用Twitchアカウントを作成します。  
2. Bot用アカウントでTwitchにサインインした状態で、下記のURLからOAuthパスワードを取得します。  
   https://twitchapps.com/tmi/
3. [config.py]の＊＊＊＊＊となっている個所の情報を書き換えます。  
   Bot_OAUTH = '＊＊＊＊＊'の＊＊＊＊＊には、上記2.で取得したOAuthパスワードを記載してください。  
4. Twitch_ChannelNameの**********は、Botを常駐させるTwitchチャンネル名に書き換えてください。
   Bot_ChannelNameの**********は、BotのTwitchチャンネル名(アカウント名)に書き換えてください(1.で取得したもの)。

## 使用方法
1. [config.py]の＊＊＊＊＊となっていない項目も、必要に応じて書き換えてください。  
2. [param_KOTONOHASearchBot.py]の各項目について、必要に応じて書き替えてください。  
3. 必要であれば、[sound]フォルダに鳴らしたい音声ファイルを追加します(WAV、MP3形式)。  
   デフォルトで鳴らすファイルが入っているので、そのままでよければ変更不要です。  
4. [data]フォルダの各ファイルについて、必要に応じて書き替えてください。  
5. [KOTONOHASearchBot.exe]を実行します。実行後、黒いウィンドウが表示されます。  
   Botの起動に成功した場合、Twitchのチャット欄に"[Bot名]が監視を始めました"と表示されます。  

# 機能説明
* **コメントログ保存**  
  チャット欄のコメントを、CSVファイルに保存します。
  > ファイルへの保存については、[param_KOTONOHASearchBot.py]からON/OFFが可能です。
* **NGワード察知**  
  コメントにNGワードが存在する場合、[param_KOTONOHASearchBot.py]で指定された音声を鳴らします。  
  > 音声については、[param_KOTONOHASearchBot.py]からON/OFFが可能です。  
  > 鳴らす音声ファイルは、[param_KOTONOHASearchBot.py]から変更が可能です。

# その他
本ソフトウェアを利用した場合の一切の責任を私は負いません、よろしくお願いします。  
本ソフトウェアを使用する場合、配信概要欄に記載するやら、下記連絡先のどっかに一言あると喜びます。  
* Mail  
  kingunsq@gmail.com
* Twitter  
  https://twitter.com/Kin_Gun_
* Github  
  https://github.com/KinGun240

素材はこちらからお借りしました。
わたおきば(https://wataokiba.net/)

## 参考
* [Twitchにチャット翻訳botを導入する](https://note.com/tatsuya_iwama/n/nc42feebbb53d)
* [翻訳ちゃんFreeNextの導入・使用方法](https://croom.sytes.net/trans/)
* [TwitchIOでTwitchのBotを作る](https://qiita.com/maguro869/items/57b866779b665058cfe8)

## 動作環境
* OS  
  Windows 10(64bit)でのみ動作確認しています。  
  MacOSへの対応予定は今のところないです。  

## ファイル構成
<details>
<summary>見たい方はどうぞ</summary>

* KOTONOHASearchBot.exe  
  本体となる実行ファイルです。無いと動きません。  
* KOTONOHASearchBot.py  
  ソースコードです。無くても動きます。  
* config.py  
  設定ファイルです。動作に必要な設定です。  
* param_KOTONOHASearchBot.py  
  パラメーターファイルです。挙動変更ための設定です。  
* Readme.md  
  説明書です。今読んでるコレ。  
* LICENSE  
  ライセンスに関して記載したファイルです。  
* [data]フォルダ  
  取得して保存するデータに関するファイルを置くフォルダです。  
  - manual.md  
    本フォルダに保存されている各ファイルの詳細について説明したファイルです。  
  - NGwordList.csv  
    NGワードを保存したファイルです。  
* [sound]フォルダ  
  音声ファイルを置くフォルダです。  
  - alert_echo.wav
    NGワード察知時に鳴らす音声ファイルです。ﾌﾟｧｰﾝ
</details>

## 更新履歴
### 最新バージョンへの更新方法
* バージョン X.Y.ZのZが異なる場合  
  1. KOTONOHASearchBot.exeのみをダウンロードし、差し替えてください。  
  2. もしくは、最新バージョン一式をダウンロードし、解凍したフォルダに対して、  
     以下のファイルを以前のバージョンのフォルダからコピーして下さい。  
   - config.py
   - param_KOTONOHASearchBot.py
   - [data]フォルダ
   - [sound]フォルダ

* バージョン X.Y.ZのXかYが異なる場合  
  1. 最新バージョン一式をダウンロードし、解凍したフォルダに対して、  
     以下のファイルを以前のバージョンのフォルダからコピーして下さい。  
   - config.py
   - [data]フォルダ
   - [sound]フォルダ
  2. 以下のファイルについて、以前のバージョンのファイルを参考にし、  
     最新バージョンのファイルの設定項目を書き換えてください。  
   - param_KOTONOHASearchBot.py

### 最新更新情報
* バージョン 1.0.1 - 2024/07/21
  - NGwordListの1行目を消去、それに伴う処理の変更

* バージョン 1.0.0 - 2024/07/20
  - 新規作成

<details>
<summary>過去の履歴</summary>

</details>

## License
The source code is licensed MIT.
