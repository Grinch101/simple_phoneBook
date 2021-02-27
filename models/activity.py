from utility.helpers import query, conv_datetime
import arrow


class Activity():

    def __init__(self):
        pass

    def add(self, action, description, date, time, user_id, contact_id):

        arrow_time = conv_datetime(date, time)
        query('activity/insert', vals=(action,
                                       description, arrow_time, user_id, contact_id))


    def get_all(self, user_id, contact_id):

        return query('activity/get_all', vals=(user_id, contact_id))


    def delete(self, activity_id, contact_id, user_id):

        query('activity/delete', vals=(activity_id, contact_id, user_id))
