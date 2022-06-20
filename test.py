import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Musician, Song


class DiveBETestCase(unittest.TestCase): 
# This class represents the DiveBEAPP test case
    def setUp(self):
        # Define test variables and initialize app
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "divebeapp_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format("postgres", "abc", "localhost:5432", self.database_name)
        setup_db(self.app, self.database_path)

        # Binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.new_musician = {
            "name": "Jingchen Xie",
            "e_mail": "qpoweiru@sdhfl.com",
            "phone": "3849302908",
            "website": "https://cyanky.github.io/",
            "introduction": "She's coming now!",
            "avatar_link": "jskldfjoeuojsfdjkl",
            "genres": "R&B",
        }

        self.new_song = {
            "name": "Get up",
            "introduction": "to the top",
            "cover_link": "woeiruojwl",
            "song_link": "https://cyanky.github.io/",
            "genre": "R&B",
            "musician_id": 10
        }

        # Set up authentication tokens info
        with open('auth_config.json', 'r') as f:
            self.auth = json.loads(f.read())

        agency_jwt = self.auth["roles"]["Musician Agency"]["jwt_token"]
        producer_jwt = self.auth["roles"]["Song Producer"]["jwt_token"]
        self.auth_headers = {
            "Musician Agency": f'Bearer {agency_jwt}',
            "Song Producer": f'Bearer {producer_jwt}'
        }

    def tearDown(self):
        """Executed after each test"""
        pass

# ------------------------------------------------------------------------------#
# Musician part test
# ------------------------------------------------------------------------------#
   
    #  Test routes with method ['GET']
    # ------------------------------------------------------------

    # def test_get_musician_for_Musician_Agency(self):
    #     header_obj = {
    #         "Authorization": self.auth_headers["Musician Agency"]
    #     }
    #     res = self.client().get('/musicians', headers=header_obj)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(data['total_musicians'])
    #     self.assertTrue(len(data['musicians']))

    # def test_get_specific_musician_info_for_Musician_Agency(self):
    #     header_obj = {
    #         "Authorization": self.auth_headers["Musician Agency"]
    #     }
    #     res = self.client().get('/musicians/3', headers=header_obj)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)

    # def test_get_musician_for_Song_Producer(self):
    #     header_obj = {
    #         "Authorization": self.auth_headers["Song Producer"]
    #     }
    #     res = self.client().get('/musicians', headers=header_obj)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(data['total_musicians'])
    #     self.assertTrue(len(data['musicians']))

    # def test_get_specific_musician_info_for_Song_Producer(self):
    #     header_obj = {
    #         "Authorization": self.auth_headers["Song Producer"]
    #     }
    #     res = self.client().get('/musicians/3', headers=header_obj)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)

    # def test_404_get_specific_musician_info(self):
    #     res = self.client().get('/musicians/10000000000')
    #     data = json.loads(res.data)        

    #     self.assertEqual(res.status_code, 404)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'], 'resource not found')

    # def test_404_sent_requesting_beyond_valid_musician_page(self):
    #     res = self.client().get('/musicians?page=10000')
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 404)
    #     self.assertEqual(data['success'], False)

    #  Test routes with method ['PATCHE''DELETE']
    # ------------------------------------------------------------

    # def test_update_musician_for_Musician_Agency(self):
    #     header_obj = {
    #         "Authorization": self.auth_headers["Musician Agency"]
    #     }
    #     res = self.client().patch("/musicians/8", json={"name":"Given"}, headers=header_obj)
    #     data = json.loads(res.data)
    #     musician = Musician.query.filter(Musician.id == 8).one_or_none()

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data["success"], True)
    #     self.assertEqual(musician.format()["name"], "Given")

    # def test_400_for_failed_update_musician(self):
    #     header_obj = {
    #         "Authorization": self.auth_headers["Musician Agency"]
    #     }
    #     res = self.client().patch("/musicians/8", headers=header_obj)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 400)
    #     self.assertEqual(data["success"], False)
    #     self.assertEqual(data["message"], "bad request")

    # def test_delete_musician_for_Musician_Agency(self):
    #     header_obj = {
    #         "Authorization": self.auth_headers["Musician Agency"]
    #     }
    #     res = self.client().delete("/musicians/14", headers=header_obj)
    #     data = json.loads(res.data)

    #     musician = Musician.query.filter(Musician.id == 14).one_or_none()

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data["success"], True)
    #     self.assertEqual(data["deleted"], 14)
    #     self.assertTrue(data["total_musicians"])
    #     self.assertTrue(len(data["musicians"]))
    #     self.assertEqual(musician, None)

    # def test_422_if_musician_not_exist(self):
    #     header_obj = {
    #         "Authorization": self.auth_headers["Musician Agency"]
    #     }
    #     res = self.client().delete("/musicians/10000", headers=header_obj)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 422)
    #     self.assertEqual(data["success"], False)
    #     self.assertEqual(data["message"], "unprocessable")

    #  Test routes with method ['POST']
    # ------------------------------------------------------------

    # def test_create_new_musician_for_Musician_Agency(self):
    #     header_obj = {
    #         "Authorization": self.auth_headers["Musician Agency"]
    #     }
    #     res = self.client().post('/musicians', json=self.new_musician, headers=header_obj)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(data['created'])
    #     self.assertTrue(len(data['musicians']))

