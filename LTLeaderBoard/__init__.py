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
def AddScore(name="Player", score=1, difficulty="Easy"):
    try:
        score = abs(int(score))
        db_connection = db.get_db()
        previous_score = db_connection.execute('SELECT * FROM scores WHERE name = ? AND difficulty = ?', (name, difficulty)).fetchone()
        if previous_score and previous_score['score'] < score:
            db_connection.execute('UPDATE scores SET name = ?, score = ? WHERE name = ? AND difficulty = ?', (name, score, name, difficulty))
            db_connection.commit()
            print("Score updated by client.")
            return "Score updated"
        elif previous_score and previous_score['score'] >= score:
            print("Score rejected by server as existing score already exists for player with a higher or equal value")
            return "Score not updated. Submitted score equal to or lower than existing value."
        else:
            db_connection.execute('INSERT INTO scores (name, score, difficulty) VALUES (?, ?, ?)',
            (name, score, difficulty))
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
            score['difficulty'] = row['difficulty']
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