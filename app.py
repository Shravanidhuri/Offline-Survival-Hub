from flask import Flask, render_template, request, jsonify
import random
import time

app = Flask(__name__)

posts = []
votes = {}
messages = []

def random_mutation(text):
    if random.random() < 0.3:
        words = text.split()
        if words:
            index = random.randint(0, len(words)-1)
            words[index] = ''.join(random.sample(words[index], len(words[index])))
            return ' '.join(words)
    return text

def random_delete(items, chance=0.2):
    return [i for i in items if random.random() > chance]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/post', methods=['POST'])
def add_post():
    content = request.form.get('content')
    if content:
        posts.append(content)
    return jsonify(success=True, posts=posts)

@app.route('/vote', methods=['POST'])
def vote():
    name = request.form.get('name')
    choice = request.form.get('choice')
    if name and choice:
        votes[name] = choice
    return jsonify(success=True, votes=votes)

@app.route('/message', methods=['POST'])
def message():
    content = request.form.get('content')
    if content:
        timestamp = int(time.time())
        messages.append({'content': content, 'timestamp': timestamp})
    return jsonify(success=True)

@app.route('/status')
def status():
    global posts
    posts = [random_mutation(p) for p in posts]
    posts = random_delete(posts, chance=0.2)

    current_votes = votes.copy()
    for k in list(current_votes.keys()):
        if random.random() < 0.1:
            del votes[k]

    recent_messages = [m for m in messages if time.time() - m['timestamp'] < 3600]
    message_to_show = random.choice(recent_messages)['content'] if recent_messages else ""

    return jsonify(posts=posts, votes=votes, message=message_to_show)

if __name__ == '__main__':
    app.run(debug=True)
