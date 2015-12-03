import json
import sys

import model


session = model.get_session()


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
        session.commit()


if __name__ == '__main__':
    filenames = sys.argv[1:]

    for filename in filenames:
        print "Parsing file: {}".format(filename)
        parse_file(filename)
