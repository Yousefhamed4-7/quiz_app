from flask import Blueprint,render_template,url_for,redirect,request,flash,session
from .utilities import database,loginrequired
from pathlib import Path
from random import choice

db = database.Database()


view = Blueprint("view",__name__)



@view.route("/")
@loginrequired.login_required
def index():
    return render_template("index.html",subjects=db.get_subjects(session["user_id"]))

@view.route("/subjects/<subject_name>")
@loginrequired.login_required
def viewsubject(subject_name):
    return render_template("subject_questions.html",questions=db.subject_questions(subject_name,user_id=session["user_id"]),subject_name=subject_name)

@view.route("/questions/<question_id>")
@loginrequired.login_required
def question(question_id):
    return render_template("question.html",question=db.get_questions(question_id,session["user_id"]),choices=db.choice_questions(question_id))

@view.route("/question/choices/<question_id>")
@loginrequired.login_required
def viewchoices(question_id):
    return render_template("question_choices.html",question=db.get_questions(question_id,session["user_id"]),choices=db.choice_questions(question_id))


@view.route("/question/create",methods=["POST","GET"])
@loginrequired.login_required
def createquestion():
    if request.method == "POST":
        questiontype = request.form.get("questiontype") 
        subject = request.form.get("subject")
        question = request.form.get("question")
        file = request.files.get("image")
        if file: file.save(Path.joinpath(Path(__file__).parent,"static\images",file.filename))
        if not questiontype:
            flash("Please Chose A Question type","warning")
            return redirect(url_for("view.createquestion"))
        if not subject:
            flash("cant create question (please create subject first)","info")
            return redirect(url_for("view.createquestion"))
        if not question:
            flash("Please Enter A Question","info")
            return redirect(url_for("view.createquestion"))
        q1 = db.create_question(question,subject,questiontype,user_id=session["user_id"],img_path= file.filename if file else None)
        if questiontype == "MCQ":
            choice1 = request.form.get("choice1")
            choice2 = request.form.get("choice2")
            choice3 = request.form.get("choice3")
            choice4 = request.form.get("choice4")
            correct = request.form.get("correct")
            if not choice1 or not choice2 or not choice3 or not choice4 or not correct:
                flash("Please Dont Leave Input Empty","info")
                return redirect(url_for("view.createquestion"))
            for num,i in enumerate([choice1,choice2,choice3,choice4]):
                if (num+1) == int(correct[-1]):
                    db.create_choice(i,q1.id,1)
                else:
                    db.create_choice(i,q1.id,0)
            flash("Created Question","success")
            return redirect(url_for("view.createquestion"))
        elif questiontype== "TF":
            choice = request.form.get("radio")
            if not choice:
                flash("Please Choose A Choice","info")
                return redirect(url_for("view.createquestion"))
            db.create_choice("True",q1.id,1 if choice == "true" else 0)
            db.create_choice("False",q1.id,1 if choice == "false" else 0)
            flash("Created Question","success")
            return redirect(url_for("view.createquestion"))
        elif questiontype == "SQ":
            answer = request.form.get("answer")
            if not answer:
                flash("Please Enter Answer","info")
                return redirect(url_for("view.createquestion"))
            db.create_choice(answer,q1.id,1)
            return redirect(url_for("view.createquestion"))
        else:
            flash("Wrong Question type","danger")
            return redirect(url_for("view.createquestion"))
    return render_template("createquestion.html",subjects=reversed(db.get_subjects(session["user_id"])))

@view.route("/subject/create",methods=["POST","GET"])
@loginrequired.login_required
def create_subject():
    if request.method == "POST":
        subject = request.form.get("name")
        if not subject:
            flash("Please Enter A Subject","info")
            return redirect(url_for("view.create_subject"))
        if db.get_subject(subject,session["user_id"]):
            flash("Subject Already Created","info")
            return redirect(url_for("view.create_subject"))
        db.create_subject(subject,session["user_id"])
        flash("Created Subject","success")
        return redirect(url_for("view.create_subject"))
    return render_template("create_subject.html")

@view.route("/subject/delete",methods=["POST"])
@loginrequired.login_required
def delete_subject():
    subject = request.form.get("subject_name")
    if not subject:
        flash("Something Went Wrong","danger")
        return redirect("/")
    flash("Deleted Subject","info")
    db.delete_subject(subject,session["user_id"])
    return redirect("/")

@view.route("question/delete",methods=["POST"])
@loginrequired.login_required
def delete_question():
    question_id  = request.form.get("question_id")
    if not question_id:
        flash("something went wrong","danger")
        return redirect("/")
    subject = db.get_subject(db.get_question(question_id,session["user_id"]).subject.name,session["user_id"]) 
    db.delete_question(question_id,session["user_id"])
    flash("deleted question","info")
    return redirect(url_for("view.viewsubject",subject_name=subject.name))

