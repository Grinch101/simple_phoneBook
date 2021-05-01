# import sys
# sys.path.insert(0, "c:/Users/MrGrinch/Desktop/tests/simple_phoneBook")
from app import app
from src.config import TestingConfig
import pytest
import json
from flask import g, Response


@pytest.fixture
def app_runner():
    global app
    global TestingConfig
    app.config.from_object(TestingConfig)
    return app


@pytest.fixture
def app_ctx(app_runner):
    with app.app_context():
        yield app


@pytest.fixture
def client(app_runner):
    with app.test_client() as client:
        yield client


# TESTS:

def test_g_contents(app_ctx):
    with app.test_request_context():
        app.preprocess_request()
        assert g.conn is not None
        app.process_response(Response('This is an empty response!'))
        # An empty response was passed to make the process_response work!
        assert g.conn is None


def test_signup(client):
    rs = client.post('/auth/signup',
                     data={'inputEmail': 'SomeEmail@gmail.com',
                           'inputPassword': 'A',
                           'client_name': 'NedaForTest'}
                     )
    data = json.loads(rs.data)['data']
    error = json.loads(rs.data)['error']
    assert error is None
    assert data is not None
    assert rs.status_code == 201


def test_signup2(app_runner):  # using request context instead of test_client
    with app.test_request_context('/auth/signup',
                                  data={'inputEmail': 'Neda',
                                        'inputPassword': 'Neda',
                                        'client_name': 'NedaForTest'},
                                  method="POST"):
        app.preprocess_request()
        rs = app.dispatch_request()
        rs = app.process_response(rs)
        data = json.loads(rs.data)['data']
        error = json.loads(rs.data)['error']
        assert error is None
        assert data is not None
        assert rs.status_code == 201


def test_login(client):
    rs = client.post('/auth/login',
                     data={'inputEmail': 'Masoud@gmail.com',
                           # this user is present in database permanently
                           'inputPassword': 'A'})
    data = json.loads(rs.data)['data']
    error = json.loads(rs.data)['error']
    with open('token.txt', 'w') as f:
        f.write(data)
        f.close()
    assert rs.status_code == 200
    assert error is None
    assert data is not None


# this test fails, note the status codes
def test_login2(app_runner):
    with app.test_client() as client:
        rs = client.post('/auth/signup',
                         data={'inputEmail': 'SomeNewEmail@gmail.com',
                               'inputPassword': 'A',
                               'client_name': 'ForTest'}
                         )
        data = json.loads(rs.data)['data']
        error = json.loads(rs.data)['error']
        assert error is None
        assert data is not None
        assert rs.status_code == 201
        rs2 = client.post('/auth/login',
                          data={'inputEmail': 'SomeNewEmail@gmail.com',
                                'inputPassword': 'A'})
        data = json.loads(rs2.data)['data']
        error = json.loads(rs2.data)['error']
        assert error is None
        assert rs2.status_code == 200


def test_current_user(client):
    with open('token.txt', 'r') as f:
        token = f.read()
        print(token)
        # read the token written in the previous test
        # for the permanent user (test: mark.three)
    rs = client.get('/auth/current_user',
                    headers={'JWT': f'{token}'})
    data = json.loads(rs.data)['data']
    error = json.loads(rs.data)['error']
    assert rs.status_code == 200
    assert error is None
    assert data is not None


def test_login3(app_runner):
    with app.test_request_context('/auth/signup',
                                  data={'inputEmail': 'Neda2',
                                        'inputPassword': 'Neda',
                                        'client_name': 'NedaForTest'},
                                  method="POST"):
        app.preprocess_request()
        rs = app.dispatch_request()
        with app.test_request_context('/auth/login',
                                      data={'inputEmail': 'Neda2',
                                            'inputPassword': 'Neda'},
                                      method="POST"):
            app.preprocess_request()
            rs1 = app.dispatch_request()
            # app.process_response(rs)
            # app.process_response(rs1)
    token = json.loads(rs1.data)['data']
    error = json.loads(rs1.data)['error']
    with open('new_user_token.txt', 'w') as f:
        f.write(error)
        f.close()
    assert token is not None
    assert error is None
    assert rs.status_code == 201
    assert rs1.status_code == 200
