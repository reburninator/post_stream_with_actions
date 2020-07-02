approve = '👍'
remove = '👎'

def get_mod_action(emoji):
    switcher = {
        '👍': 'approve',
        '👎': 'remove'
    }

    return switcher.get(emoji, 'Invalid action')


def get_emoji(mod_action):
    switcher = {
        'approve': '👍',
        'remove': '👎'
    }

    return switcher.get(mod_action, 'Invalid action')
