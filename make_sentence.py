import sys

import model

from sqlalchemy.sql.expression import func


SENTENCE_WORD_LIMIT = 100


session = model.get_session()


def make_sentence(username):

    # Try to find the user
    user = session.query(model.User).filter(
        model.User.name==username).first()
    if not user:
        raise Exception('Username {} not found'.format(username))

    sentence = ''
    # Load up an initial random word
    word = session.query(model.WordEntry)\
        .filter(model.WordEntry.user == user.id, model.WordEntry.word_prev == '')\
        .order_by(func.rand()).first()
    sentence += word.word_next
    for i in xrange(SENTENCE_WORD_LIMIT):
        word = word.next(session)
        if word.word_next:
            sentence += ' ' + word.word_next
        else:
            break
    return "*{}:* ".format(str(user)) + sentence
