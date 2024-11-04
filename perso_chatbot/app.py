import pandas as pd
from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB connection
def connect_to_mongo():
    client = MongoClient('mongodb://localhost:27017/')
    return client

# Load fitness tips from CSV into MongoDB
def load_fitness_tips(db, file_path):
    dataset = pd.read_csv(file_path)
    db.fitness_tips.insert_many(dataset.to_dict('records'))
    print("Data loaded into fitness_tips collection successfully.")

# Get fitness tips from MongoDB
def get_fitness_tips(db):
    tips = list(db.fitness_tips.find({}, {'_id': 0, 'description': 1}))
    return [tip['description'] for tip in tips] if tips else []

# Load data when the app starts
client = connect_to_mongo()
db = client.chatbot
load_fitness_tips(db, "Datasets/Synthetic-Persona-Chat_train.csv")  # Use forward slashes for paths

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message')

    # Simple logic for general conversation and fitness tips
    response = handle_user_message(user_message)
    return jsonify({'response': response})

def handle_user_message(user_message):
    # Normalize user input to lower case for easier matching
    user_message = user_message.lower()

    # Responses based on user input
    if 'tasks' in user_message:
        response = "You have 3 tasks scheduled for today: Go for a walk, Complete project report, and Call the doctor."
    elif 'hello' in user_message or 'hi' in user_message:
        response = "Hello! How can I assist you today?"
    elif 'fitness tips' in user_message:
        tips = get_fitness_tips(db)
        response = "Here are some fitness tips: " + ", ".join(tips[:3])  # Displaying first 3 tips
    elif 'what can you do' in user_message:
        response = "I can remind you of your tasks, provide fitness tips, and have general conversations!"
    elif 'thank you' in user_message:
        response = "You're welcome! If you have any other questions, feel free to ask."
    else:
        response = "I'm not sure how to respond to that. Can you ask something else?"

    return response

if __name__ == '__main__':
    app.run(debug=True)
