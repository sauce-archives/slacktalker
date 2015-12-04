import json
import os
import pickle
import sys

import model


# Keep track of the last loaded version of each channel
MEMORY = 'pickle.db'
try:
    with open(MEMORY, 'rb') as f:
        memory = pickle.load(f)
except IOError:
    memory = {}


def get_last_loaded(channel):
    return memory.get(channel)


def set_last_loaded(channel, last_loaded):
    memory[channel] = last_loaded


def save_memory():
    with open(MEMORY, 'wb') as f:
        pickle.dump(memory, f)


session = model.get_session()


def get_channel_name_and_date(filename):
    channel = os.path.split(os.path.split(filename)[0])[1]
    date = os.path.split(filename)[1].split('.json')[0]
    return channel, date


def parse_file(filename):
    with open(filename, 'rb') as f:
        data = json.loads(f.read())
    for item in data:
        """
        {
            "type": "message",
            "user": "U02FVR4ND",
            "text": "isaac: we're heading to dinner around 7pm",
            "ts": "1409746135.000671"
        }
        """
        # Only messages
        if item['type'] != 'message':
            continue
        # Skip bots
        if 'bot_id' in item:
            continue
        # Ignore edits
        if 'subtype' in item:
            continue
        words = item['text'].split()
        for i in xrange(len(words) + 1):
            user = item['user']
            word_prev = words[i - 1].lower()[:254] if i > 0 else ''
            word_next = words[i].lower()[:254] if i < len(words) else ''
            word_entry = session.query(model.WordEntry).filter(
                model.WordEntry.user==user,
                model.WordEntry.word_prev==word_prev,
                model.WordEntry.word_next==word_next).first()
            if not word_entry:
                word_entry = model.WordEntry()
                word_entry.user = user
                word_entry.word_prev = word_prev
                word_entry.word_next = word_next
                word_entry.count = 0
            word_entry.count += 1
            session.add(word_entry)

        #two word combos
        for i, word_next in enumerate(words):
            if i<2:
                continue
            word_prev = '%s %s' % (words[i-2].lower()[:254], words[i-1].lower()[:254] )
            word_entry = session.query(model.WordEntry).filter(
                model.WordEntry.user==user,
                model.WordEntry.word_prev==word_prev,
                model.WordEntry.word_next==word_next).first()
            if not word_entry:
                word_entry = model.WordEntry()
                word_entry.user = user
                word_entry.word_prev = word_prev
                word_entry.word_next = word_next
                word_entry.count = 0
            word_entry.count += 1
            
            session.add(word_entry)

        session.commit()


if __name__ == '__main__':
    filenames = sys.argv[1:]

    for filename in filenames:
        channel, date = get_channel_name_and_date(filename)
        last_loaded = get_last_loaded(channel)
        if last_loaded >= date:
            print "Skipping file: {}.  Already loaded up to {} for channel {}"\
                .format(filename, last_loaded, channel)
        else:
            print "Parsing file: {}".format(filename)
            parse_file(filename)
            set_last_loaded(channel, date)
            save_memory()
