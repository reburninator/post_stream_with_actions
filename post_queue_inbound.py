import config
import post_queue_database
import post_queue_stream
import praw
import discord
from operator import itemgetter


reddit = praw.Reddit(client_id=config.redditapp['client_id'],
                     client_secret=config.redditapp['client_secret'],
                     password=config.redditapp['password'],
                     user_agent=config.redditapp['user_agent'],
                     username=config.redditapp['user_id'])


def get_new_posts():
    items = []

    connection = post_queue_database.connect_to_database()
    subreddit_name = config.subreddit_name

    stop = False
    submissions = reddit.subreddit(subreddit_name).new(limit=config.post_limit)
    for submission in submissions:
        if stop:
            break

        created_utc = int(submission.created_utc)
        if submission.approved_by is not None:
            print('Already approved by ' + submission.approved_by)
            continue

        if created_utc < config.starting_utc:
            continue

        if submission.num_reports > 0:
            continue

        username = ''
        if submission.author is not None:
            username = submission.author.name

        ban_note = ''
        if hasattr(submission, 'ban_note'):
            if submission.ban_note is not None:
                ban_note = submission.ban_note

        selftext = ''
        if hasattr(submission, 'selftext'):
            if submission.selftext is not None:
                selftext = submission.selftext[0:500]

        fullname = submission.fullname
        permalink = 'https://www.reddit.com' + submission.permalink
        post_title = submission.title
        url = submission.url
        number_of_reports = submission.num_reports

        item = {'created_utc': created_utc, 'fullname': fullname, 'subreddit_name': subreddit_name,
                'username': username,'permalink': permalink, 'post_title': post_title, 'url': url,
                'selftext': selftext, 'ban_note': ban_note, 'number_of_reports': number_of_reports,
                'location': 'newqueue'}

        if not post_queue_database.check_if_previously_queued(item, connection):
            post_queue_database.add_item_to_post_queue(item, connection)
            items.append(item)
        else:
            stop = True

    modqueue = reddit.subreddit(subreddit_name).mod.modqueue(only='submissions')
    for submission in modqueue:
        created_utc = int(submission.created_utc)

        username = ''
        if submission.author is not None:
            username = submission.author.name

        ban_note = ''
        if hasattr(submission, 'ban_note'):
            if submission.ban_note is not None:
                ban_note = submission.ban_note

        selftext = ''
        if hasattr(submission, 'selftext'):
            if submission.selftext is not None:
                selftext = submission.selftext[0:500]

        fullname = submission.fullname
        permalink = 'https://www.reddit.com' + submission.permalink
        post_title = submission.title
        url = submission.url
        number_of_reports = submission.num_reports

        item = {'created_utc': created_utc, 'fullname': fullname, 'subreddit_name': subreddit_name,
                'username': username,'permalink': permalink, 'post_title': post_title, 'url': url,
                'selftext': selftext, 'ban_note': ban_note, 'number_of_reports': number_of_reports,
                'location': 'modqueue'}

        if not post_queue_database.check_if_previously_queued(item, connection):
            post_queue_database.add_item_to_post_queue(item, connection)
            items.append(item)

    sorted_items = sorted(items, key=itemgetter('created_utc'))

    for item in sorted_items:
        print(item['location'] + ' - ' + str(len(item['selftext'])) + ' characters')
        # embeds.append(create_embed(item))

    connection.close()
    return items


def main():
    items = get_new_posts()
    embeds = post_queue_stream.get_stream_embeds(items)


if __name__ == '__main__':
    main()


