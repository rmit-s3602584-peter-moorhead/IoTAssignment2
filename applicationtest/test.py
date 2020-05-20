from appTest import app
import unittest

class test_api(unittest.TestCase):
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_login_page_loads(self):
        tester = app.test_client(self)
        response = tester.get('/')
        self.assertIn(b'Login', response.data)
        
        # Ensure login behaves correctly with correct credentials
    def test_correct_login(self):
        tester = app.test_client()
        response = tester.post(
            '/',
            data=dict(username="john", password="john"),
            follow_redirects=True
        )
        self.assertIn(b'Home page', response.data)

    # Ensure login behaves correctly with incorrect credentials
    def test_incorrect_login(self):
        tester = app.test_client()
        response = tester.post(
            '/',
            data=dict(username="wrong", password="wrong"),
            follow_redirects=True
        )
        self.assertIn(b'Incorrect username/password!', response.data)

    # Ensure logout behaves correctly
    def test_logout(self):
        tester = app.test_client()
        tester.post(
            '/',
            data=dict(username="john", password="john"),
            follow_redirects=True
        )
        response = tester.get('/logout', follow_redirects=True)
        self.assertIn(b'You were logged out', response.data)

    # Ensure that main page requires user login
    def test_main_route_requires_login(self):
        tester = app.test_client()
        response = tester.get('/home', follow_redirects=True)
        self.assertIn(b'You need to login first.', response.data)

    # Ensure that logout page requires user login
    def test_logout_route_requires_login(self):
        tester = app.test_client()
        response = tester.get('/logout', follow_redirects=True)
        self.assertIn(b'You need to login first.', response.data)

    # Ensure that posts show up on the main page
    def test_posts_show_up_on_main_page(self):
        tester = app.test_client()
        response = tester.post(
            '/',
            data=dict(username="admin", password="admin"),
            follow_redirects=True
        )
        self.assertIn(b'Hello from the shell', response.data)

if __name__ == '__main__':
    unittest.main()