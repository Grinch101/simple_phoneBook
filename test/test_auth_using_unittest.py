import unittest
from app import app, connections
from src.config import TestingConfig
import json
from flask import g, current_app, Response


class test_api_flask(unittest.TestCase):
    app.config.from_object(TestingConfig)

    def test_signup(self):
        with app.test_client() as client:
            r = client.post('/auth/signup',
                        data={'inputEmail':'SomeEmail@gmail.com',
                            'inputPassword':'A',
                            'client_name':'NedaForTest'}
                            )
            self.assertEqual(r.status_code, 201)
            self.assertEqual(json.loads(r.data)['info'], 'user created!')

    def test_g_contents(self):
        with app.app_context():
            with app.test_request_context():
                app.preprocess_request()
                # now g must be initialzed in our before_request func
                self.assertIsNotNone(g.conn)
                app.process_response(Response())
                # Now the connection must be rolled back, closed and g.conn set to None
                self.assertIsNone(g.conn)

if __name__=="__main__":
    unittest.main()