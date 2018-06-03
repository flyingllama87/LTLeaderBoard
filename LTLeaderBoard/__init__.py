from flask import Flask
from flask_jsonrpc import JSONRPC
import os
from traceback import print_exc
from pprint import pprint
import json

from LTLeaderBoard import db

app = Flask(__name__)

jsonrpc = JSONRPC(app, '/api')

db.init_app(app)

@jsonrpc.method('app.index')
def index():
    return u'Welcome to flask JSON-RPC!'

@jsonrpc.method('app.hello')
def hello(name="world"):
    return "Hello, %s!" % name

@jsonrpc.method('app.AddScore')
def AddScore(name="Player", score=1):
    try:
        db_connection = db.get_db()
        db_connection.execute('INSERT INTO scores (name, score) VALUES (?, ?)',
        (name, score))
        db_connection.commit()
        return "Score added"
    except:
        print_exc()
        raise ValueError
    finally:
        db.close_db()

@jsonrpc.method('app.GetScores')
def GetScores():
    try:
        db_connection = db.get_db()
        db_scores = db_connection.execute('SELECT * FROM scores ORDER BY score DESC').fetchall()
        scores = []
        for row in db_scores:
            score = {}
            score['name'] = row['name']
            score['score'] = row['score']
            scores.append(score)
        print(scores[0]['score'])
        print(scores[0]['name'])
        print(json.dumps(scores))
        print(type(scores))
        print(type(json.dumps(scores)))
        return json.dumps(scores)
    except:
        print_exc()
        raise ValueError
    finally:
        db.close_db()
        

if __name__ == "__main__":
    app.run()