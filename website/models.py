from . import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column,relationship,Mapped


class users(db.Model):
    __tablename__ = "users"

    id:Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    name:Mapped[str] = mapped_column(unique=True)
    email:Mapped[str]
    password:Mapped[str]


class question_type(db.Model):
    __tablename__ = "question_type"

    id:Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    name:Mapped[str] = mapped_column(unique=True)

class subject(db.Model):
    __tablename__ = "subject"

    id:Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    name:Mapped[str] 
    user:Mapped["users"] = relationship()
    user_id:Mapped[int] = mapped_column(ForeignKey("users.id"))

class question(db.Model):
    __tablename__ = "question"

    id:Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    content:Mapped[str] 
    Solved:Mapped[int] = mapped_column(default=0)
    subject:Mapped["subject"] = relationship()
    subject_id:Mapped[int] = mapped_column(ForeignKey("subject.id"))
    question_type:Mapped["question_type"] = relationship()
    question_type_id:Mapped[int] = mapped_column(ForeignKey("question_type.id"))
    user:Mapped["users"] = relationship()
    user_id:Mapped[int] = mapped_column(ForeignKey("users.id"))

class choices(db.Model):
    __tablename__ = "choice"

    id:Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    text:Mapped[str]
    correct:Mapped[int] = mapped_column(default=0)
    question:Mapped["question"] = relationship()
    question_id:Mapped[int] =  mapped_column(ForeignKey("question.id"))