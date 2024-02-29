import csv

import pymongo
import bcrypt
import ast
import pandas as pd
import random
#from sklearn.feature_extraction.text import TfidfVectorizer
#from sklearn.metrics.pairwise import cosine_similarity
from pymongo.errors import BulkWriteError


class LoginManager:

    def __init__(self) -> None:
        # MongoDB connection
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db = self.client["project"]
        self.collection = self.db["users"]
        self.salt = bcrypt.gensalt()  # TODO: if not working, generate a new salt bcrypt.gensalt()

    def register_user(self, username: str, password: str) -> None:
        # empty username or password
        if not username:
            raise ValueError("Username is require.")
        if not password:
            raise ValueError("Password is require.")


        # minimum length of username and password
        if len(username) < 3 or len(password) < 3:
            raise ValueError("Username and password must be at least 3 characters.")

        # if username already exists
        if self.collection.find_one({"username": username}) is not None:
            raise ValueError(f"User already exists: {username}")

        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), self.salt)

        # Create new user in the database
        new_user = {"username": username, "hashed_password": hashed_password.decode()}  # Convert bytes to string
        self.collection.insert_one(new_user)

    def login_user(self, username: str, password: str) -> object:
        # Find the user
        user = self.collection.find_one({"username": username})
        if user is None or not bcrypt.checkpw(password.encode('utf-8'), user['hashed_password'].encode('utf-8')):
            raise ValueError("Invalid username or password")
        print(f"Logged in successfully as: {username}")
        return user



class DBManager:

    def __init__(self) -> None:
        # MongoDB connection
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db = self.client["project"]
        self.user_collection = self.db["users"]
        self.game_collection = self.db["games"]

    def load_csv(self) -> None:
        # Define file path and collection name
        filename = "NintendoGames.csv"
        collection_name = "games"

        # Open CSV file and create cursor
        with open(filename, "r") as csvfile:
            reader = csv.DictReader(csvfile)

            # Prepare data for insertion
            data_to_insert = []
            for row in reader:
                try:
                    row["genres"] = ast.literal_eval(row["genres"])
                except (ValueError, SyntaxError) as e:
                    print(f"Error parsing 'genres' field for row: {row} (Skipping)")
                    continue
                row["is_rented"] = False
                data_to_insert.append(row)

            # Insert data into collection with duplicate prevention
            try:
                self.game_collection.insert_many(data_to_insert, ordered=False)
                print(f"Data loaded from {filename} into {collection_name} collection.")
            except BulkWriteError as e:
                print(f"Error encountered during data insertion: {e}")

    def recommend_games_by_genre(self, user: dict) -> str:
        # TODO
        pass

    def recommend_games_by_name(self, user: dict) -> str:
        # TODO
        pass

    def rent_game(self, user: dict, game_title: str) -> str:
        # TODO
        pass

    def return_game(self, user: dict, game_title: str) -> str:
        # TODO
        pass
