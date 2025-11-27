from django.db import models

from musicApp import settings
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship


class Album(settings.BaseModel):
    __tablename__ = 'albums'

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
        unique=True,
    )
    album_name = Column(
        String,
        unique=True,
        nullable=False,
    )
    image_url = Column(
        String,
        nullable=False,
    )
    price = Column(
        Float,
        nullable=False,
    )

    # FIXED — remove backref, use back_populates instead
    songs = relationship(
        'Song',
        back_populates='album',
        cascade='all, delete-orphan',
    )


class Song(settings.BaseModel):
    __tablename__ = 'songs'

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
        unique=True,
    )
    song_name = Column(
        String,
        nullable=False,
    )
    album_id = Column(
        Integer,
        ForeignKey('albums.id'),
        nullable=False
    )

    # FIXED — matches back_populates from Album
    album = relationship(
        'Album',
        back_populates='songs',
    )
    def __str__(self):
        return self.song_name