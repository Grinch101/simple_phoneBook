import psycopg2
from psycopg2.pool import ThreadedConnectionPool
from psycopg2.extras import DictCursor, RealDictCursor
from psycopg2.extensions import AsIs
from pathlib import Path
from flask import g, make_response
import arrow
import json

##### Create Connection pool ######


def conn_pool(minconn, maxconn, /,
              host='localhost',
              database='phonebook',
              user='postgres',
              password=1):

    return ThreadedConnectionPool(minconn,
                                  maxconn,
                                  host=host,
                                  database=database,
                                  user=user,
                                  password=password)


############ query func  ##########
def query(query, vals=""):

    query = "c:/Users/MrGrinch/Desktop/tests/simple_phoneBook/sql/" + query + ".sql"
    path = Path(query)

    with open(path, 'r') as f:
        query_text = str(f.read())

    cur = g.conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(query_text, vals)
    return cur


############## convet date and time to datetime ############

def conv_datetime(date, time):
    date = str(date)
    time = str(time)

    arrow_time = arrow.get(f'{date} {time}', 'YYYY-MM-DD HH:mm')
    return arrow_time.format('h:m A - dddd MMM Do, YYYY')


################ Secure User info on appContext #############
def secure_g(g):
    user = dict(g.user)
    user.pop('passkey')
    return user


############## Convert cursor to dict type ###################

def fetcher(cur):
    if cur is not None:
        output = []
        for row in cur:
            output.append({**row})
        return output
    return []


# create an output dictionary containing
#  all information to return to the client #########

def json_output(message=None, data=None, error=None, http_code=200):

    return make_response(json.dumps({'info': message,
                                     'data': data,
                                     'error': error
                                     }), http_code)
