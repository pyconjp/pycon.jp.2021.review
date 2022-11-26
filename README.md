# PyCon JP 2021 プロポーザルレビューアプリ

雰囲気を伝えるために静的化してGitHub Pagesにしています（ステージング環境のデータであり、実際のレビューではありません）

## 環境構築メモ

（[Issues](https://github.com/pyconjp/pycon.jp.2021.review/issues)を開発メモとして使っており、つまづいたときに参照できるドキュメント的な役割を果たせそう）

`docker compose up -d`  
ref: https://github.com/pyconjp/pycon.jp.2021.review/issues/1

ローカルで動かしたときにSlackアカウントでログインするには`python manage.py runsslserver`でサーバを動かす  
ref: https://github.com/pyconjp/pycon.jp.2021.review/issues/2

APIはToken認証で実装  
`curl http://127.0.0.1:8000/api/v1/auth/token/login/ --data 'username=管理者&password=ひみつ'`  
ref: https://github.com/pyconjp/pycon.jp.2021.review/issues/17
