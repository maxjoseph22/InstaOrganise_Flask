from lib.connection import Connection

class ConnectionRepository:

    def __init__(self, connection):
        self._connection = connection

    def add_connection(self, auth0_id, user_id_2):
        user_id_dict_list = self._connection.execute('SELECT id from users WHERE auth0_id = %s', [auth0_id])
        user_id_dict = user_id_dict_list[0]
        user_id_1 = user_id_dict['id']
        self._connection.execute('INSERT INTO connections (user_id_1, user_id_2) VALUES (%s, %s)', (user_id_1, user_id_2))
        print(f"Connection created between {user_id_1} and {user_id_2}.")

    def all(self, auth0_id):
        user_id_dict_list = self._connection.execute('SELECT id from users WHERE auth0_id = %s', [auth0_id])
        user_id_dict = user_id_dict_list[0]
        user_id_1 = user_id_dict['id']
        connection_ids = self._connection.execute('SELECT * FROM connections WHERE user_id_1 = %s OR user_id_2 = %s ORDER BY created_at DESC', [user_id_1, user_id_1])
        return connection_ids
    
    def delete(self, id):
        self._connection.execute('DELETE FROM connections WHERE id = %s', [id])
        return None