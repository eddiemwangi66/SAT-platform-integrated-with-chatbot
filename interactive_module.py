from flask import Flask, render_template, request, redirect, url_for


app = Flask(__name__)

class MultipleChoiceQuiz:
    def __init__(self, question, options, correct_option):
        self.question = question
        self.options = options
        self.correct_option = correct_option

# Define multiple quiz questions
quiz_questions = [
    MultipleChoiceQuiz("What is the most common type of social engineering attack?", ["Phishing", "Malware", "DDoS", "Spoofing"], 1),
    MultipleChoiceQuiz("Which of the following is a secure password practice?", ["Using 'password'", "Using a combination of letters, numbers, and symbols", "Writing the password on a sticky note", "Sharing the password with colleagues"], 2),
    # Add more questions as needed
]
current_question_index = 0  # Variable to keep track of the current question index


class CyberAttackSimulation:
    def __init__(self, scenario_description):
        self.scenario_description = scenario_description

class RealLifeSituation:
    def __init__(self, scenario_description):
        self.scenario_description = scenario_description


def home(user=None):
    return render_template('interactive_index.html', user=user)

@app.route('/quiz', methods=['GET', 'POST'])
def quiz(user=None):
    global current_question_index

    if current_question_index >= len(quiz_questions):
        # If all questions have been answered, redirect to a summary or completion page
        return redirect(url_for('quiz_summary_route'))

    current_question = quiz_questions[current_question_index]

    if request.method == 'POST':
        user_answer = int(request.form['user_answer'])
        result = user_answer == current_question.correct_option
        current_question_index += 1  # Move to the next question
        return render_template('quiz_result.html', result=result, user=user)

    return render_template('quiz.html', quiz=current_question, user=user)

@app.route('/quiz_summary', methods=['GET'])
def quiz_summary():
    # Provide a page summarizing the quiz results
    return render_template('quiz_summary.html')

@app.route('/simulation', methods=['GET'])
def simulation():
    simulation_description = "An employee receives a suspicious email with an attachment."
    cyber_attack_simulation = CyberAttackSimulation(simulation_description)
    return render_template('simulation.html', simulation=cyber_attack_simulation)

@app.route('/simulation_response', methods=['POST'])
def simulation_response():
    if request.method == 'POST':
        # Extract data from the form using request.form
        user_response = request.form.get('user_response')

        # Perform any necessary logic based on the user's response
        correct_answer = "Report it"
        if user_response == correct_answer:
            result = "Your answer is correct!"
        else:
            result = "Your answer is incorrect. The correct answer is: " + correct_answer

        # Redirect the user to a page indicating the result of the simulation
        return redirect(url_for('simulation_result', result=result))

    # If the request method is not POST, redirect to the simulation page
    return redirect(url_for('simulation'))

@app.route('/simulation_result/<result>', methods=['GET'])
def simulation_result(result):
    # Provide a page indicating the result of the simulation
    return render_template('simulation_result.html', result=result)

@app.route('/real_life_situation', methods=['GET'])
def real_life_situation():
    situation_description = "An employee receives a phone call from someone claiming to be IT support."
    real_life_situation = RealLifeSituation(situation_description)
    return render_template('real_life_situation.html', situation=real_life_situation)

@app.route('/real_life_situation_response', methods=['POST'])
def real_life_situation_response():
    if request.method == 'POST':
        # Extract data from the form using request.form
        user_response = request.form.get('user_response')

        # Perform any necessary logic based on the user's response
        # In a real application, you might check if the response is appropriate, provide feedback, etc.

        # Redirect the user to a page indicating the result of the real-life situation
        return redirect(url_for('real_life_situation_result'))

    # If the request method is not POST, redirect to the real-life situation page
    return redirect(url_for('real_life_situation'))

@app.route('/real_life_situation_result', methods=['GET'])
def real_life_situation_result():
    # Provide a page indicating the result of the real-life situation
    return render_template('real_life_situation_result.html')
   


if __name__ == '__main__':
    app.run(debug=True)
