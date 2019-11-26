import os
from instabot import Bot
from dotenv import load_dotenv
import re
import argparse


def get_usernames_from_comment(comment):
    pattern = re.compile(
        r'(?:@)([A-Za-z0-9_]'
        r'(?:(?:[A-Za-z0-9_]|(?:\.(?!\.))){0,28}(?:[A-Za-z0-9_]))?)')
    return pattern.findall(comment)


def is_user_exists(bot, username):
    return bot.get_user_id_from_username(username) is not None


def is_user_tag_friends(bot, comment):
    text_comment = comment['text']
    tagged_friends = get_usernames_from_comment(text_comment)

    for friend in tagged_friends:
        if is_user_exists(bot, friend):
            return True
    return False


def is_users_followed(comment, followed_users):
    followed_user_id = str(comment['user_id'])
    return followed_user_id in followed_users


def is_user_liked(comment):
    liked = 'comment_like_count'
    return liked in comment and comment[liked] > 0


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
    bot.login(username=login, password=password, force=True)

    media_id = bot.get_media_id_from_link(instagram_url)
    media_owner_id = bot.get_media_owner(media=media_id)
    media_owner = bot.get_username_from_user_id(media_owner_id)
    author_followers = bot.get_user_followers(media_owner)
    comments = bot.get_media_comments_all(media_id=media_id)

    finalists = []

    for comment in comments:
        user_followed = is_users_followed(comment, author_followers)
        user_liked = is_user_liked(comment)

        if not (user_followed and user_liked):
            continue

        if not is_user_tag_friends(bot, comment):
            continue

        username = comment['user']['username']
        finalists.append(username)

    winners = set(finalists)
    bot.logout()
    print(winners)


if __name__ == '__main__':
    main()
