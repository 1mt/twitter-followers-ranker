import tweepy

def setup_tweepy_api(consumer_key, consumer_secret, access_token, access_token_secret):
    """
    Setup the tweepy API with the provided credentials.
    """
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    return api

def lookup_user_list(follower_ids, api):
    """
    Gets user objects from a list of IDs.
    """
    full_users = []
    users_count = len(follower_ids)
    for i in range(0, users_count, 100):
        batch = follower_ids[i:i+100]
        full_users.extend(api.lookup_users(user_ids=batch))
    return full_users

def get_followers_info(target_screen_name, api):
    """
    Fetch follower info for the given target screen name.
    """
    screennames_and_count = []
    total_count = 0

    for page in tweepy.Cursor(api.followers_ids, screen_name=target_screen_name, count=200).pages():
        users = lookup_user_list(page, api)
        total_count += len(users)
        for user in users:
            screennames_and_count.append([user.screen_name, user.followers_count])
        print(f"{total_count} accounts processed")

    screennames_and_count.sort(key=lambda x: x[1], reverse=True)
    return screennames_and_count

if __name__ == "__main__":
    # NOTE: Replace "REDACTED" with your credentials.
    api_instance = setup_tweepy_api("REDACTED", "REDACTED", "REDACTED", "REDACTED")
    results = get_followers_info("TARGET_SCREEN_NAME_HERE", api_instance)
    print('\n'.join(['\t'.join(map(str, row)) for row in results]))
