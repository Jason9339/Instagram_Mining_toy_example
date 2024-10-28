from instagrapi import Client
import pandas as pd
import json

ACCOUNT_USERNAME = '--------'
ACCOUNT_PASSWORD = '--------'

cl = Client()
cl.load_settings('settings.json')
cl.login(ACCOUNT_USERNAME, ACCOUNT_PASSWORD)
cl.get_timeline_feed() # check session
print('Logged in as:', cl.user_id)

cl.delay_range = [1, 3]

# user_id = str(cl.user_id)
# 
# user_followers = cl.user_followers(user_id)
# with open('followers.json', 'w') as file:
#     json.dump(user_followers, file, indent=1)
# 
# user_following = cl.user_following(user_id)
# with open('following.json', 'w') as file:
#     json.dump(user_following, file, indent=1)

user_name = 'afuuuuuuuuuu'
user_id = cl.user_id_from_username(user_name)
# print('User info:')
# print(cl.user_info(user_id), end='\n\n')

print('User medias:')
medias = cl.user_medias(user_id)
print('Total:', len(medias))

# sort medias by likes
# medias.sort(key=lambda x: x.like_count, reverse=True)

data = pd.DataFrame([{
    'code': media.code,
    'url': f'https://www.instagram.com/p/{media.code}/',
    'media_type': media.media_type,
    'like_count': media.like_count,
    'comment_count': media.comment_count,
    'taken_at': media.taken_at,
    'type': media.media_type,
    'caption_text': media.caption_text
} for media in medias])
# for media in medias:
#     # print media url, likes, comments, shares
#     print(f'https://www.instagram.com/p/{media.code}/')
#     print('Type:', media.media_type, end=' ')
#     print('Likes:', media.like_count, end=' ')
#     print('Comments:', media.comment_count)
#     print('Date', media.taken_at)
#     print('Caption:', media.caption_text)
#     print()

data.to_csv(f'{user_name}.csv', index=False)
