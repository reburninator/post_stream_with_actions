import config
import post_queue_database
import praw
import discord
from datetime import datetime
from operator import itemgetter


reddit = praw.Reddit(client_id=config.redditapp['client_id'],
                     client_secret=config.redditapp['client_secret'],
                     password=config.redditapp['password'],
                     user_agent=config.redditapp['user_agent'],
                     username=config.redditapp['user_id'])


def get_stream_embeds(items):
    embeds = []

    for item in items:
        embeds.append(create_embed(item))

    return embeds


def create_embed(item):
    posted_date = datetime.utcfromtimestamp(item['created_utc']).strftime('%Y-%m-%d %H:%M:%S')
    color = discord.Colour.gold()
    title = ''

    selftext = item['selftext']
    if len(selftext) == 0:
        selftext = "No post body found."

    selftext = 'Post body:\n\n' + selftext

    if item['username'] == '':
        title = 'Post from deleted user'
    else:
        title = 'Post from u/' + item['username']

    field_description = selftext
    number_of_reports = item['number_of_reports']

    if number_of_reports > 0:
        color = discord.Colour.blue()
        title = 'Reported post from u/' + item['username']

    if item['ban_note'] =='spam':
        color = discord.Colour.red()
        title = 'Spam post from u/' + item['username']
        number_of_reports = 0

    if item['ban_note'] == 'remove not spam':
        color = discord.Colour.orange()
        title = 'Filtered post from u/' + item['username']
        number_of_reports = 0

    discord_embed = discord.Embed(
        title=title,
        description=field_description,
        colour=color
    )

    discord_embed.url = item['permalink']

    if number_of_reports > 0:
        discord_embed.add_field(
            name='Number of reports',
            value=str(number_of_reports),
            inline=False
        )

    discord_embed.add_field(
        name='Post title',
        value=item['post_title'],
        inline=False
    )

    return discord_embed
