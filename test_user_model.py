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

    