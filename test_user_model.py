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
        

    def test_user_model(self):
        """Does basic model work?"""

        # User should have no messages & no followers
        self.assertEqual(len(self.u1.messages), 0)
        self.assertEqual(len(self.u1.followers), 0)

    def test_user_repr(self):
        """Does the user model repr function work?"""

        self.assertEqual(str(self.u1), f"<User #{self.u1.id}: testuser, test@test.com>" )

    def test_user_is_followed_by(self):
        """ Can we check if a user is being followed by another user correctly?"""
    
        # Check before we have user 2 follow user 1: should be False
        self.assertEqual(self.u2.is_following(self.u1), False)

        # Have user 2 follow user 1 and check again: should be True
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.u2.id
            self.client.post(f"/users/follow/{self.u1.id}", follow_redirects=True)
            
            self.u1 = User.query.get(1)
            self.u2 = User.query.get(2)
            
            self.assertEqual(self.u1.is_followed_by(self.u2), True)
            
    def test_user_is_following(self):
        """ Can we check if a user is following another user correctly?"""

        # Check before we have user 1 follow user 2: should be False
        self.assertEqual(self.u1.is_following(self.u2), False)

        # Have user 1 follow user 2 and check again: should be True
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.u1.id
            self.client.post(f"/users/follow/{self.u2.id}", follow_redirects=True)
            
            self.u1 = User.query.get(1)
            self.u2 = User.query.get(2)
            
            self.assertEqual(self.u1.is_following(self.u2), True)
        
    def test_user_is_blocking(self):
        """ Can we check is a user is blocking another user correctly? """

        # Check before we have user 1 block user 2: should be False
        self.assertEqual(self.u1.is_blocking(self.u2), False)

        # Have user 1 block user 2 and check again: should be True
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.u1.id
            self.client.post(f"/users/block/{self.u2.id}", follow_redirects=True)
            
            self.u1 = User.query.get(1)
            self.u2 = User.query.get(2)
            
            self.assertEqual(self.u1.is_blocking(self.u2), True)
    
    def test_user_authenticate(self):
        """ Does the User class method 'authenticate' work? """

        # When valid password and username is entered:
        result = User.authenticate("testuser","HASHED_PASSWORD")
        self.assertEqual(bool(result), True)

        #When invalid username is entered:
        result = User.authenticate("invalid_username","HASHED_PASSWORD")
        self.assertEqual(bool(result), False)

        #When invalid passowrd is entered:
        result = User.authenticate("testuser","NOT_VALID_PASS")
        self.assertEqual(bool(result), False)
    
    # def test_user_signup: Testing the User Class method was left our
    # as we are using the signup method in our setup; if it did not work
    # none of our other tests would be working.