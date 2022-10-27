# -*- coding: utf-8 -*-
from datetime import datetime

from application.extensions import db


class PhotoModel(db.Model):
    __tablename__ = "file_photo"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    href = db.Column(db.String(255))
    mime = db.Column(db.CHAR(50))
    size = db.Column(db.CHAR(30))

    user_id = db.Column(db.Integer, db.ForeignKey("cp_user.id"))

    create_at = db.Column(db.DateTime, default=datetime.now, comment="创建时间")
