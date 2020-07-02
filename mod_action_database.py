import config
import mysql
from mysql.connector import Error


def connect_to_database():
    try:
        connection = mysql.connector.connect(host=config.db['hostname'], database=config.db['database'],
                                             user=config.db['user_id'], password=config.db['password'])

        if connection.is_connected():
            return connection

    except Error as e:
        print('Error connecting to MySQL', e)


def update_moderation_history(item, action, mod_to_action, channel_id, connection):
    updated = False
    post_title = ''

    try:
        post_title = item['post_title'].replace("\'", "\'\'")
    except:
        pass

    if post_title == '':
        try:
            post_title = item['item_text'].replace("\'", "\'\'")
        except:
            pass

    query = "INSERT INTO mod_action_history (fullname, subreddit_name, username, item_type, permalink, " \
            "item_text, mod_action, mod_to_action, mod_action_on, channel_id) " \
            "VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', NOW(), %s);" \
            % (item['fullname'], item['subreddit_name'], item['username'], item['item_type'],
               item['permalink'], post_title, action, mod_to_action, channel_id)

    try:
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        updated = True
    except Error as error:
        print(error)
    except Exception as error:
        print(error)

    return updated
