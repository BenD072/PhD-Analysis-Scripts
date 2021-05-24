import time
from GUI_functions import update_text_output


def rate_limit_timer(window_name):
    for i in range(1, 16):
        update_text_output("You have encountered Twitter's rate limit. Waiting for {} minutes before "
                           "continuing".format(16-i), window_name.window2, window_name.text_box)
        time.sleep(60)


def set_column_heads(window_name):
    column_heads = []
    if window_name.get_author:
        column_heads.append('Author')
    else:
        pass
    if window_name.get_author_bio:
        column_heads.append('Author_Bio')
    else:
        pass
    if window_name.get_time_created:
        column_heads.append('Time_Created')
    else:
        pass
    if window_name.get_location:
        column_heads.append('Location')

    column_heads.append('TweetText')
    column_heads.append('RetweetedStatusYN')

    if window_name.get_follower_count:
        column_heads.append('Follower_Count')
    else:
        pass
    if window_name.get_favourite_count:
        column_heads.append('Favourite_Count')
    else:
        pass
    if window_name.get_retweet_count:
        column_heads.append('Retweet_Count')
    else:
        pass

    return column_heads
