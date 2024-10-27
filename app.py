import os
from os.path import join, dirname
from dotenv import load_dotenv

from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient


dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URL = os.environ.get("MONGODB_URL")
DB_NAME = os.environ.get("DB_NAME")

client = MongoClient(MONGODB_URL)
db = client[DB_NAME]

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/diary', methods=['GET'])
def show_diary():
    articles = list(db.diary.find({}, {'_id': False}))
    return jsonify({'articles': articles})

@app.route('/diary', methods=['POST'])
def save_diary():
    file = request.files['file_give']
    extension = file.filename.split('.')[-1]
    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')
    filename = f'file-{mytime}.{extension}'
    save_to = f'static/{filename}'
    file.save(save_to)

    profile = request.files['profile_give']
    profile_extension = profile.filename.split('.')[-1]
    profile_name = f'profile-{mytime}.{profile_extension}'
    profile_save_to = f'static/{profile_name}'
    profile.save(profile_save_to)

    title_receive = request.form.get('title_give')
    content_receive = request.form.get('content_give')

    doc = {
        'file': filename,
        'profile': profile_name,
        'title': title_receive,
        'content': content_receive,
        'time': today.strftime('%Y.%m.%d'),
    }

    db.diary.insert_one(doc)
    return jsonify({'message': 'Data was saved!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
