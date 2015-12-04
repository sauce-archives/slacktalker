import sys, math, random

import model
from model import WordEntry

from sqlalchemy.sql.expression import func
from sqlalchemy import Column, Integer, MetaData, String, Table, desc

#for each possible next word sampled from the crowd, generate PERSONALITY_WEIGHT entries from the actual user
PERSONALITY_WEIGHT = 15
SENTENCE_WORD_MINIMUM = 2
SENTENCE_WORD_LIMIT = 100

session = model.get_session()

def get_next_word(user, word):
    words = session.query(WordEntry)\
            .filter(WordEntry.word_prev == word)\
            .order_by(desc(WordEntry.count)).limit(10)

    user_words = session.query(WordEntry)\
            .filter(WordEntry.user == user.id, WordEntry.word_prev == word)\
            .order_by(desc(WordEntry.count)).limit(10)

    candidates = []
    for w in user_words:
        for i in range(PERSONALITY_WEIGHT):
            candidates.append(w.word_next)
        
    for w in words:
        candidates.append(w.word_next)

    result = random.choice(candidates)
    return result

def make_sentence(username):
    sentence = ''
    while len(sentence.split(' ')) < SENTENCE_WORD_MINIMUM:
        # Try to find the user
        user = session.query(model.User).filter(model.User.name==username).first()
        if not user:
            raise Exception('Username {} not found'.format(username))

        sentence = ''
        # Load up an initial random word
        word = session.query(model.WordEntry)\
            .filter(model.WordEntry.user == user.id, model.WordEntry.word_prev == '')\
            .order_by(func.rand()).first()

        next_word = word.word_next
        sentence += next_word
        for i in xrange(SENTENCE_WORD_LIMIT):
            next_word = get_next_word(user, next_word)
            if next_word:
                sentence += ' ' + next_word
            else:
                break
    return sentence
