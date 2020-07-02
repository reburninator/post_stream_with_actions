import config
import post_queue_database
import mod_action_database
import praw

reddit = praw.Reddit(client_id=config.redditapp['client_id'],
                     client_secret=config.redditapp['client_secret'],
                     password=config.redditapp['password'],
                     user_agent=config.redditapp['user_agent'],
                     username=config.redditapp['user_id'])


def process_mod_action(channel_id, message_id, discord_username, action):
    connection = post_queue_database.connect_to_database()

    item = post_queue_database.get_modqueue_item_by_discord_message_id(message_id, connection)

    if action == 'approve':
        approve(channel_id, item, discord_username, message_id, connection)

    if action == 'remove':
        remove(channel_id, item, discord_username, message_id, connection)


def approve(channel_id, item, discord_username, message_id, connection):
    item_type = 'Submission'
    permalink = item['permalink']

    try:
        submission = reddit.submission(url=permalink)
        fullname = submission.fullname
        subreddit_name = config.subreddit_name

        username = ''
        if submission.author is not None:
            username = submission.author.name
        else:
            username = 'Not available'

        title = submission.title[0:1000]

        item_text = title.replace("\'", "\'\'")

        item = {'fullname': fullname, 'subreddit_name': subreddit_name,
                'username': username, 'item_type': item_type,
                'permalink': permalink, 'discord_username': discord_username,
                'item_text': item_text, 'channel_id': channel_id}

        submission.mod.approve()
        mod_action_database.update_moderation_history(item, 'approve', discord_username, channel_id, connection)
        post_queue_database.delete_item_from_post_modqueue(message_id)
    except:
        print('Could not approve item')


def remove(channel_id, item, discord_username, message_id, connection):
    item_type = 'Submission'
    permalink = item['permalink']

    try:
        submission = reddit.submission(url=permalink)
        fullname = submission.fullname
        subreddit_name = config.subreddit_name

        username = ''
        if submission.author is not None:
            username = submission.author.name
        else:
            username = 'Not available'

        title = submission.title[0:1000]

        item_text = title.replace("\'", "\'\'")

        item = {'fullname': fullname, 'subreddit_name': subreddit_name,
                'username': username, 'item_type': item_type,
                'permalink': permalink, 'discord_username': discord_username,
                'item_text': item_text, 'channel_id': channel_id}

        submission.mod.remove()
        submission.mod.flair(text='Removed', css_class=None)
        mod_action_database.update_moderation_history(item, 'remove', discord_username, channel_id, connection)
        post_queue_database.delete_item_from_post_modqueue(message_id)
    except:
        print('Could not approve item')
