from lib.favourite_dog import FavouriteDog
from datetime import datetime

class FavouriteDogRepository:
    def __init__(self, connection):
        self._connection = connection

    def all(self, auth0_id):
        user_id_dict_list = self._connection.execute('SELECT id from users WHERE auth0_id = %s', [auth0_id])
        user_id_dict = user_id_dict_list[0]
        user_id = user_id_dict['id']
        favourite_dog_ids = self._connection.execute('SELECT dog_id FROM favourite_dogs WHERE user_id = %s', [user_id])
        return favourite_dog_ids
    
    def delete(self, id):
        self._connection.execute('DELETE FROM favourite_dogs WHERE id = %s', [id])
        return None
    
    def add_favourite_dog(self, auth0_id, dog_id):
        user_id_dict_list = self._connection.execute('SELECT id from users WHERE auth0_id = %s', [auth0_id])
        user_id_dict = user_id_dict_list[0]
        user_id = user_id_dict['id']
        already_favourited = self._connection.execute('SELECT id from favourite_dogs WHERE user_id = %s AND dog_id = %s', (user_id, dog_id))
        if already_favourited == []:
            self._connection.execute('INSERT INTO favourite_dogs (user_id, dog_id) VALUES (%s, %s)', (user_id, dog_id))
            print(f"Favourite dog added for user {user_id}.")
        else:
            print("this dog is already in your favourites!")
