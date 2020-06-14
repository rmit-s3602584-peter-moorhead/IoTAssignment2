from IoTAssignment2.api import app
import unittest


class FlaskTestCase(unittest.TestCase):
    """
    Unit test 
    """

    # Ensure that flask was set up correctly
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    # Ensure that the login page loads correctly
    def test_login_page_loads(self):
        tester = app.test_client(self)
        response = tester.get('/')
        self.assertIn(b'Login', response.data)

    # Ensure login behaves correctly with correct credentials
    def test_correct_admin_login(self):
        tester = app.test_client()
        response = tester.post(
            '/',
            data=dict(username="admin1", password="admin1"),
            follow_redirects=True
        )
        self.assertIn(b'Home page', response.data)

    # Ensure login behaves correctly with correct credentials
    def test_correct_engineer_login(self):
        tester = app.test_client()
        response = tester.post(
            '/',
            data=dict(username="Engineer1", password="Engineer1"),
            follow_redirects=True
        )
        self.assertIn(b'Engineer Page', response.data)

    # Ensure login behaves correctly with correct credentials
    def test_correct_Manager_login(self):
        tester = app.test_client()
        response = tester.post(
            '/',
            data=dict(username="frank", password="frank"),
            follow_redirects=True
        )
        self.assertIn(b'Manager', response.data)

    # Ensure login behaves correctly with correct credentials
    def test_correct_customer_login(self):
        tester = app.test_client()
        response = tester.post(
            '/',
            data=dict(username="Green", password="Green"),
            follow_redirects=True
        )
        self.assertIn(b'User History', response.data)

    # Ensure login behaves correctly with correct credentials
    def test_correct_login(self):
        tester = app.test_client()
        response = tester.post(
            '/',
            data=dict(username="admin1", password="admin1"),
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

    # Ensure that main page requires user login
    def test_main_route_requires_login(self):
        tester = app.test_client()
        response = tester.get('/home', follow_redirects=True)
        response = tester.get('/', follow_redirects=True)

    # Ensure login behaves correctly with correct credentials
    def test_correct_register(self):
        tester = app.test_client()
        response = tester.post(
            '/register',
            data=dict(username="test1", password="test1", firstName ="test1" , lastName= "test1", email= "test1@test1.com"),
            follow_redirects=True
        )
        self.assertIn(b'Login', response.data)

    # Ensure Cars loads correctly
    def test_correct_cars(self):
        tester = app.test_client()
        response = tester.post(
            '/',
            data=dict(username="admin1", password="admin1"),
            follow_redirects=True
        )
        response = tester.get('/cars', follow_redirects=True)
        self.assertIn(b'Car Search', response.data)

    # Ensure Profile loads correctly
    def test_correct_cars(self):
        tester = app.test_client()
        response = tester.post(
            '/',
            data=dict(username="admin1", password="admin1"),
            follow_redirects=True
        )
        response = tester.get('/profile', follow_redirects=True)
        self.assertIn(b'Profile Page', response.data)

    # Ensure cars loads correctly
    def test_correct_cars(self):
        tester = app.test_client()
        response = tester.post(
            '/',
            data=dict(username="admin1", password="admin1"),
            follow_redirects=True
        )
        response = tester.get('/cars', follow_redirects=True)
        self.assertIn(b'Ford Falcon', response.data)

    # Ensure cars searchcorrectly
    def test_search_correcrt(self):
        tester = app.test_client()
        response = tester.post(
            '/',
            data=dict(username="admin1", password="admin1"),
            follow_redirects=True
        )
        response = tester.get('/cars', follow_redirects=True)
        response = tester.post(
            '/cars',
            data=dict(idCar="9"),
            follow_redirects=True
        )
        response = tester.get('/cars', follow_redirects=True)
        self.assertIn(b'Honda', response.data)

    # Ensure cars history table loads
    def test_car_history(self):
        tester = app.test_client()
        response = tester.post(
            '/',
            data=dict(username="admin1", password="admin1"),
            follow_redirects=True
        )
        response = tester.get('/home', follow_redirects=True)
        self.assertIn(b'Booking Id', response.data)
    
    # Ensure cars searchcorrectly
    def test_search_user_correct(self):
        tester = app.test_client()
        response = tester.post(
            '/',
            data=dict(username="admin1", password="admin1"),
            follow_redirects=True
        )
        response = tester.get('/searchDatabase', follow_redirects=True)
        response = tester.post(
            '/searchDatabase',
            data=dict(firstName="admin1"),
            follow_redirects=True
        )
        response = tester.get('/searchDatabase', follow_redirects=True)
        self.assertIn(b'admin1', response.data)

    # Ensure cars searchcorrectly
    def test_search_user_correct(self):
        tester = app.test_client()
        response = tester.post(
            '/',
            data=dict(username="admin1", password="admin1"),
            follow_redirects=True
        )
        response = tester.get('/searchDatabase', follow_redirects=True)
        response = tester.post(
            '/searchDatabase',
            data=dict(firstName="admin1"),
            follow_redirects=True
        )
        response = tester.get('/searchDatabase', follow_redirects=True)
        self.assertIn(b'admin1', response.data)



if __name__ == '__main__':
    unittest.main()
