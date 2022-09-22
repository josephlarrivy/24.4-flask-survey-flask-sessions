from flask import Flask, request, render_template, redirect, flash, session
app = Flask(__name__)
from flask_debugtoolbar import DebugToolbarExtension
app.config['SECRET_KEY'] = 'secret'
from surveys import satisfaction_survey as survey


debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False





RESPONSES_KEY = "responses"
# responses = []

@app.route('/')
def start_page():
    return render_template('/start_page.html', survey=survey)


@app.route("/begin", methods=["POST"])
def start_survey():
    session[RESPONSES_KEY] = []
    return redirect('/questions/0')






@app.route('/questions/<int:qnum>', methods= ['GET'])
def questions(qnum):
    responses = session.get(RESPONSES_KEY)
    question = survey.questions[qnum]

    

    # if the lenght of the responses list is the same as the length of the questions list, the survey must be complete
    if (len(responses) == len(survey.questions)):
        return redirect("/complete")

    if (len(responses) != qnum):
        flash("Invalid. Please answer questions in order.")
        return redirect(f'/questions/{len(responses)}')

    
    return render_template('/questions.html', question_num=qnum, question=question)




@app.route('/answer', methods=['POST'])
def answer():
    choice = request.form['answer']

    responses = session[RESPONSES_KEY]
    responses.append(choice)
    session[RESPONSES_KEY] = responses

    if (len(responses) == len(survey.questions)):
        return redirect("/complete")

    else:
        return redirect(f"/questions/{len(responses)}")


@app.route('/complete')
def survey_complete():
    return render_template('complete.html')





if __name__ == '__main__':
    app.run()