import os
from instabot import Bot
from dotenv import load_dotenv
import re
import argparse


def get_username_and_id(comment):
    user_id = comment['user_id']
    username = comment['user']['username']
    return user_id, username


def get_users_who_tag_friends(bot, comments):
    marked_friends = []
    for comment in comments:
        text = comment['text']
        friends = get_usernames_from_comment(text)
        for friend in friends:
            if is_user_exists(bot, friend):
                marked_friends.append(get_username_and_id(comment))
                break

    return marked_friends


def get_users_liked_post(comments):
    liked_comments = []
    for comment in comments:
        if 'comment_like_count' in comment:
            liked = comment['comment_like_count']
            if liked > 0:
                liked_comments.append(get_username_and_id(comment))

    return liked_comments


def get_followed_users(bot, comments, media_id):
    media_owner_id = bot.get_media_owner(media=media_id)
    media_owner = bot.get_username_from_user_id(media_owner_id)
    author_followers = bot.get_user_followers(media_owner)

    followed_users = []
    for comment in comments:
        user_id = str(comment['user_id'])
        if user_id in author_followers:
            followed_users.append(get_username_and_id(comment))

    return followed_users


def get_usernames_from_comment(comment):
    pattern = re.compile(
        r'(?:@)([A-Za-z0-9_]'
        r'(?:(?:[A-Za-z0-9_]|(?:\.(?!\.))){0,28}(?:[A-Za-z0-9_]))?)')
    return pattern.findall(comment)


def is_user_exists(bot, username):
    result = bot.get_user_id_from_username(username)
    if result:
        return True
    return False


def get_action_winners(bot, url):
    media_id = bot.get_media_id_from_link(url)
    comments = bot.get_media_comments_all(media_id=media_id)

    users_liked_post = set(get_users_liked_post(comments))
    users_who_tag_friends = set(get_users_who_tag_friends(bot, comments))
    followed_users = set(get_followed_users(bot, comments,  media_id))

    winners = users_liked_post.intersection(followed_users). \
        intersection(users_who_tag_friends)
    winners = [winner[1] for winner in winners]

    return winners


def main():
    load_dotenv()

    parser = argparse.ArgumentParser(
        description='Программа для конкурсов в Instagram'
    )
    parser.add_argument("url", help="Адрес ссылки (URL) на акцию")
    args = parser.parse_args()
    instagram_url = args.url

    login = os.getenv('INSTAGRAM_LOGIN')
    password = os.getenv('INSTAGRAM_PASSWORD')
    instagram_dir = os.getenv('INSTAGRAM_DIR')

    if not os.path.exists(instagram_dir):
        os.makedirs(instagram_dir)

    bot = Bot(base_path=instagram_dir)
    bot.login(username=login, password=password)

    action_winners = get_action_winners(bot=bot, url=instagram_url)

    bot.logout()

    print(action_winners)


if __name__ == '__main__':
    main()
