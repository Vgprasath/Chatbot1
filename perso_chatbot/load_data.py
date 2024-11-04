# load_data.py
from Database.database import connect_to_mongo, load_fitness_tips

if __name__ == '__main__':
    mongo_client = connect_to_mongo()
    db = mongo_client['perso_chatbot']

    # Update this path to your actual file location
    file_path = 'Datasets\Synthetic-Persona-Chat_train.csv'
    load_fitness_tips(db, file_path)
