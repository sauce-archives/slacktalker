from flask import Flask
app = Flask(__name__)

import make_sentence
import model


@app.route('/generate/<username>/')
def generate(username):
    return make_sentence.make_sentence(username)


@app.route('/users/')
def users():
    session = model.get_session()
    return " ".join([u.name for u in session.query(model.User).all()])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