@view.route("/quiz")
@loginrequired.login_required
def quizview():
    return render_template("quizview.html",subjects=db.get_subjects(session["user_id"]))

@view.route("/quiz/me",methods=["POST"])
@loginrequired.login_required
def quizme():
    if request.method == "POST":
        subject = request.form.get("subject")
        quiztype = request.form.get("quiztype")
        if not subject:
            flash("Please Enter Subject","info")
            return redirect("view.quizme")
        if not quiztype:
            flash("Please Enter QuizType","info")
            return redirect("view.quizme")
        questions = []
        if subject == "all" and quiztype == "all":
            for subjects in db.get_subjects(session["user_id"]):
                questions.extend(db.subject_questions(subjects.name,session["user_id"]))

        elif subject != "all" and quiztype == "all":
            questions = list(db.subject_questions(subject,session["user_id"]))

        elif subject == "all" and quiztype == "random":
            for subjects in db.get_subjects(session["user_id"]):
                questions.extend(db.subject_questions(subjects.name,session["user_id"]))
            questions = [choice(questions) for _ in range(10)] if len(questions) >=10 else questions

        elif subject != "all" and quiztype == "random":
            questions = list(db.subject_questions(subject,session["user_id"]))
            random_question = []
            if len(questions) >= 10:
                while len(random_question) != 10:
                    q = choice(questions)
                    if q not in random_question:
                        random_question.append(q)
                questions = random_question
            else:
                questions = questions
        
        elif subject != "all" and quiztype == "unsolved":
            questions = list(db.get_unsolved_question(subject,session["user_id"]))
        
        elif subject == "all" and quiztype == "unsolved":
            questions = list(db.get_unsolved_questions(session["user_id"]))
        else:
            flash("Something Went Wrong Please Try Again","danger")
            return redirect(url_for("view.quizview"))
        return render_template("quiz.html",questions=set(questions))

@view.route("/question/edit/<question_id>",methods=["POST","GET"])  
@loginrequired.login_required    
def edit_question(question_id):
    if request.method == "GET":
        return render_template("edit_question.html",question=db.get_question(question_id,session["user_id"]))
    else:
        questiontype = request.form.get("questiontype") 
        old_path = request.form.get("old_path")
        question = request.form.get("question")
        file = request.files.get("image")
        if file: file.save(Path.joinpath(Path(__file__).parent,"static\images",file.filename))
        if not questiontype:
            flash("Please Chose A Question type","warning")
            return redirect(url_for("view.edit_question", question_id=question_id))
        if not old_path:
            flash("Something Went Wrong","warning")
            return redirect(url_for("view.edit_question", question_id=question_id))
        if not question:
            flash("Please Enter A Question","info")
            return redirect(url_for("view.edit_question", question_id=question_id))
        subject = db.get_question(question_id,session["user_id"]).subject.name
        db.delete_question(question_id,session["user_id"])
        q1 = db.create_question(question,subject,questiontype,user_id=session["user_id"],img_path= file.filename if file else old_path if old_path != "None" else None)
        if questiontype == "MCQ":
            choice1 = request.form.get("choice1")
            choice2 = request.form.get("choice2")
            choice3 = request.form.get("choice3")
            choice4 = request.form.get("choice4")
            correct = request.form.get("correct")
            if not choice1 or not choice2 or not choice3 or not choice4 or not correct:
                flash("Please Dont Leave Input Empty","info")
                return redirect(url_for("view.edit_question", question_id=question_id))
            for num,i in enumerate([choice1,choice2,choice3,choice4]):
                if (num+1) == int(correct[-1]):
                    db.create_choice(i,q1.id,1)
                else:
                    db.create_choice(i,q1.id,0)
            flash("Updated Question","success")
            return redirect(url_for("view.viewchoices", question_id=question_id))
        elif questiontype== "TF":
            choice = request.form.get("radio")
            if not choice:
                flash("Please Choose A Choice","info")
                return redirect(url_for("view.edit_question", question_id=question_id))
            db.create_choice("True",q1.id,1 if choice == "True" else 0)
            db.create_choice("False",q1.id,1 if choice == "False" else 0)
            flash("Updated Question","success")
            return redirect(url_for("view.viewchoices", question_id=question_id))
        elif questiontype == "SQ":
            answer = request.form.get("answer")
            if not answer:
                flash("Please Enter Answer","info")
                return redirect(url_for("view.edit_question", question_id=question_id))
            db.create_choice(answer,q1.id,1)
            flash("Updated Question","success")
            return redirect(url_for("view.viewchoices", question_id=question_id))
        else:
            flash("Wrong Question type","danger")
            return redirect(url_for("view.edit_question", question_id=question_id))


