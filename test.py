from unittest import TestCase
from flask import session
from app import app
from models import db, User, Post


class BloglyTests(TestCase):

    def setUp(self):
        """Clear the User and Post tables before testing."""
        User.query.delete()
        Post.query.delete()
    
    def tearDown(self):
        """Remove any incomplete database transactions."""
        db.session.rollback()
    
    def add_test_user(self, client):
        form_data = {"first_name":"Test_first", "last_name":"Test_last"}
        return client.post("/users/new", data=form_data, follow_redirects=True)
    
    def add_user_and_post(self, client):
        self.add_test_user(client)
        test_user = User.query.filter_by(first_name="Test_first").first()
        post_data = {"title":"First Post", "content":"Lorem ipsum"}
        return client.post(f"/users/{test_user.id}/posts/new", data=post_data, follow_redirects=True)

    def test_display_users(self):
        """Test that the index response is received correctly 
            and has the expected content."""
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Users", html)
            self.assertIn(">Add User</button>", html)
    
    def test_add_user_form(self):
        """Test that the new user response is received correctly 
            and has the expected content."""
        with app.test_client() as client:
            resp = client.get("/users/new")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Add New User", html)
    
    def test_adding_user(self):
        """Test adding a new user and displaying it."""
        with app.test_client() as client:
            resp = self.add_test_user(client)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Users", html)
            self.assertIn(">Add User</button>", html)
            self.assertIn("Test_first Test_last", html)
    
    def test_editing_user(self):
        """Test editing a user's details."""
        with app.test_client() as client:
            self.add_test_user(client)
            test_user = User.query.filter_by(first_name="Test_first").first()

            updated_form_data = {"first_name":"Test_Updated_First", "last_name":"Test_Updated_Last"}
            resp = client.post(f"/users/{test_user.id}/edit", data=updated_form_data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Test_Updated_First Test_Updated_Last", html)


    
    def test_deleting_user(self):
        """Test deleting a user from the users list."""
        with app.test_client() as client:
            resp = self.add_test_user(client)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Test_first Test_last", html)

            test_user = User.query.filter_by(first_name="Test_first").first()

            resp = client.post(f"/users/{test_user.id}/delete", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn("Test_first Test_last", html)

    def test_no_posts(self):
        """Test that a user without posts displays the appropriate message"""
        with app.test_client() as client:
            self.add_test_user(client)
            test_user = User.query.filter_by(first_name="Test_first").first()

            resp = client.get(f"/users/{test_user.id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Test_first Test_last has no posts yet", html)


    def test_adding_post(self):
        """Test adding a new post, redirecting correctly, then displaying it."""
        with app.test_client() as client:
            resp = self.add_user_and_post(client)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Test_first Test_last's Posts", html)

            test_post = Post.query.filter_by(title="First Post").first()

            resp = client.get(f"/posts/{test_post.id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Lorem ipsum", html)
            self.assertIn("Return To User", html)
    
    def test_editing_post(self):
        """Test adding a post and editing it."""
        with app.test_client() as client:
            resp = self.add_user_and_post(client)

            test_post = Post.query.filter_by(title="First Post").first()
            post_data = {"title":"", "content":"Lorem edited"}
            resp = client.post(f"/posts/{test_post.id}/edit", data=post_data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("First Post", html)
            self.assertIn("Lorem edited", html)
    
    def test_deleting_post(self):
        """Test adding a post and deleting it."""
        with app.test_client() as client:
            resp = self.add_user_and_post(client)

            test_post = Post.query.filter_by(title="First Post").first()
            resp = client.post(f"/posts/{test_post.id}/delete", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Test_first Test_last has no posts yet", html)
