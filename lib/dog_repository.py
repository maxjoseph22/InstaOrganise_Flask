from lib.dog import Dog
import datetime
from colorama import init, Fore, Style
import random
import instaloader
import csv
from datetime import datetime

class DogRepository:
    # Initialize with a database connection
    def __init__(self, connection):
        self._connection = connection

    # Retrieve all dogs
    def all(self):
        rows = self._connection.execute('SELECT * FROM dogs ORDER BY date_posted DESC')
        dogs = []
        for row in rows:
            item = Dog(
                row["id"], row["name"], row["breed"], row["purebreed"],
                row["mix"], row["age"], row["sex"], row["location"],
                row["personality"], row["likes"], row["comments"],
                row["link_to_post"], row["video"], row["date_posted"], row["photo"], row["breed_id"]
            )
            dogs.append(item)
        return dogs
    
  
  
    def get_breed_popularity(self):
        rows = self._connection.execute(
            'SELECT breed, COUNT(*) AS count FROM dogs GROUP BY breed ORDER BY count DESC'
        )
        result = []
        for row in rows:
            result.append({"breed": row["breed"], "count": row["count"]})
        return result
    
    def get_rare_breeds(self):
        rows = self._connection.execute(
            'SELECT breed, COUNT(*) AS count FROM dogs GROUP BY breed HAVING COUNT(*) IN (1, 2, 3) ORDER BY count ASC'
        )
        result = []
        for row in rows:
            result.append({"breed": row["breed"], "count": row["count"]})
        return result
    
    def get_rare_purebreeds(self):
        rows = self._connection.execute(
             '''
        SELECT breed, COUNT(*) AS count
        FROM dogs
        WHERE breed NOT LIKE '%%/%%' AND breed NOT LIKE '%%mix%%' AND breed NOT LIKE '%%Mix%%'
        GROUP BY breed
        ORDER BY count ASC
        '''
        )
        result = []
        for row in rows:
            result.append({"breed": row["breed"], "count": row["count"]})
        return result

    def get_loveable_mutts(self):
        rows = self._connection.execute(
            '''
        SELECT breed, COUNT(*) AS count
        FROM dogs
        WHERE breed LIKE '%%/%%' OR breed LIKE '%%mix%%'
        GROUP BY breed
        ORDER BY count ASC
        '''
        )
        result = []
        for row in rows:
            result.append({"breed": row["breed"], "count": row["count"]})
        return result

    # Retrieve popularity by likes
    def get_likes_popularity(self):
        rows = self._connection.execute(
            'SELECT name, id, likes, link_to_post FROM dogs ORDER BY likes DESC'
        )
        result = []
        for row in rows:
            result.append({
                "name": row["name"],
                "id": row["id"],
                "likes": row["likes"],
                "link_to_post": row["link_to_post"]
            })
        return result
    
    # Retrieve name popularity
    def get_name_popularity(self):
        rows = self._connection.execute(
            'SELECT name, COUNT(*) AS count FROM dogs GROUP BY name ORDER BY count DESC'
        )
        result = []
        for row in rows:
            result.append({
                "name": row["name"],
                "count": row["count"]
            })
        return result
    
    # Find a dog by ID
    def find(self, id):
        rows = self._connection.execute('SELECT * FROM dogs WHERE id = %s', [id])
        dogs = []
        for row in rows:
            item = Dog(
                row["id"], row["name"], row["breed"], row["purebreed"], row["mix"],
                row["age"], row["sex"], row["location"], row["personality"],
                row["likes"], row["comments"], row["link_to_post"], row["video"], row["date_posted"], row["photo"], row["breed_id"]
            )
            dogs.append(item)
        
        return dogs
    
    # Find dogs by name
    def find_by_name(self, name):
        rows = self._connection.execute('SELECT * FROM dogs WHERE UPPER(name) LIKE UPPER(%s)', [f'%{name}%'])
        dogs = []
        for row in rows:
            item = Dog(
                row["id"], row["name"], row["breed"], row["purebreed"], row["mix"],
                row["age"], row["sex"], row["location"], row["personality"],
                row["likes"], row["comments"], row["link_to_post"], row["video"], row["date_posted"], row["photo"], row["breed_id"]
            )
            dogs.append(item)

        return dogs
        
        readable_dogs = "\n\n".join(
        f"""
        ID: {dog.id}
        Name: {dog.name}
        Breed: {dog.breed}
        Purebred: {"Yes" if dog.purebreed else "No"}
        Mix: {dog.mix}
        Age: {dog.age}
        Sex: {dog.sex}
        Location: {dog.location}
        Personality: {dog.personality}
        Likes: {dog.likes}
        Comments: {dog.comments}
        Link to Post: {dog.link_to_post}
        Video: {dog.video}
        Date Posted: {dog.date_posted}
        Photo URL: {dog.photo}
        Breed ID: {dog.breed_id}
        """
        for dog in dogs
    )

        return readable_dogs
        
        
    # Find dogs by breed
    def find_by_breed(self, breed):
        rows = self._connection.execute('SELECT * FROM dogs WHERE UPPER(breed) LIKE UPPER(%s)', [f'%{breed}%'])
        dogs = []
        for row in rows:
            item = Dog(
                row["id"], row["name"], row["breed"], row["purebreed"], row["mix"],
                row["age"], row["sex"], row["location"], row["personality"],
                row["likes"], row["comments"], row["link_to_post"], row["video"], row["date_posted"], row["photo"], row["breed_id"]
            )
            dogs.append(item)
        return dogs
        
    #     readable_dogs = "\n\n".join(
    #     f"""
    #     ID: {dog.id}
    #     Name: {dog.name}
    #     Breed: {dog.breed}
    #     Purebred: {"Yes" if dog.purebreed else "No"}
    #     Mix: {dog.mix}
    #     Age: {dog.age}
    #     Sex: {dog.sex}
    #     Location: {dog.location}
    #     Personality: {dog.personality}
    #     Likes: {dog.likes}
    #     Comments: {dog.comments}
    #     Link to Post: {dog.link_to_post}
    #     Video: {dog.video}
    #     Date Posted: {dog.date_posted}
    #     Photo URL: {dog.photo}
    #     Breed ID: {dog.breed_id}
    #     """
    #     for dog in dogs
    # )
    #     return readable_dogs

    # Find dogs by id
    def find_by_id(self, id):
        rows = self._connection.execute('SELECT * FROM dogs WHERE id = %s', [id])
        row = rows[0]
        return Dog(
                row["id"], row["name"], row["breed"], row["purebreed"], row["mix"],
                row["age"], row["sex"], row["location"], row["personality"],
                row["likes"], row["comments"], row["link_to_post"], row["video"], row["date_posted"], row["photo"], row["breed_id"]
            )
    
    # Find dogs by age
    def find_by_age(self, age):
        rows = self._connection.execute('SELECT * FROM dogs WHERE age LIKE %s', [f'%{age}%'])
        dogs = []
        for row in rows:
            item = Dog(
                row["id"], row["name"], row["breed"], row["purebreed"], row["mix"],
                row["age"], row["sex"], row["location"], row["personality"],
                row["likes"], row["comments"], row["link_to_post"], row["video"], row["date_posted"], row["photo"], row["breed_id"]
            )
            dogs.append(item)
        
        readable_dogs = "\n\n".join(
        f"""
        ID: {dog.id}
        Name: {dog.name}
        Breed: {dog.breed}
        Purebred: {"Yes" if dog.purebreed else "No"}
        Mix: {dog.mix}
        Age: {dog.age}
        Sex: {dog.sex}
        Location: {dog.location}
        Personality: {dog.personality}
        Likes: {dog.likes}
        Comments: {dog.comments}
        Link to Post: {dog.link_to_post}
        Video: {dog.video}
        Date Posted: {dog.date_posted}
        Photo URL: {dog.photo}
        Breed ID: {dog.breed_id}
        """
        for dog in dogs
    )

        return readable_dogs
    
    # Create a new dog entry
    def create(self, dog):
        # First try to find the breed in the purebred table
        breed_rows = self._connection.execute(
            'SELECT id FROM breeds WHERE breed_name = %s',
            [dog.breed]
        )

        # If found in purebred table, use that ID and set purebreed=True
        if len(breed_rows) > 0:
            breed_id = breed_rows[0]["id"]
            rows = self._connection.execute(
                '''
                INSERT INTO dogs (
                    name, breed, purebreed, mix, age, sex, location, personality, 
                    likes, comments, link_to_post, video, date_posted, photo, breed_id
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
                ''', 
                [
                    dog.name, dog.breed, True, False, dog.age, dog.sex,
                    dog.location, dog.personality, dog.likes, dog.comments,
                    dog.link_to_post, dog.video, dog.date_posted, dog.photo, breed_id
                ]
            )
        # If not found in purebred table, check cross breeds table
        else:
            cross_breed_rows = self._connection.execute(
                'SELECT id FROM cross_breeds WHERE breed_name = %s',
                [dog.breed]
            )

            if len(cross_breed_rows) == 0:
                raise ValueError(f"Breed '{dog.breed}' not found in either breeds or cross breeds tables")

            cross_breed_id = cross_breed_rows[0]["id"]
            rows = self._connection.execute(
                '''
                INSERT INTO dogs (
                    name, breed, purebreed, mix, age, sex, location, personality, 
                    likes, comments, link_to_post, video, date_posted, photo, cross_breed_id
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
                ''', 
                [
                    dog.name, dog.breed, False, True, dog.age, dog.sex,
                    dog.location, dog.personality, dog.likes, dog.comments,
                    dog.link_to_post, dog.video, dog.date_posted, dog.photo, cross_breed_id
                ]
            )

        return rows[0]["id"]
    
    # Get random dog
    def random_dog(self):
        range_list = self._connection.execute('SELECT COUNT(*) FROM dogs')
        range_dict = range_list[0]
        range_num = range_dict['count']
        random_num = random.randrange(1, range_num)

        rows = self._connection.execute('SELECT * FROM dogs WHERE id = %s', [random_num])
        dogs = []
        for row in rows:
            item = Dog(
                row["id"], row["name"], row["breed"], row["purebreed"], row["mix"],
                row["age"], row["sex"], row["location"], row["personality"],
                row["likes"], row["comments"], row["link_to_post"], row["video"], row["date_posted"], row["photo"], row["breed_id"], row["cross_breed_id"]
            )
            dogs.append(item)

        return dogs
        
        readable_dogs = "\n\n".join(
        f"""
        ID: {dog.id}
        Name: {dog.name}
        Breed: {dog.breed}
        Purebred: {"Yes" if dog.purebreed else "No"}
        Mix: {dog.mix}
        Age: {dog.age}
        Sex: {dog.sex}
        Location: {dog.location}
        Personality: {dog.personality}
        Likes: {dog.likes}
        Comments: {dog.comments}
        Link to Post: {dog.link_to_post}
        Video: {dog.video}
        Date Posted: {dog.date_posted}
        Photo URL: {dog.photo}
        Breed ID: {dog.breed_id}
        Cross breed ID: {dog.cross_breed_id}
        """
        for dog in dogs
    )
        return readable_dogs

    # Delete a dog entry
    def delete(self, id):
        self._connection.execute('DELETE FROM dogs WHERE id = %s', [id])
        return None
    
    # def scrape_recent_posts(self, date):
    #     # Create an instance of Instaloader
    #     L = instaloader.Instaloader()

    #     # Specify the profile and cutoff date
    #     profile_name = "thedogist"
    #     cutoff_date = date  # Year, Month, Day

    #     # Prepare data storage
    #     posts_data = []

    #     try:
    #         # Get profile
    #         profile = instaloader.Profile.from_username(L.context, profile_name)

    #         # Get posts
    #         posts = profile.get_posts()

    #         # Iterate through posts
    #         for post in posts:
    #             # Stop if we've reached posts older than our cutoff date
    #             if post.date < cutoff_date:
    #                 break

    #             # Collect post data
    #             post_data = {
    #                 'caption': post.caption,
    #                 'likes': post.likes,
    #                 'comments': post.comments,
    #                 'link_to_post': f"https://www.instagram.com/p/{post.shortcode}"
    #             }
    #             posts_data.append(post_data)
    #             print(f"Processed post from {post.date}")

    #         # Save to CSV
    #         csv_filename = f"{profile_name}_posts.csv"
    #         with open(csv_filename, 'w', newline='', encoding='utf-8') as file:
    #             writer = csv.DictWriter(file, fieldnames=['caption', 'likes', 'comments', 'link_to_post'])
    #             writer.writeheader()
    #             writer.writerows(posts_data)

    #         print(f"\nSaved {len(posts_data)} posts to {csv_filename}")

    #     except instaloader.exceptions.ProfileNotExistsException:
    #         print(f"Profile {profile_name} does not exist")
    #     except Exception as e:
    #         print(f"An error occurred: {e}")

