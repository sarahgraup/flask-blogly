import os

os.environ["DATABASE_URL"] = "postgresql:///blogly"

from unittest import TestCase

from app import app, db
from models import User

# DEFAULT_IMAGE_URL - further study

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.drop_all()
db.create_all()


class UserViewTestCase(TestCase):
    """Test views for users."""

    def setUp(self):
        """Create test client, add sample data."""

        # As you add more models later in the exercise, you'll want to delete
        # all of their records before each test just as we're doing with the
        # User model below.
        User.query.delete()

        self.client = app.test_client()

        test_user = User(
            first_name="test1_first",
            last_name="test1_last",
            image_url=None,
        )

        db.session.add(test_user)
        db.session.commit()

        # We can hold onto our test_user's id by attaching it to self (which is
        # accessible throughout this test class). This way, we'll be able to
        # rely on this user in our tests without needing to know the numeric
        # value of their id, since it will change each time our tests are run.
        self.user_id = test_user.id

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    def test_list_users(self):
        with self.client as c:
            resp = c.get("/users")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("test1_first", html)
            self.assertIn("test1_last", html)

    def add_user(self):
        """Test adding user and redirects"""

        with self.client as c:
            resp = c.post('/users/new', data={
                'first_name':'James',
                'last_name':'Smith',
                'image_url':'https://images.unsplash.com/photo-1603415526960-f7e0'
                 + '328c63b1?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfH'
                 + 'x8fGVufDB8fHx8&auto=format&fit=crop&w=1170&q=80'
            }, follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)

            self.assertIn('James Smith', html)
    
    def show_user_details(self):
        """Test getting user details"""

        with self.client as c:
            resp = c.get('/users/{self.user_id}')

            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn('test1_first test1_last', html)


    def edit_user(self):
        """ Test changing user data"""

        with self.client as c:
            resp = c.post('/users/{self.user_id}/edit', data={
                'first_name':'Kevin',
                'last_name':'Matthews',
            }, follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)

            self.assertIn('Kevin Mathews', html)
            self.assertEqual(resp.location, '/users')
            

    def delete_user(self):
        """ Test deleting user data"""
        
        with self.client as c:
            resp = c.post('/users/{self.user_id}/delete', follow_redirects = True)

            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)

            self.assertNotIn('Kevin Mathews', html)
            self.assertEqual(resp.location, '/users')








