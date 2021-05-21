from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from surveys import surveys
satisfaction = surveys['satisfaction']

app = Flask(__name__)
app.config['SECRET_KEY'] = "some-secret"

debug = DebugToolbarExtension(app)


#routing
#base route
@app.route('/')
def home_page():
    """Displays homepage"""

    return render_template('base.html', satisfaction=satisfaction)

#base route POST, session storage
@app.route('/', methods=["POST"])
def start_session():
    """Handle's start survey button and initializes session"""
    session['responses'] = []
    return redirect('/questions/0')

#questions route
@app.route('/questions/<num>')
def show_question(num):
    """Displays question information for given survey question"""

    #get responses from session
    responses = session['responses']
    #validate correct question number
    length = len(responses)

    if length < int(num):

        flash("You tried to access a later question, here's the next one:")

        numb = length

        return redirect(f'/questions/{numb}')

    elif length > int(num):

        flash("You already answered that question, here's the next one:")

        numb = length

        return redirect(f'/questions/{numb}')


    elif length == int(num):

        #get question
        questions_list = satisfaction.questions
        this_question = questions_list[int(num)]
        question_text = this_question.question

        #get choices
        choice_list = this_question.choices
        choice_1 = choice_list[0]
        choice_2 = choice_list[1]

        numb = int(num)+1


        return render_template('question.html', question=question_text, choice_1=choice_1, choice_2=choice_2, num=numb)


#handle POST request for answers
@app.route('/questions/<num>', methods=["POST"])
def submit_answer(num):
    """Handles POST request and redirects to next question"""

    #incrementing num to access answer data AND to pass for next question
    number = int(num) + 1

    #accesing and storing data in session
    answer = request.form[f"q_{number}_answer"]

    responses = session['responses']
    responses.append(answer)
    session['responses'] = responses

    
    #does survey have more quesions 
    questions_list = satisfaction.questions
    if int(number) >= len(questions_list):
        return redirect('/thanks')
    else:
        #next question
        return redirect(f'/questions/{number}')


#Thank you page 
@app.route('/thanks')
def show_thanks():
    return render_template('thanks.html')