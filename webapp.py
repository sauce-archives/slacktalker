from flask import Flask
app = Flask(__name__)

import talker_exceptions as exceptions
import make_sentence
import model


@app.route('/generate/<username>/')
def generate(username):
    try:
        return make_sentence.make_sentence(username)
    except exceptions.TalkerException as e:
        return str(e)


@app.route('/users/')
def users():
    session = model.get_session()
    return ", ".join(["{} ({})".format(u.name.encode('utf8'), str(u))
                      for u in session.query(model.User).all()])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
