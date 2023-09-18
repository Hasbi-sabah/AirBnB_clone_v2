#!/usr/bin/python3
""" Module for testing DB storage"""

from models import storage
from models.engine import db_storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

import inspect
import os
import unittest

env_value = os.environ.get('HBNB_TYPE_STORAGE')
known_classes = {"Amenity": Amenity, "City": City, "Place": Place,
                 "Review": Review, "State": State, "User": User}

user = os.environ.get('HBNB_MYSQL_USER')
pwd = os.environ.get('HBNB_MYSQL_PWD')
host = os.environ.get('HBNB_MYSQL_HOST')
database = os.environ.get('HBNB_MYSQL_DB')
env = os.environ.get('HBNB_ENV')

DBStorage = None
if env_value == "db":
    DBStorage = db_storage.DBStorage

if env_value == 'db':
    # print(f"user: {user}, password: {pwd}, host: {host}")

    class test_DBStorage(unittest.TestCase):
        """ a class that tests the DB storage method """
        def setUp(self):
            """ Set up test environment """
            try:
                self.engine = create_engine(f"mysql+mysqldb://{user}:{pwd}@{host}/{database}",
                                            pool_pre_ping=True)
                self.Session = sessionmaker(bind=self.engine)
            except SQLAlchemyError as e:
                print(f"Error connecting to the database: {e}")
            self.db_func = inspect.getmembers(DBStorage, inspect.isfunction)

        def test_docstring(self):
            """Test for the DBStorage class docstring"""
            if not DBStorage:
                return
            self.assertIsNot(DBStorage.__doc__, None)
            self.assertTrue(len(DBStorage.__doc__) >= 1,
                            "DBStorage class needs a docstring")

        def test_methods_docstrings(self):
            """Test for the presence of docstrings in DBStorage methods"""
            for func in self.db_func:
                self.assertIsNot(func[1].__doc__, None,
                                 "{:s} method needs a docstring".format(func[0]))
                self.assertTrue(len(func[1].__doc__) >= 1,
                                "{:s} method needs a docstring".format(func[0]))

        def test_module_docstring(self):
            """Test for the db_storage.py module docstring"""
            self.assertIsNot(db_storage.__doc__, None,
                             "db_storage.py needs a docstring")
            self.assertTrue(len(db_storage.__doc__) >= 1,
                            "db_storage.py needs a docstring")

        def tearDown(self):
            """ Remove storage file at end of tests """
            """cleanup actions go here"""
            metadata = MetaData()
            metadata.drop_all(self.engine, checkfirst=False)
            self.engine.dispose()

        def test_new(self):
            """ test case for creation of newly created instances """
            session = self.Session()

            new_review = Review()
            new_user = User()
            new_city = City()
            new_state = State()
            new_amenity = Amenity()
            new_place = Place()

            new_review.place_id = new_place.id
            new_review.user_id = new_user.id
            new_review.text = "this is a good place bro"

            new_amenity.name = "wifi"
            new_amenity.place_amenities.append(new_place)

            new_place.city_id = new_city.id
            new_place.user_id = new_user.id
            new_place.name = "johannesburg"
            new_place.description = "the capital of SA"
            new_place.number_rooms = 5
            new_place.max_guest = 9
            new_place.price_by_night = 100
            new_place.latitude = 12.0
            new_place.longitude = 15.5
            new_place.reviews.append(new_review)

            new_city.name = "lost city of arthemis"
            new_city.state_id = new_state.id
            new_city.places.append(new_place)

            new_state.name = "california"
            new_state.cities.append(new_city)

            new_user.email = "mail@google.com"
            new_user.password = "googlepassw0rd"
            new_user.first_name = "hazel"
            new_user.last_name = "hasbi"
            new_user.places.append(new_place)
            new_user.reviews.append(new_review)

            all_entries = [new_amenity, new_place, new_city, new_state, new_user]
            session.add_all(all_entries)
            session.commit()
            # session.close()

            # session = self.Session()
            res_user = session.query(User).filter(User.first_name == "hazel").first()
            # print(f"id is {res_user.id}")

            self.assertIsNotNone(res_user)
            self.assertEqual(res_user.first_name, "hazel")
            self.assertIsNotNone(res_user.places)
            session.close()

            # session = self.Session()
            # res_review = session.query(Review).filter(Review.text == "this is a good place bro").first()
            # print("result review:")
            # print(res_review)
            # print("new review:")
            # print(new_review)
            # self.assertEqual(res_review, new_review)
            # session.close()

        def test_all(self):
            """ test case for the proper return of all instances of a class """

        def test_save(self):
            """ test case for DBStorage save method """

        def test_delete(self):
            """ test case for DBStorage delete method """

        def test_reload(self):
            """ test case for reloading the DB storage """
