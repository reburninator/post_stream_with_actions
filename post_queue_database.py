import config
import mysql
from mysql.connector import Error


def connect_to_database():
    try:
        connection = mysql.connector.connect(host=config.db['hostname'],
                                             database=config.db['database'],
                                             user=config.db['user_id'],
                                             password=config.db['password'])

        if connection.is_connected():
            return connection

    except Error as e:
        print('Error connecting to MySQL', e)


def check_if_previously_queued(item, connection):
    previously_queued = False
    fullname = item['fullname']

    query = "SELECT fullname FROM post_queue " \
            "WHERE fullname = '%s';" % item['fullname']

    try:
        cursor = connection.cursor()
        cursor.execute(query)
        records = cursor.fetchall()
        for record in records:
            previously_queued = True
    except Error as error:
        print(error)

    return previously_queued


def add_item_to_post_queue(item, connection):
    added = False
    post_title = item['post_title'].replace("\'", "\'\'")
    selftext = item['selftext'].replace("\'", "\'\'")

    query = "INSERT INTO post_queue (fullname, subreddit_name, username, post_title, " \
            "ban_note, permalink, number_of_reports, created_utc, url, selftext, location) " \
            "VALUES ('%s', '%s', '%s', '%s', '%s', '%s', %s, %s, '%s', '%s', '%s');" % \
            (item['fullname'], item['subreddit_name'], item['username'], post_title,
             item['ban_note'], item['permalink'], item['number_of_reports'], item['created_utc'],
             item['url'], selftext, item['location'])

    try:
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        added = True
    except Error as error:
        print(error)

    return added


def delete_from_post_queue(permalink):
    deleted = False
    connection = connect_to_database()

    query = "DELETE FROM post_queue WHERE permalink = '%s';" % permalink

    try:
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        cursor.close()
        deleted = True
    except Error as error:
        print(error)

    return deleted


def update_post_with_message_id(permalink, message_id):
    updated = False
    connection = connect_to_database()

    query = "UPDATE post_queue SET message_id = %s WHERE permalink = '%s';" % (message_id, permalink)

    try:
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        cursor.close()
        updated = True
    except Error as error:
        print(error)

    return updated


def get_modqueue_item_by_discord_message_id(message_id, connection):
    item = {'item_type': '', 'permalink': ''}

    query = "SELECT permalink FROM post_queue WHERE message_id = %s;" % message_id

    try:
        cursor = connection.cursor()
        cursor.execute(query)
        records = cursor.fetchall()
        for record in records:
            item = {'item_type': 'Submission', 'permalink': record[0]}
    except Error as error:
        print(error)

    return item


def delete_item_from_post_modqueue(message_id):
    connection = connect_to_database()

    query = "DELETE FROM post_queue WHERE message_id = %s" % message_id

    try:
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
    except Error as error:
        print(error)

    connection.close()