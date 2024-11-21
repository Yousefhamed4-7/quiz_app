from sqlalchemy import Select
from typing import Literal
from werkzeug.security import generate_password_hash,check_password_hash
from ..models import *


class Database():


    USERS = 0
    QUESTION = 1
    QUESTION_TYPE = 2
    CHOICES = 3
    SUBJECT = 4

    LST =  [users,question,question_type,choices,subject]
        
    def get_questions(self,id,user_id):
        return db.session.execute(Select(question).filter_by(user_id=user_id,id=id)).scalar_one()
    
    def get_subjects(self,user_id):
        return db.session.execute(Select(subject).filter_by(user_id=user_id)).scalars().all()

    def get_question_type(self,name):
        return db.session.execute(Select(question_type).filter_by(name=name)).scalar()

    def get_subject(self,name,user_id):
        return db.session.execute(Select(subject).filter_by(name=name,user_id=user_id)).scalar()
    
    def get_choice(self,choice_id):
        return db.session.execute(Select(choices).filter_by(id=choice_id)).scalar_one()
    
    def get_question(self,question_id,user_id):
        return db.session.execute(Select(question).filter_by(id=question_id,user_id=user_id)).scalar()

    def get_unsolved_question(self,subject_name,user_id):
        return db.session.execute(Select(question).filter_by(user_id=user_id,subject_id=self.get_subject(subject_name,user_id).id,Solved=0)).scalars().all()
    
    def get_unsolved_questions(self,user_id):
        return db.session.execute(Select(question).filter_by(user_id=user_id,Solved=0)).scalars().all()
    

    def subject_questions(self,name,user_id):
        return db.session.execute(Select(question).filter_by(subject_id=self.get_subject(name,user_id).id,user_id=user_id)).scalars().all()

    def choice_questions(self,question_id):
        return db.session.execute(Select(choices).filter_by(question_id=question_id)).scalars().all()
    
    @staticmethod
    def choice_questions_function(question_id):
        return db.session.execute(Select(choices).filter_by(question_id=question_id)).scalars().all()
    
    def create_user(self,name:str,email:str,password:str):
        user = users(name=name,email=email,password=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        return user

    def delete_subject(self,name,user_id):
        subject = self.get_subject(name,user_id)
        questions = self.subject_questions(name,user_id)
        for question in questions:
            self.delete_choices(question.id)
            db.session.delete(question)
        db.session.delete(subject)
        db.session.commit()

    def delete_question(self,question_id,user_id):
        q = self.get_question(question_id,user_id)
        self.delete_choices(q.id)
        db.session.delete(q)
        db.session.commit()

    def delete_choices(self,question_id):
        choices = self.choice_questions(question_id)
        for choice in choices:
            db.session.delete(choice)
        db.session.commit()

    def create_question_type(self,name:str):
        questiontype = question_type(name=name)
        db.session.add(questiontype)
        db.session.commit()


    def update(self):
        db.session.commit()


    def create_subject(self,name,user_id):
        subject1 = subject(name=name,user_id=user_id)
        db.session.add(subject1)
        db.session.commit()
    
    def create_question(self,content,subject_name,question_type,user_id):
        q1  = question(content=content,subject_id=self.get_subject(subject_name,user_id).id,question_type_id=self.get_question_type(question_type).id,user_id=user_id)
        db.session.add(q1)
        db.session.commit()
        return q1
    

    def create_choice(self,text,question_id,correct=0):
        choice = choices(text=text,correct=correct,question_id=question_id)
        db.session.add(choice)
        db.session.commit()

    def userexists(self,name):
        return db.session.execute(Select(users).filter_by(name=name)).scalar()
 
    
    def login(self,name,password,email):
        user = db.session.execute(Select(users).filter_by(name=name,email=email)).scalar()
        if not user: return None
        if check_password_hash(user.password,password): return user
        return None