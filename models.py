import os
import json
from sqlalchemy import ForeignKey, Column, String, Integer
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

database_name = "divebeapp"
# database_path = "postgres://{}/{}".format('localhost:5432', database_name)
# database_path = "postgres:///{}".format(database_name)
# database_path = os.environ['DATABASE_URL']
database_path = 'postgres://iyzmytehxnmvss:31dfdacfa9c474f8beb9405061bce84c8500939f18683a39f53ec0e2becce5ed@ec2-52-22-136-117.compute-1.amazonaws.com:5432/d5q2mtc9cm2a76'
db = SQLAlchemy()

# ------------------------------------------------------------------------------#
# setup_db(app)
# binds a flask application and a SQLAlchemy service
# ------------------------------------------------------------------------------#


def setup_db(app, database_path=database_path):

    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    migrate = Migrate(app, db)

# ------------------------------------------------------------------------------#
# Data Model
# ------------------------------------------------------------------------------#

class Musician(db.Model):

    __tablename__ = 'musician'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)
    e_mail = Column(String(120))
    phone = Column(String(120))
    website = Column(String(500))
    introduction = Column(String(120))
    avatar_link = Column(String())
    genres = Column(String(120))
    songs = relationship('Song', backref='musicians', lazy=True, cascade="save-update, merge, delete")
    
    def __init__(self, name, e_mail, phone, website, introduction, avatar_link, genres):
        self.name = name
        self.e_mail = e_mail
        self.phone = phone
        self.website = website
        self.introduction = introduction
        self.avatar_link = avatar_link
        self.genres = genres


    def add(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        # db.session.update(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'e_mail': self.e_mail,
            'phone' : self.phone,
            'website': self.website,
            'introduction' : self.introduction,
            'avatar_link' : self.avatar_link,
            'genres' : self.genres,
            'songs': list(map(lambda song: song.format(), self.songs))
        }

class Song(db.Model):

    __tablename__ = 'song'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)
    introduction = Column(String(120))
    cover_link = Column(String())
    song_link = Column(String(500), nullable=False)
    genre = Column(String(120))
    musician_id = Column(Integer, ForeignKey('musician.id'), nullable=True)

    def __init__(self, name, introduction, cover_link, song_link, musician_id, genre):
        self.name = name
        self.introduction = introduction
        self.cover_link = cover_link
        self.song_link = song_link
        self.musician_id = musician_id
        self.genre = genre

    def add(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        # db.session.update(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'introduction': self.introduction,
            'cover_link': self.cover_link,
            'song_link': self.song_link,
            'musician_id': self.musician_id,
            'genre': self.genre,
        }