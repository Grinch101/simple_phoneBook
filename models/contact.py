from utility.helpers import query
from utility.decor import path_set
from flask import g


####
class Contact():
    def __init__(self):
        pass

    @path_set(path='SQL/contact')
    def add(self, userid, contact_name, contact_phone,  path):

        query(path, 'insert',
              vals=(userid, contact_name, contact_phone))

    @path_set(path='SQL/contact')
    def find_book(self, userid, path):
        query(path, 'get_by_id', vals=(userid,))
        cur = g.cur
        rows = cur.fetchall()
        dic_list = []
        for row in rows:
            dic_list.append(
                {'client_name': row['client_name'],
                    'name': row['contact_name'],
                    'phone': row['contact_phone'],
                    'id': row['id']})
        return dic_list

    # @path_set(path='SQL/contact')
    # def find_row(self, row_id , path):
    #     rows = query(path , 'row_info' , vals=(row_id,))
    #     return rows[0]

    # @path_set(path='SQL/contact')
    # def leave_comment(self,comment, posting_date, row_id , contact_name, path):
    #     query(path , 'comment' , vals=(comment,posting_date,row_id, contact_name))

    @path_set(path='SQL/contact')
    def get_all(self, path):
        query(path, 'get_all')
        cur = g.cur
        rows = cur.fetchall()
        dic_list = []
        for row in rows:
            dic_list.append(
                    {'name': row['contact_name'],
                    'phone': row['contact_phone'],
                    'userid': row['userid']})
        return dic_list
        

    @path_set(path='SQL/contact')
    def delete(self, row_id, path):
        query(path, 'delete', vals=(row_id,))

    @path_set(path='SQL/contact')
    def update(self, row_id, new_entry, path):

        userid = new_entry['userid']
        contact_name = new_entry['name']
        contact_phone = new_entry['phone']

        query(path, 'update', vals=(contact_name,
                                    contact_phone, userid))

    @path_set(path='SQL/contact')
    def clear_all(self, path):
        query(path, 'truncate')
