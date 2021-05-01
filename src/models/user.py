from utility.helpers import query


####
class User():

    def __init__(self):
        pass

    def add(self, client_name, email, password):
        return query('user/register',
                     vals=(client_name, email, password))

    def get_by_email(self, email):
        if query('user/presence_using_email',
                 vals=(email,)).fetchone()['count'] == 1:
            return query('user/get_by_email', vals=(email,))
        else:
            return None

    def validate(self, email, password):
        if query('user/presence_using_email',
                 vals=(email,)).fetchone()['count'] == 1:
            row = query('user/get_by_email', vals=(email,))
            return password == row.fetchone()['passkey']
        else:
            return False

    def delete(self, user_id):
        if query('user/presence',
                 vals=(user_id,)).fetchone()['count'] == 1:
            return query('user/delete', vals=(user_id,))
        else:
            return False

    def get_all(self):

        return query('user/get_all')

    def update(self, user_id, new_email, new_name, new_password):
        if query('user/presence',
                 vals=(user_id,)).fetchone()['count'] == 1:
            return query('user/update',
                         vals=(new_email, new_password, new_name, user_id))
        else:
            return False

    def get_by_id(self, user_id):
        if query('user/presence', vals=(user_id,)).fetchone()['count'] == 1:
            cur = query('user/get_by_id', vals=(user_id,))
            return cur.fetchone()
        else:
            return False

    def clear_all(self):
        query('user/truncate')
