import pandas as pd
from pymongo import MongoClient

def connect_to_mongo():
    client = MongoClient('mongodb://localhost:27017/')
    return client

def load_fitness_tips(db, file_path):
    # Load the dataset from a CSV file
    dataset = pd.read_csv("Datasets\Synthetic-Persona-Chat_train.csv")

    # Insert data into the fitness_tips collection
    db.fitness_tips.insert_many(dataset.to_dict('records'))
    print(f"Data loaded into fitness_tips collection successfully.")

def get_fitness_tips(db):
    tips = list(db.fitness_tips.find({}, {'_id': 0, 'description': 1}))
    return [tip['description'] for tip in tips] if tips else []
