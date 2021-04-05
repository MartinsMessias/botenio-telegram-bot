#import redis
from flask import Flask
from flask.json import jsonify
from src.newsletter.news_letter import newsletter

app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess'


#cache = redis.from_url(os.environ.get("REDISTOGO_URL"))

@app.route('/', methods=['GET'])
def index():
    #newsletters = newsletter()
    return jsonify({'newsletter':'newsletter'})


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)