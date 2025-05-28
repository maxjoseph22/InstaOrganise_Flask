class FavouriteDog:
    def __init__(self, id, user_id, dog_id, created_at=None):
        self.id = id
        self.user_id = user_id
        self.dog_id = dog_id
        self.created_at = created_at

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

   
