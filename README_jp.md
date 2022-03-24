# Task Master

![Screenshot of Application](screenshot1.png)

## 概要

これはタスク管理・ToDoリストのアプリケーションです。ユーザーはタスクを追加・削除・更新することができ、さらにチェックボックスにチェックを入れることでタスクのステータスを完了とすることができます。タスクはデータベース上で管理されています。タスクの更新はREST APIとJavaScriptのHTTPリクエストを利用し、それ以外の機能はサーバーサイドでレンダリングを行います。

このアプリの製作を通し、以下について練習しました:
- Python
- Flask 
- SQLAlchemy
- SQL Database
- Jinja2
- REST API
- HTML/CSS/JavaScript

## 要件
- Python 3.8+
- Python 3 Virtual Environment
- pip

## インストール
1. 仮想環境を作成し起動する
```shell
python3 -m venv venv 
source venv/bin/activate
```
2. 要件をインストールする
```shell
pip install -r requirements.txt
```

## 使用方法
1. サーバーを開始する
```shell
flask run
```
2. 右記のURLへアクセスする [http://127.0.0.1:5000/](http://127.0.0.1:5000/)