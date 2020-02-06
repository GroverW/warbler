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

    
    def test_new_message(self):
        """ Can a user make a new message """
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.u1.id
        
            resp = self.client.post("/messages/new", data={
                                                 "text":"This is a new test message"}
                                                  , follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<p>This is a new test message</p>", html)
            self.assertIn("<p>test message number one</p>", html)


    def test_new_blank_message(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.u1.id
        
            resp = self.client.post("/messages/new", data={
                                                 "text":""}
                                                  ,follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('This field is required.', html)
    

    def test_delete_message(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.u1.id
        
            message1 = Message.query.filter(Message.text=="test message number one").first()
            resp = self.client.post(f"/messages/{message1.id}/delete", follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertNotIn("<p>test message number one</p>", html)


    def test_delete_other_user_message(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.u1.id
        
            message2 = Message.query.filter(Message.text=="test message number two").first()
            
            resp = self.client.post(f"/messages/{message2.id}/delete", follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Access unauthorized", html)