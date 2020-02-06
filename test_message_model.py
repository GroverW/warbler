""" Message model tests"""

import os
from unittest import TestCase

from models import db, User, Message, Follows

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app, session, CURR_USER_KEY
app.config["DEBUG_TB_HOSTS"] = ["dont-show-debug-toolbar"]
app.config['WTF_CSRF_ENABLED'] = False


class MessageModelTestCase(TestCase):
    """ Test for message model"""

    def setUp(self):
        """Create test client, add sample data."""
        app.config['SECRET_KEY'] = 'secret'
        db.create_all()
        User.query.delete()
        Message.query.delete()
        Follows.query.delete()


        self.u1 = User.signup(
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

        db.session.add_all([self.u1, self.u2])
        db.session.commit()

        self.u1 = User.query.filter_by(username=self.u1.username).first()
        self.u2 = User.query.filter_by(username=self.u2.username).first()

        message1 = Message(text="test message number one", user_id = self.u1.id)
        message2 = Message(text="test message number two", user_id = self.u2.id)
       
        db.session.add_all([message1, message2])
        db.session.commit()


        self.client = app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    
    def test_message_model(self):
        """ Does message model work? """

        self.assertEqual(len(self.u1.messages), 1)
        self.assertEqual(len(self.u2.messages), 1)
    

       