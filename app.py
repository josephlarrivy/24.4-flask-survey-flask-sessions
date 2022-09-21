from flask import Flask, request, render_template, redirect, flash, session

app = Flask(__name__)

from flask_debugtoolbar import DebugToolbarExtension
app.config['SECRET_KEY'] = 'secret'

debug = DebugToolbarExtension(app)

from surveys import satisfaction_survey as survey








responses = []

@app.route('/')
def start_page():
    return render_template('/start_page.html', survey=survey)


@app.route("/begin", methods=["POST"])
def start_survey():
    return redirect('/questions/0')






@app.route('/questions/<int:qnum>', methods= ['GET'])
def questions(qnum):

    question = survey.questions[qnum]
    

    # if the lenght of the responses list is the same as the length of the questions list, the survey must be complete
    if (len(responses) == len(survey.questions)):
        return redirect("/complete")

    if (len(responses) != qnum and qnum>0):
        flash("Invalid. Please answer questions in order.")
        return redirect(f'/questions/{len(responses)}')

    
    return render_template('/questions.html', question_num=qnum, question=question)




@app.route('/answer', methods=['POST'])
def answer():
    choice = request.form['answer']
    responses.append(choice)

    if (len(responses) == len(survey.questions)):
        return redirect("/complete")

    else:
        return redirect(f"/questions/{len(responses)}")


@app.route('/complete')
def survey_complete():
    return render_template('complete.html')





if __name__ == '__main__':
    app.run()