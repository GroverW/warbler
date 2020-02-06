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

from app import app, session
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
        self.u.id = 1
        self.u2 = User.signup(
            email="test2@test.com",
            username="testuser2",
            password="HASHED_PASSWORD",
            image_url=""
        )
        self.u2.id = 2

        db.session.add_all([self.u, self.u2])
        db.session.commit()

        self.u = User.query.get(1)
        self.u2 = User.query.get(2)

        self.client = app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        

    def test_user_model(self):
        """Does basic model work?"""

        # User should have no messages & no followers
        self.assertEqual(len(self.u.messages), 0)
        self.assertEqual(len(self.u.followers), 0)

    def test_user_repr(self):
        """Does the user model repr function work?"""
    
        self.assertEqual(str(self.u), f"<User #{self.u.id}: testuser, test@test.com>" )


    def test_user_following(self):
        """ Does the following user feature work?"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess["curr_user"] = self.u.id
            
            id = self.u2.id
            resp = self.client.post(f"/users/follow/{id}", follow_redirects=True)

            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code, 200)
            self.assertIn("<p>@testuser2</p>", html)
        
        # """Issue was with teardown not resetting the auto incrementing IDs?"""

    
    def test_user_followers(self):
        """ Can other users follow us, and are they displayed?"""
        #Write later; right now, we have an issue where we can not have one user
        #access another user? We can only test if they display themselves.
    

    # def test_user_login(self, username, password):
    #     """ Can an user log in? """
    #     resp = self.client.post(f"/login", data = dict(username = self.u2.username, password = self.u2.password),
    #                                        follow_redirects=True)   
    #     html = resp.get_data(as_text=True)
        
    #     self.assertEqual(resp.status_code, 200)
    #     self.assertIn("Hello",html)