#flaskモジュールの、Flaskクラスをインポート　他
from flask import Flask, render_template, url_for, request, redirect, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

#Flaskクラスのインスタンスを作成し、それを変数appに代入。第一引数として(__name__)を渡す
#appはこれから作るWebアプリの核となる
app = Flask(__name__)
#アクセスするDBの種類と位置を設定　種類はsqlite、位置は///の後ろに相対パスで記載(今回はファイル名のみ)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'  
#SQLAlchemyのインスタンスを作成し、それを変数dbに代入。第一引数として(app)を渡す
#dbを使ってデータベースを操作していく
db = SQLAlchemy(app)


class Todo(db.Model):   #TodoというDBのデータ型やデータの制約を記載
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)   #String(size)は文字列の上限
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    #__repr__()メソッドを使うことでクラスから作成したインスタンスのデータを文字列で表示できる
    #※作成したインスタンスを単純にprintすると、インスタンスの名前とアドレス(メモリの場所？)が返されてしまう
    def __repr__(self):
        return '<Task %r>' % self.id
    
    def to_dict(self):
        return {
            'id': self.id,
            'content': self.content,
            'completed': self.completed,
            'date_created': self.date_created
        }



@app.route('/', methods = ['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        print(task_content)
        new_task = Todo(content=task_content)
        print(new_task)
        if task_content:
            #通常の処理
            try:
                db.session.add(new_task)   #セッションに乗せる
                db.session.commit()   #DBに反映させる
                return redirect('/')
            #例外(エラー時)の処理    
            except Exception as e:   #エラー理由を出力
                print(e)
                return "There was an issue adding your task"
        else:
            print("empty")
            return redirect('/')

    else:
        #.query.order_byでタスク作成日昇順にソートする .all()を使ってリスト型で取得
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)


@app.route('/delete/<int:id>') #<>内に変数を入れられる　intなどの型の指定がない場合は文字列となる
def delete(id):
    #.query.get(PRIMARY KEY)でDBから削除するオブジェクトを取得
    #_or_404 を付けると、例えばユーザーが存在しないエンドポイントを表示しようとした場合、サーバーサイドまでいく必要なく、クライアントサイドでエラーであること(404)を表示できる
    task_to_delete = Todo.query.get_or_404(id)

    try:
        print (task_to_delete)
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')

    except:
        return "There was an issue deleting that task"


@app.route('/task/<int:id>', methods = ['PUT'])
def update(id):
    task = Todo.query.get(id)
    print(task)
    if not task:
        abort(404, {'code': 'Not found', 'message': 'task not found'})

    payload = request.json #JSON形式でPUTされたものを受け取る
    print(payload)

    completed = payload.get("completed", None)
    content = payload.get("content", None)

    if completed is not None:
        task.completed = completed

    if content is not None:
        task.content = content

    db.session.commit()
    return jsonify(task.to_dict())


#このファイルから実行されたらapp.runを実行する
if __name__ == "__main__":
    app.run(debug=True)


