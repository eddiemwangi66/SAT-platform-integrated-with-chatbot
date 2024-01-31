from flask import Flask, render_template, request, jsonify
import json
from difflib import get_close_matches

app = Flask(__name__)

# Load the knowledge base
def load_knowledge_base(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

# Save the knowledge base
def save_knowledge_base(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

# Find the best match
def find_best_match(user_question, questions):
    matches = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None

# Get the answer for a question
def get_answer_for_question(question, knowledge_base):
    for q in knowledge_base["questions"]:
        if q["question"] == question:
            return q["answer"]

# Load the knowledge base
knowledge_base = load_knowledge_base('knowledge_base.json')

# Render the initial page
@app.route('/')
def index():
    return render_template('index.html', bot_response='')

# Handle the form submission
@app.route('/ask', methods=['POST'])
def ask():
    # Get the user's input from the form
    user_input = request.form['user_input']

    # Find the best match for the user's input
    best_match = find_best_match(user_input, [q["question"] for q in knowledge_base["questions"]])

    # If a match is found, get the answer and return it
    if best_match:
        answer = get_answer_for_question(best_match, knowledge_base)
        return jsonify({"bot_response": answer})

    # If no match is found, update the conversation and ask the user to teach the bot
    else:
        return jsonify({"bot_response": "I don't know the answer. Can you teach me?"})

# Handle the form submission for teaching the bot a new response
@app.route('/teach', methods=['POST'])
def teach():
    # Get the new answer from the form
    new_answer = request.form['new_answer']

    # If the user doesn't want to teach, skip the process
    if new_answer.lower() == 'skip':
        return jsonify({"status": "skipped"})

    # Add the new question and answer to the knowledge base
    knowledge_base["questions"].append({"question": request.form['user_input'], "answer": new_answer})
    save_knowledge_base('knowledge_base.json', knowledge_base)

    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(debug=True)
