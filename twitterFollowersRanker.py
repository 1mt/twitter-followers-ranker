import time
import tweepy

# tweepy API config
auth = tweepy.OAuthHandler("REDACTED", "REDACTED")
auth.set_access_token("REDACTED", "REDACTED")
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
# list of user objects
users=[]
# 2D list of screenname and follower count respectivly
screennames_and_count=[]
total_count=0

# Gets user objects from list of ids
def lookup_user_list(followers_id, api):
    full_users = []
    users_count = len(followers_id)
    for i in range(int((users_count / 100))):
        full_users.extend(api.lookup_users(user_ids=followers_id[i*100:min((i+1)*100, users_count)]))
    return full_users, users_count

# gets a list of follower ids      
for page in tweepy.Cursor(api.followers_ids, screen_name="TARGET_SCREEN_NAME_HERE", count=200).pages():
    temp_users, temp_count = lookup_user_list(page, api)
    total_count += temp_count
    users.extend(temp_users)
    print(str(total_count) + " accounts processed")
    
for user in users:
    screennames_and_count.append([user.screen_name, user.followers_count])
    
# orders list by follower account
screennames_and_count = sorted(screennames_and_count,key=lambda l:l[1], reverse=True)
# prints as a table
print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in screennames_and_count]))
