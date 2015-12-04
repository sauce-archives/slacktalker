import sys, math, random

import model
from model import WordEntry

from sqlalchemy.sql.expression import func
from sqlalchemy import Column, Integer, MetaData, String, Table, desc

#for each possible next word sampled from the crowd, generate PERSONALITY_WEIGHT entries from the actual user
WORD_PAIRS_WEIGHT = 1
SENTENCE_WORD_LIMIT = 100

session = model.get_session()

def get_next_word(user, word, last_words):
    user_words = session.query(WordEntry)\
            .filter(WordEntry.user == user.id, WordEntry.word_prev == word)\
            .order_by(desc(WordEntry.count)).limit(10)

    user_word_pairs = session.query(WordEntry)\
            .filter(WordEntry.user == user.id, WordEntry.word_prev == last_words)\
            .order_by(desc(WordEntry.count)).limit(10)

    candidates = []
    for w in user_words:
        candidates.append(w.word_next)

    for w in user_word_pairs:
        for i in range(WORD_PAIRS_WEIGHT):
            candidates.append(w.word_next)

    result = random.choice(candidates)
    return result

def make_sentence(username, prompt=""):
    sentence = ''
    # Try to find the user
    user = session.query(model.User).filter(model.User.name==username).first()
    if not user:
        raise Exception('Username {} not found'.format(username))

    sentence = ''
    # there's probably a nicer way to write this
    if prompt: # Load up an initial word
        word = session.query(model.WordEntry)\
            .filter(model.WordEntry.user == user.id, model.WordEntry.word_prev == prompt)\
            .order_by(func.rand()).first()
    if word:
        sentence += word.word_prev + " "
    else:
        word = session.query(model.WordEntry)\
            .filter(model.WordEntry.user == user.id, model.WordEntry.word_prev == '')\
            .order_by(func.rand()).first()
    word = word.word_next
    sentence += word
    for i in xrange(SENTENCE_WORD_LIMIT):
        last_words = ' '.join(sentence.split()[-2:])
        word = get_next_word(user, word, last_words)
        if word:
            sentence += ' ' + word
        else:
            break
    return sentence

