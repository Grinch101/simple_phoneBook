from utility.helpers import query


####
class Contact():
    
    def __init__(self):
        pass

    def add(self, user_id, name, phone):

        return query('contact/insert',
              vals=(user_id, name, phone))


    def get_by_user(self, user_id):

        return query('contact/get_by_user', vals=(user_id,))


    def get_by_id(self, row_id):
        cur = query('contact/get_by_id', vals=(row_id,))
        return cur.fetchone()


    def get_all(self):

        return query('contact/get_all')
        

    def delete(self, row_id):

        return query('contact/delete', vals=(row_id,row_id)) # Can you suggest sth better?

    def update(self, row_id, new_entry):

        row_id = new_entry['id']
        name = new_entry['name']
        phone = new_entry['phone']

        return query('contact/update', vals=(name,
                                      phone, row_id))


    def clear_all(self):
        
        return query('contact/truncate')