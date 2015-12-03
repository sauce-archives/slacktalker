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
            "id": "U02HCHXGE",
            "team_id": "T024TC0TE",
            "name": "allison",
            "deleted": false,
            "status": null,
            "color": "8469bc",
            "real_name": "Allison Wilbur",
            "tz": "America\/Los_Angeles",
            "tz_label": "Pacific Standard Time",
            "tz_offset": -28800,
            "profile": {
                "first_name": "Allison",
                "last_name": "Wilbur",
                "title": "Support Ninja",
                "skype": "allison.wilbur",
                "phone": "5129442311",
                "image_24": "https:\/\/avatars.slack-edge.com\/2014-08-28\/2593251567_24.jpg",
                "image_32": "https:\/\/avatars.slack-edge.com\/2014-08-28\/2593251567_32.jpg",
                "image_48": "https:\/\/avatars.slack-edge.com\/2014-08-28\/2593251567_48.jpg",
                "image_72": "https:\/\/avatars.slack-edge.com\/2014-08-28\/2593251567_72.jpg",
                "image_192": "https:\/\/avatars.slack-edge.com\/2014-08-28\/2593251567_72.jpg",
                "image_original": "https:\/\/avatars.slack-edge.com\/2014-08-28\/2593251567_original.jpg",
                "fields": {
                    "Xf0D7F040P": {
                        "value": "allison.wilbur",
                        "alt": ""
                    }
                },
                "real_name": "Allison Wilbur",
                "real_name_normalized": "Allison Wilbur",
                "email": "allison@saucelabs.com"
            },
            "is_admin": false,
            "is_owner": false,
            "is_primary_owner": false,
            "is_restricted": false,
            "is_ultra_restricted": false,
            "is_bot": false
        },
        """
        # Skip bots
        if item.get('bot'):
            continue
        user = model.User(
            id=item['id'],
            name=item['name'],
            real_name=item['profile'].get('real_name', ''),
            first_name=item['profile'].get('first_name', ''),
            last_name=item['profile'].get('last_name', ''),
            image_24=item['profile'].get('image_24', ''),
            image_32=item['profile'].get('image_32', ''),
            image_48=item['profile'].get('image_48', ''),
            image_72=item['profile'].get('image_72', ''),
            image_192=item['profile'].get('image_192', ''),
            image_original=item['profile'].get('image_original', ''),
        )
        session.merge(user)
        session.commit()

        """
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
        """


if __name__ == '__main__':
    # Look for users.json
    assert len(sys.argv) == 2
    filename = sys.argv[1]
    print "Parsing file: {}".format(filename)
    parse_file(filename)
