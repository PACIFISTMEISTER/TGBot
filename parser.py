import time

import vk
import json

from database import CheckLastUpdate, UpdateTime
import os
token = os.getenv('VK_TOKEN')

def ParsePublic(user_id, Publics:list,type):
    """парсинг пабликов"""
    lastSeen = CheckLastUpdate(user_id,type)
    unix = 1
    if lastSeen is not None:
        unix = time.mktime(lastSeen.timetuple())
    try:
        api = vk.API(access_token=token, v='5.131')
    except:
        print('too many requests')
    urls = []
    for public in Publics:

        posts = json.loads(json.dumps(api.wall.get(access_token=token, domain=public, count=10)))

        for post in posts['items']:
            if unix and post['date'] > unix:
                for attachment in post['attachments']:
                    if attachment['type'] == 'photo':
                        urls.extend([photo['url'] for photo in attachment['photo']['sizes'] if photo['type'] == 'y'])

            else:
                break
    UpdateTime(user_id,type)

    return urls
