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

@jsonrpc.method('app.AddScore')
def AddScore(name="Player", score=1):
    try:
        score = abs(int(score))
        db_connection = db.get_db()
        previous_score = db_connection.execute('SELECT * FROM scores WHERE name = ?', (name, )).fetchone()
        if previous_score:
            db_connection.execute('UPDATE scores SET name = ?, score = ? WHERE name = ?', (name, score, name))
            db_connection.commit()
            print("Score updated by client.")
            return "Score updated"
        else:
            db_connection.execute('INSERT INTO scores (name, score) VALUES (?, ?)',
            (name, score))
            db_connection.commit()
            print("Score added by client.")
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
        print("Received request to get scores")
        return json.dumps(scores)
    except:
        print_exc()
        raise ValueError
    finally:
        db.close_db()
        

if __name__ == "__main__":
    app.run()