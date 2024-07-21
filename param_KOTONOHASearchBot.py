# パラメーター項目 ###########################
# 音声・効果音ファイルは、WAVかMP3形式のみ対応しています。ファイルは[sound]フォルダに置いてください。
# 音声・効果音のボリュームは、0~100の範囲で指定して下さい。

# 無視ユーザーリスト
# 本リストに設定されたユーザーのコメントは無視します
IgnoreUsersList = ['Nightbot', 'StreamElements', 'moobot']
# 無視テキストリスト
# 本リストに設定されたテキストの含まれているメッセージは無視します
IgnoreTextList = ['http']

# コメントログ保存のON/OFF
IsSaveCommentsFile = False

# NGワード確認時に発言者へのリプライ
IsReplyWrongUser = True
# NGワードの音声のON/OFF
IsPlaySoundNGword = True
# NGワードの音声ファイル
NGwordSound = 'alert_echo.wav'
# NGワードの音声のボリューム
NGwordVolume = 50
