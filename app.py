from dotenv import load_dotenv
import os
from openai import OpenAI
from lib.dog_repository import DogRepository
from lib.breed_repository import BreedRepository
from lib.dog import Dog
import json
from lib.database_connection import DatabaseConnection
import csv
from colorama import init, Fore, Style
from datetime import datetime

connection = DatabaseConnection()
connection.connect()


def extract_and_save_dog_data(description):
    dog_repository = DogRepository(connection)
    breed_repository = BreedRepository(connection)
    print("Welcome to The Dogist!\nWhat would you like to do? \n1 - Add a new dog \n2 - View rankings by breed \n3 - Viewing rankings by name \n4 - Search by breed \n5 - Search by name \n6 - View all breeds \n7 - Import dogs by CSV file \n8 - Add to breed count \n9 - View never featured breeds \n10 - View a random dog")
   
    return "\n".join(dog_repository.get_breed_popularity())
    
   