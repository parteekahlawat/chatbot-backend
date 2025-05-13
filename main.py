import os
from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
from redis import Redis
from flask_cors import CORS

import json
from search_and_llm import searchQuery
from scrape import scrapeData
from embedding_and_store import embedding_store
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

socketio = SocketIO(app, cors_allowed_origins="*")

redis = Redis(host=os.getenv("REDIS_HOST"), port=os.getenv("REDIS_PORT"))


@app.route('/')
def index():
    return "Chat Server is running!"

@app.route('/history/<session_id>', methods=['GET'])
def get_session_history(session_id):
    try:
        history = redis.lrange(session_id, 0, -1) 
        return jsonify({"history": [(msg.decode('utf-8')) for msg in history]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    
@app.route('/clear_session/<session_id>', methods=['GET'])
def clear_session(session_id):

    redis.delete(session_id)
    return jsonify({"message": "Session cleared successfully!"})

@socketio.on('message')
def handle_message(data):
    session_id = data['session_id']
    message = data['message']

    response = searchQuery(message)
    
    message_data = json.dumps({"sender": "user","message": message})
    redis.rpush(session_id, (message_data)) 
    
    message_data = json.dumps({"sender": "assistant","message": response})
    redis.rpush(session_id, (message_data)) 
    
    print(f"Session {session_id} message count:", redis.llen(session_id))
    emit('response', {'message': response}, broadcast=True)


if __name__ == '__main__':

    redis.ping()
    print("Connected to Redis")
    scrapeData()
    embedding_store()
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
