from lib.favourite_dog import FavouriteDog
from datetime import datetime

class FavouriteDogRepository:
    def __init__(self, connection):
        self._connection = connection

    def all(self):
        rows = self._connection.execute('SELECT * FROM favourite_dogs ORDER BY created_at DESC')
        favourite_dogs = []
        for row in rows:
            item = FavouriteDog(
                row["id"], row["user_id"], row["dog_id"], row["created_at"]
                )
            favourite_dogs.append(item)
        return favourite_dogs
    
    def delete(self, id):
        self._connection.execute('DELETE FROM favourite_dogs WHERE id = %s', [id])
        return None
    
    def add_favourite_dog(self, auth0_id, dog_id):
        user_id_dict_list = self._connection.execute('SELECT id from users WHERE auth0_id = %s', [auth0_id])
        user_id_dict = user_id_dict_list[0]
        user_id = user_id_dict['id']
        print(user_id)
        self._connection.execute('INSERT INTO favourite_dogs (user_id, dog_id) VALUES (%s, %s)', (user_id, dog_id))
        return f"Favourite dog added for user {user_id}."
