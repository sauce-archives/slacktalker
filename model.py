# coding: utf-8
from sqlalchemy import Column, Integer, MetaData, String, Table, desc
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm import sessionmaker
import random


Base = declarative_base()


class WordEntry(Base):

    __tablename__ = 'word_entries'

    user = Column('user', String(9), primary_key=True)
    word_prev = Column('word_prev', String(255), primary_key=True)
    word_next = Column('word_next', String(255), primary_key=True)
    count = Column('count', Integer, nullable=False, index=True)

    def __repr__(self):
        return "<model.WordEntry '{}:{}:{}'>".format(self.user, self.word_prev,
                                                     self.word_next)

    def next(self, session):
        words = session.query(WordEntry)\
            .filter(WordEntry.word_prev == self.word_next)\
            .order_by(desc(WordEntry.count)).limit(10)
        return random.choice(list(words))


class User(Base):

    __tablename__ = 'users'

    id = Column('id', String(9), primary_key=True)
    name = Column('name', String(255))
    real_name = Column('real_name', String(255))
    first_name = Column('first_name', String(255))
    last_name = Column('last_name', String(255))
    image_24 = Column('image_24', String(255))
    image_32 = Column('image_32', String(255))
    image_48 = Column('image_48', String(255))
    image_72 = Column('image_72', String(255))
    image_192 = Column('image_192', String(255))
    image_original = Column('image_original', String(255))

    def __repr__(self):
        return "<model.User '{} - {}'>".format(self.name.encode('utf8'),
                                               self.real_name.encode('utf8'))


def get_session():
    engine = create_engine(
        'mysql://root:***REMOVED***@localhost/slacktalker?charset=utf8')
    Session = sessionmaker(bind=engine)
    return Session()


if __name__ == '__main__':
    engine = create_engine('mysql://root:***REMOVED***@localhost/?charset=utf8')
    engine.execute(
        """
        CREATE DATABASE IF NOT EXISTS slacktalker
          DEFAULT CHARACTER SET = 'utf8'
          DEFAULT COLLATE 'utf8_general_ci';""")
    engine.execute("USE slacktalker")
    Base.metadata.create_all(engine)
