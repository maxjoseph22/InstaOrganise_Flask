class Connection:
    def __init__(self, id, user_id_1, user_id_2, created_at=None):
        self.id = id
        self.user_id_1 = user_id_1
        self.user_id_2 = user_id_2
        self.created_at = created_at

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return (
            f"<Connection(id={self.id}, user_1='{self.user_id_1}', user_2='{self.user_id_2}'>")