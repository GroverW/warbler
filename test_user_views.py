"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app, session, CURR_USER_KEY
app.config["DEBUG_TB_HOSTS"] = ["dont-show-debug-toolbar"]
app.config['WTF_CSRF_ENABLED'] = False
# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data




class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""
        app.config['SECRET_KEY'] = 'secret'
        db.create_all()
        User.query.delete()
        Message.query.delete()
        Follows.query.delete()


        self.u = User.signup(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD",
            image_url=""
        )

        self.u2 = User.signup(
            email="test2@test.com",
            username="testuser2",
            password="HASHED_PASSWORD",
            image_url=""
        )

        db.session.add_all([self.u, self.u2])
        db.session.commit()

        self.u1 = User.query.get(1)
        self.u2 = User.query.get(2)

        self.client = app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        

    def test_user_following(self):
        """ Does the following user feature work?"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.u1.id

            id = self.u2.id
            resp = self.client.post(f"/users/follow/{id}", follow_redirects=True)

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<p>@testuser2</p>", html)

        # """Issue was with teardown not resetting the auto incrementing IDs?"""

    def test_user_followers(self):
        """ Can other users follow us, and are they displayed?"""

        with self.client as c:
            id = self.u1.id
            
            # u2 is not initially following u1
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.u1.id

            resp = self.client.get(f"/users/{id}/followers")

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn("<p>@testuser2</p>", html)

            # u2 can follow u1
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.u2.id

            resp = self.client.post(f"/users/follow/{id}", follow_redirects=True)

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)

            # u2 is following u1
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.u1.id

            resp = self.client.get(f"/users/{id}/followers")

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<p>@testuser2</p>", html)

    def test_user_login(self):
        """ Can an user log in? """
        with self.client as c:
            resp = self.client.post("/login", data={
                                        "username": self.u2.username,
                                        "password": 'HASHED_PASSWORD'
                                        }, follow_redirects=True)   
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(f"Hello, {self.u2.username}", html)

    def test_create_user(self):
        """ Can you create a user? """
        with self.client as c:
            resp = self.client.post("/signup", data={
                                        "username": "testuser3",
                                        "password": "HASHED_PASSWORD",
                                        "email": "testuser3@gmail.com",
                                        "image_url": ""
                                        }, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<p>@testuser3</p>", html)
            self.assertNotIn("Username already taken", html)
    
    def test_create_user_fail(self):
        """ Can you fail to create a user? """
        with self.client as c:
            # No email
            resp = self.client.post("/signup", data={
                                        "username": "testuser3",
                                        "password": "HASHED_PASSWORD",
                                        "email": "",
                                        "image_url": ""
                                        }, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<span class="text-danger">This field is required.</span>', html)

            # Bad email
            resp = self.client.post("/signup", data={
                                        "username": "testuser3",
                                        "password": "HASHED_PASSWORD",
                                        "email": "notanemailaddress",
                                        "image_url": ""
                                        }, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<span class="text-danger">Invalid email address.</span>', html)

            # Username already taken
            resp = self.client.post("/signup", data={
                                        "username": "testuser",
                                        "password": "HASHED_PASSWORD",
                                        "email": "testuser@gmail.com",
                                        "image_url": ""
                                        }, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<div class="alert alert-danger">Username / Email already taken</div>', html)

            # Email already taken
            resp = self.client.post("/signup", data={
                                        "username": "testuser47",
                                        "password": "HASHED_PASSWORD",
                                        "email": "test@test.com",
                                        "image_url": ""
                                        }, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<div class="alert alert-danger">Username / Email already taken</div>', html)

