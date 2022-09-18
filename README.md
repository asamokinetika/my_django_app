# my_django_app
自作のチャットアプリです

## 内容
Djangoを利用して作成した、チャットアプリです。ユーザー登録、ログイン、フレンド登録、グループ作成・登録、チャットが主な機能です。channelsを用いたWebsocketにより、リアルタイムで
チャットが可能です。

## 使い方
①Dockerが使える環境を構築してください

②my.cnfを読み取り専用ファイルに設定してください

③docker-compose　up -d でコンテナを立ち上げてください

④mediaディレクトリにimageというディレクトリを作ってください

⑤docker-compose  exec web bash　でDjangoが立ち上がっているコンテナに入ってください

⑦コンテナ内でコマンド　python manage.py makemigrations　でマイグレーションファイルを作成してください

⑧同じくコンテナ内でコマンド　python manage.py　migrate でマイグレートしてください

⑨localhost:8000/sns　をブラウザで開けばトップページにつながるはずです（もしうまくいかなければ、まずコンテナを再起動してみてください）
