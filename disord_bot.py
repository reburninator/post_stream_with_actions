import config
import action_helper
import mod_actions
import post_queue_database
import post_queue_inbound
import post_queue_stream
import discord
from discord.ext import commands, tasks

client = commands.Bot(command_prefix='.')


@client.event
async def on_ready():
    process_new_posts.start()
    print('Ready')


@tasks.loop(seconds=180)
async def process_new_posts():
    print('Starting new post loop')

    channel = client.get_channel(config.post_channel)

    items = post_queue_inbound.get_new_posts()
    post_embeds = post_queue_stream.get_stream_embeds(items)

    for post_embed in post_embeds:
        try:
            message = await channel.send(embed=post_embed)
            await message.add_reaction(action_helper.approve)
            await message.add_reaction(action_helper.remove)

            permalink = post_embed.url
            message_id = message.id
            post_queue_database.update_post_with_message_id(permalink, message_id)
        except Exception as error:
            print(error)

    print('Ending new post loop.\n')


@client.command()
async def clear(ctx, amount=2):
    post_channel = client.get_channel(config.post_channel)
    if post_channel.id == ctx.channel.id:
        print('Purging up to ' + str(amount) + ' messages')
        await ctx.channel.purge(limit=amount)
    else:
        await ctx.send("I\'m not allowed to do that here.")


@client.event
async def on_raw_reaction_add(payload):
    channel_id = payload.channel_id

    if channel_id != config.post_channel:
        return

    message_id = payload.message_id
    user_id = payload.user_id
    user = client.get_user(user_id)
    emoji = payload.emoji.name

    if config.discord['botname'] != user.name:
        print(user.name + ' - ' + str(message_id))
        channel = client.get_channel(channel_id)

        if channel_id == config.post_channel:
            try:
                message = await channel.fetch_message(message_id)
                embeds = message.embeds

                if len(embeds) > 0:
                    action = action_helper.get_mod_action(emoji)
                    print(action)
                    if action != 'Invalid action':
                        mod_actions.process_mod_action(channel_id, message_id, user.name, action)
                        await message.delete()
                else:
                    print('No embeds found to process')
            except discord.NotFound:
                print('Message not found')


client.run(config.discord['token'])