# ------------------------------------------------------------------------------#
# Song part test
# ------------------------------------------------------------------------------#
   
    #  Test routes with method ['GET']
    # ------------------------------------------------------------

    # def test_get_song_for_Song_Producer(self):
    #     header_obj = {
    #         "Authorization": self.auth_headers["Song Producer"]
    #     }
    #     res = self.client().get('/songs', headers=header_obj)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(data['total_songs'])
    #     self.assertTrue(len(data['songs']))

    # def test_get_song_for_Musician_Agency(self):
    #     header_obj = {
    #         "Authorization": self.auth_headers["Musician Agency"]
    #     }
    #     res = self.client().get('/songs', headers=header_obj)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 403)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'], 'Permission not found.')

    # def test_get_specific_song_info_for_Song_Producer(self):
    #     header_obj = {
    #         "Authorization": self.auth_headers["Song Producer"]
    #     }
    #     res = self.client().get('/songs/3', headers=header_obj)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)

    # def test_404_get_specific_song_info(self):
    #     header_obj = {
    #         "Authorization": self.auth_headers["Song Producer"]
    #     }
    #     res = self.client().get('/songs/10000000000', headers=header_obj)
    #     data = json.loads(res.data)        

    #     self.assertEqual(res.status_code, 404)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'], 'resource not found')

    # def test_404_sent_requesting_beyond_valid_song_page(self):
    #     header_obj = {
    #         "Authorization": self.auth_headers["Song Producer"]
    #     }
    #     res = self.client().get('/songs?page=10000', headers=header_obj)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 404)
    #     self.assertEqual(data['success'], False)

    #  Test routes with method ['PATCHE''DELETE']
    # ------------------------------------------------------------

    def test_update_song_for_Song_Producer(self):
        header_obj = {
            "Authorization": self.auth_headers["Song Producer"]
        }
        res = self.client().patch("/songs/5", json={"cover_link":"sjkdlfjlkjwoeiur"}, headers=header_obj)
        data = json.loads(res.data)
        song = Song.query.filter(Song.id == 5).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(song.format()["cover_link"], "sjkdlfjlkjwoeiur")

    def test_400_for_failed_update_song(self):
        header_obj = {
            "Authorization": self.auth_headers["Song Producer"]
        }
        res = self.client().patch("/songs/5", headers=header_obj)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "bad request")

    def test_delete_song_for_Song_Producer(self):
        header_obj = {
            "Authorization": self.auth_headers["Song Producer"]
        }
        res = self.client().delete("/songs/8", headers=header_obj)
        data = json.loads(res.data)

        song = Song.query.filter(Song.id == 8).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["deleted"], 8)
        self.assertTrue(data["total_songs"])
        self.assertTrue(len(data["songs"]))
        self.assertEqual(song, None)

    def test_422_if_song_not_exist(self):
        header_obj = {
            "Authorization": self.auth_headers["Song Producer"]
        }
        res = self.client().delete("/songs/10000", headers=header_obj)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")

    #  Test routes with method ['POST']
    # ------------------------------------------------------------

    def test_create_new_song_for_Song_Producer(self):
        header_obj = {
            "Authorization": self.auth_headers["Song Producer"]
        }
        res = self.client().post('/songs', json=self.new_song, headers=header_obj)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(len(data['songs']))

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()