import tkinter as tk
import tweepy
import pandas as pd
import time
from datetime import datetime, timedelta
from GUI_functions import update_text_output, build_new_window, run_commands
from twitter_functions import rate_limit_timer, set_column_heads
import os


class StartWindow:
    def __init__(self):
        self.consumer_key = ''
        self.consumer_key_secret = ''
        self.access_token = ''
        self.access_token_secret = ''

        self.passed_credentials = False

        self.window = tk.Tk()
        self.window.title("Login Details")
        self.window.geometry("500x500")
        self.window.resizable(0, 0)

        self.consKey_label = tk.Label(text="Enter Consumer Key")
        self.consKey_entry = tk.Entry(self.window)

        self.consSecret_label = tk.Label(text="Enter Consumer Secret")
        self.consSecret_entry = tk.Entry(self.window)

        self.accessToken_label = tk.Label(text="Enter Access Token")
        self.accessToken_entry = tk.Entry(self.window)

        self.accessSecret_label = tk.Label(text="Enter Access Token Secret")
        self.accessSecret_entry = tk.Entry(self.window)

        # GUI bits for selecting which twitter function to load
        self.twitter_function_label = tk.Label(text="Select function")

        self.twitter_function_variable = tk.IntVar()
        self.phrase_tweets_button = tk.Radiobutton(self.window, text="Get Tweets from a word/phrase",
                                                   variable=self.twitter_function_variable,
                                                   value=0, indicatoron=True, width=30)
        self.person_tweets_button = tk.Radiobutton(self.window, text="Get Tweets from a specific user",
                                                   variable=self.twitter_function_variable,
                                                   value=1, indicatoron=True, width=30)

        self.button = tk.Button(self.window, text="Submit", command=lambda: [self.store_login(),
                                                                             self.check_credentials(self.consumer_key,
                                                                                                    self.consumer_key_secret,
                                                                                                    self.access_token,
                                                                                                    self.access_token_secret),
                                                                             self.choose_window()])

        # Text box for updates
        self.text_box = tk.Text(self.window, width=25, height=4, wrap='word')
        self.text_box.grid(row=8, column=0, columnspan=4, rowspan=2)
        self.text_box.insert('0.0', "")
        self.text_box.config(state='disabled')

        # Pack GUI objects
        self.consKey_label.grid(row=0, column=0)
        self.consKey_entry.grid(row=0, column=1)
        self.consSecret_label.grid(row=1, column=0)
        self.consSecret_entry.grid(row=1, column=1)
        self.accessToken_label.grid(row=2, column=0)
        self.accessToken_entry.grid(row=2, column=1)
        self.accessSecret_label.grid(row=3, column=0)
        self.accessSecret_entry.grid(row=3, column=1)
        self.twitter_function_label.grid(row=5, column=0)
        self.phrase_tweets_button.grid(row=5, column=1)
        self.person_tweets_button.grid(row=6, column=1)
        self.button.grid(row=7, column=0)

    def store_login(self):
        self.consumer_key = self.consKey_entry.get().strip()
        self.consumer_key_secret = self.consSecret_entry.get().strip()
        self.access_token = self.accessToken_entry.get().strip()
        self.access_token_secret = self.accessSecret_entry.get().strip()
        return self.consumer_key, self.consumer_key_secret, self.access_token, self.access_token_secret

    def check_credentials(self, consumer_key, consumer_key_secret, access_token, access_token_secret):
        global api
        auth = tweepy.OAuthHandler(consumer_key, consumer_key_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth, wait_on_rate_limit=False, wait_on_rate_limit_notify=False)

        try:
            test = api.verify_credentials()
            if test == False:
                update_text_output("Error: The API credentials are incorrect or invalid", self.window, self.text_box)
                self.passed_credentials = False
            else:
                update_text_output("Credentials are good.", self.window, self.text_box)
                self.passed_credentials = True
        except tweepy.TweepError:
            update_text_output("Error: The API credentials are incorrect or invalid", self.window, self.text_box)
            self.passed_credentials = False

    def choose_window(self):
        global window2, window3
        if self.twitter_function_variable.get() == 0 and self.passed_credentials:
            window2 = build_new_window(PhraseWindow, self.window)
            return window2
        elif self.twitter_function_variable.get() == 1 and self.passed_credentials:
            window3 = build_new_window(PersonWindow, self.window)
            return window3
        else:
            pass


# Get Phrase Tweets Window Class
class PhraseWindow:
    def __init__(self, master):
        self.search_term = ''
        self.number_of_tweets = 100
        self.get_author = True
        self.get_author_bio = True
        self.get_time_created = True
        self.get_location = True
        self.get_follower_count = True
        self.get_retweet_count = True
        self.get_favourite_count = True
        self.seven_day_date = (datetime.today() - timedelta(days=7)).strftime('%Y-%m-%d')
        self.current_date = (datetime.today()).strftime('%Y-%m-%d')
        self.run_tweets = False

        self.entered_start_date = ''
        self.entered_end_date = ''

        self.window2 = tk.Toplevel(master)
        self.window2.geometry("800x500")
        self.window2.resizable(0, 0)
        self.window2.title('Enter Details')

        self.title_label = tk.Label(self.window2, text="Enter what information you would like to collect")
        self.author_label = tk.Label(self.window2, text="Author")
        self.authorBio_label = tk.Label(self.window2, text="Author Bio")
        self.timeCreated_label = tk.Label(self.window2, text="Time Created")
        self.location_label = tk.Label(self.window2, text="Location")
        self.followerCount_label = tk.Label(self.window2, text="Follower Count")
        self.favouriteCount_label = tk.Label(self.window2, text="Favourite Count")
        self.retweetCount_label = tk.Label(self.window2, text="Retweet Count")

        # On/Off Toggle switches for each piece of information
        self.switch_variable = tk.IntVar()  # Each on/off button has a control integer that manages on/off states
        self.author_off_button = tk.Radiobutton(self.window2, text="On", variable=self.switch_variable, value=0,
                                                indicatoron=True, width=8)
        self.author_on_button = tk.Radiobutton(self.window2, text="Off", variable=self.switch_variable, value=1,
                                               indicatoron=True, width=8)

        self.switch_variable1 = tk.IntVar()
        self.authorBio_off_button = tk.Radiobutton(self.window2, text="On", variable=self.switch_variable1, value=0,
                                                   indicatoron=True, width=8)
        self.authorBio_on_button = tk.Radiobutton(self.window2, text="Off", variable=self.switch_variable1, value=1,
                                                  indicatoron=True, width=8)

        self.switch_variable2 = tk.IntVar()
        self.timeCreated_off_button = tk.Radiobutton(self.window2, text="On", variable=self.switch_variable2, value=0,
                                                     indicatoron=True, width=8)
        self.timeCreated_on_button = tk.Radiobutton(self.window2, text="Off", variable=self.switch_variable2, value=1,
                                                    indicatoron=True, width=8)

        self.switch_variable3 = tk.IntVar()
        self.location_off_button = tk.Radiobutton(self.window2, text="On", variable=self.switch_variable3, value=0,
                                                  indicatoron=True, width=8)
        self.location_on_button = tk.Radiobutton(self.window2, text="Off", variable=self.switch_variable3, value=1,
                                                 indicatoron=True, width=8)

        self.switch_variable4 = tk.IntVar()
        self.followerCount_off_button = tk.Radiobutton(self.window2, text="On", variable=self.switch_variable4, value=0,
                                                       indicatoron=True, width=8)
        self.followerCount_on_button = tk.Radiobutton(self.window2, text="Off", variable=self.switch_variable4, value=1,
                                                      indicatoron=True, width=8)

        self.switch_variable5 = tk.IntVar()
        self.favouriteCount_off_button = tk.Radiobutton(self.window2, text="On", variable=self.switch_variable5,
                                                        value=0, indicatoron=True, width=8)
        self.favouriteCount_on_button = tk.Radiobutton(self.window2, text="Off", variable=self.switch_variable5,
                                                       value=1, indicatoron=True, width=8)

        self.switch_variable6 = tk.IntVar()
        self.retweetCount_off_button = tk.Radiobutton(self.window2, text="On", variable=self.switch_variable6, value=0,
                                                      indicatoron=True, width=8)
        self.retweetCount_on_button = tk.Radiobutton(self.window2, text="Off", variable=self.switch_variable6, value=1,
                                                     indicatoron=True, width=8)

        # Entry box for search term
        self.searchTerm_label = tk.Label(self.window2, text='Enter your search term')
        self.searchTerm_entry = tk.Entry(self.window2)

        # Entry box for start and end date
        # Start date
        self.start_date_label = tk.Label(self.window2, text='Enter your start date (must be within the last 7 days)')
        self.start_date_box = tk.Entry(self.window2)
        self.start_date_label.grid(row=9, column=0)
        self.start_date_box.grid(row=9, column=1)
        self.start_date_box.insert(0, self.seven_day_date)

        # End Date
        self.end_date_label = tk.Label(self.window2, text="Enter your end date (must be within the last 7 days)")
        self.end_date_box = tk.Entry(self.window2)
        self.end_date_label.grid(row=10, column=0)
        self.end_date_box.grid(row=10, column=1)
        self.end_date_box.insert(0, self.current_date)

        # Entry box for number of tweets to get
        self.number_of_tweets_label = tk.Label(self.window2, text="Enter the number of tweets you would like to collect")
        self.number_of_tweets_box = tk.Entry(self.window2)
        self.number_of_tweets_label.grid(row=11, column=0)
        self.number_of_tweets_box.grid(row=11, column=1)
        self.number_of_tweets_box.insert(0, 100)

        # Text box used to print status updates
        self.text_box = tk.Text(self.window2, width=25, height=4, wrap='word')
        self.text_box.grid(row=13, column=0, columnspan=4, rowspan=2)
        self.text_box.insert('0.0', "")
        self.text_box.config(state='disabled')

        # Submit button
        # When pressed, runs functions to check that all conditions are met (e.g. date requirements), checks which
        # data on/off toggles have been set, and then runs the command which gets the tweets
        self.submit_button = tk.Button(self.window2, text="Submit", command=lambda: [self.check_toggles(),
                                                                                     self.check_date(), self.get_phrase_entry(),
                                                                                     run_commands(window2, 'Phrase')])

        # Layout of all buttons and labels
        self.title_label.grid(row=0, column=1)
        self.author_label.grid(row=1, column=0)
        self.author_on_button.grid(row=1, column=1)
        self.author_off_button.grid(row=1, column=2)

        self.authorBio_label.grid(row=2, column=0)
        self.authorBio_on_button.grid(row=2, column=1)
        self.authorBio_off_button.grid(row=2, column=2)

        self.timeCreated_label.grid(row=3, column=0)
        self.timeCreated_on_button.grid(row=3, column=1)
        self.timeCreated_off_button.grid(row=3, column=2)

        self.location_label.grid(row=4, column=0)
        self.location_on_button.grid(row=4, column=1)
        self.location_off_button.grid(row=4, column=2)

        self.followerCount_label.grid(row=5, column=0)
        self.followerCount_on_button.grid(row=5, column=1)
        self.followerCount_off_button.grid(row=5, column=2)

        self.favouriteCount_label.grid(row=6, column=0)
        self.favouriteCount_on_button.grid(row=6, column=1)
        self.favouriteCount_off_button.grid(row=6, column=2)

        self.retweetCount_label.grid(row=7, column=0)
        self.retweetCount_on_button.grid(row=7, column=1)
        self.retweetCount_off_button.grid(row=7, column=2)

        self.searchTerm_label.grid(row=8, column=0)
        self.searchTerm_entry.grid(row=8, column=1)

        self.submit_button.grid(row=12, column=1)

    def get_phrase_entry(self):
        self.search_term = self.searchTerm_entry.get()
        try:
            self.number_of_tweets = int(self.number_of_tweets_box.get())
            self.run_tweets = True
        except ValueError:
            update_text_output("Error, you must enter a number", self.window2, self.text_box)
            self.run_tweets = False

    def get_phrase_tweets(self, get_author=True, get_author_bio=True, get_time_created=True, get_location=True,
                          get_follower_count=True, get_retweet_count=True, get_favourite_count=True,
                          search_term='search_term',
                          maxTweets=100, since='', until='',
                          lang='en', geocode=None):

        # Disable buttons
        self.submit_button["state"] = "disabled"

        # Parameters for tweets
        tweet_count = 0
        tweets_per_query = 100  # this is the max the API permits
        since_id = None
        max_id = -1
        tweets = []
        data = []

        while tweet_count < maxTweets:
            try:
                if max_id <= 0:
                    if not since_id:
                        new_tweets = api.search(q=search_term, count=tweets_per_query, tweet_mode='extended',
                                                since=since, until=until, lang=lang, geocode=geocode)
                    else:
                        new_tweets = api.search(q=search_term, count=tweets_per_query, tweet_mode='extended',
                                                since_id=since_id, since=since, until=until, lang=lang, geocode=geocode)
                else:
                    if not since_id:
                        new_tweets = api.search(q=search_term, count=tweets_per_query, tweet_mode='extended',
                                                max_id=str(max_id - 1), since=since, until=until, lang=lang,
                                                geocode=geocode)
                    else:
                        new_tweets = api.search(q=search_term, count=tweets_per_query, tweet_mode='extended',
                                                max_id=str(max_id - 1),
                                                since_id=since_id, since=since, until=until, lang=lang, geocode=geocode)
                tweets.extend(new_tweets)
                update_text_output("Getting {} of {} tweets".format(tweet_count, maxTweets), window2.window2,
                                   window2.text_box)
                if not new_tweets:
                    print("No more tweets found")
                    break
                tweet_count += len(new_tweets)
                max_id = new_tweets[-1].id

            except tweepy.RateLimitError:
                rate_limit_timer(window2)

            except tweepy.TweepError as e:
                # Just exit if any error
                update_text_output("An error has occurred. Please try again", window2.window2, window2.text_box)
                print("some error : " + str(e))
                break

        # Get selected information (based on toggles) for each tweet and place in a dataframe
        for tweet in tweets:
            data_package = []
            if get_author:
                author = tweet.user.screen_name
                data_package.append(author)
            else:
                pass
            if get_author_bio:
                bio = tweet.user.description
                data_package.append(bio)
            else:
                pass
            if get_time_created:
                created = tweet.created_at
                data_package.append(created)
            else:
                pass
            if get_location:
                location = tweet.user.location
                data_package.append(location)
            try:
                tweetText = tweet.retweeted_status.full_text
                retweet_status = 'Yes'
                data_package.append(tweetText)
                data_package.append(retweet_status)
            except AttributeError:  # Not a retweet
                tweetText = tweet.full_text
                retweet_status = 'No'
                data_package.append(tweetText)
                data_package.append(retweet_status)
            if get_follower_count:
                follower_count = tweet.user.followers_count
                data_package.append(follower_count)
            else:
                pass
            if get_favourite_count:
                favourite_count = tweet.favorite_count
                data_package.append(favourite_count)
            else:
                pass
            if get_retweet_count:
                retweet_count = tweet.retweet_count
                data_package.append(retweet_count)
            else:
                pass

            data.append(data_package)

        column_heads = set_column_heads(self)
        df = pd.DataFrame(data, columns=column_heads)

        try:
            path = os.path.expanduser('~/Desktop/')
            df.to_excel(os.path.join(path,r'Tweets Save File.xlsx'))
            update_text_output('Done - The file has been saved to your Desktop', window2.window2, window2.text_box)
        except:
            update_text_output("There has been an error, cannot find Desktop directory.", self.window2, self.text_box)

        # Re-enable button
        window2.submit_button["state"] = "normal"
        return df

    def check_toggles(self):
        if self.switch_variable.get() == 0:
            self.get_author = True
        else:
            self.get_author = False
        if self.switch_variable1.get() == 0:
            self.get_author_bio = True
        else:
            self.get_author_bio = False
        if self.switch_variable2.get() == 0:
            self.get_time_created = True
        else:
            self.get_time_created = False
        if self.switch_variable3.get() == 0:
            self.get_location = True
        else:
            self.get_location = False
        if self.switch_variable4.get() == 0:
            self.get_follower_count = True
        else:
            self.get_follower_count = False
        if self.switch_variable5.get() == 0:
            self.get_favourite_count = True
        else:
            self.get_favourite_count = False
        if self.switch_variable6.get() == 0:
            self.get_retweet_count = True
        else:
            self.get_retweet_count = False

    def check_date(self):
        self.entered_start_date = self.start_date_box.get()
        self.entered_end_date = self.end_date_box.get()
        try:
            if datetime.strptime(self.entered_start_date, '%Y-%m-%d') < datetime.today() - timedelta(days=8):
                update_text_output('Error: The start date must be within 7 days of the current date', window2.window2,
                                   window2.text_box)
                self.run_tweets = False
            elif datetime.strptime(self.entered_end_date, '%Y-%m-%d') < datetime.today() - timedelta(days=8):
                update_text_output("Error: The end date must be within 7 days of the current date", window2.window2,
                                   window2.text_box)
                self.run_tweets = False
            elif datetime.strptime(self.entered_start_date, '%Y-%m-%d') > datetime.today():
                update_text_output('Error: The start date cannot be a date in the future', window2.window2,
                                   window2.text_box)
                self.run_tweets = False
            elif datetime.strptime(self.entered_start_date, '%Y-%m-%d') == datetime.strptime(self.entered_end_date, '%Y-%m-%d'):
                update_text_output(
                    "Error: The start and end date cannot be the same. There must be at least a one day gap",
                    window2.window2, window2.text_box)
                self.run_tweets = False
            elif datetime.strptime(self.entered_start_date, '%Y-%m-%d') > datetime.strptime(self.entered_end_date, '%Y-%m-%d'):
                update_text_output("Error: The end date cannot be before the start date", window2.window2,
                                   window2.text_box)
                self.run_tweets = False
            else:
                self.run_tweets = True
        except ValueError:
            update_text_output('Incorrect Date Format: You must enter the date with the format yyyy-mm-dd',
                               window2.window2, window2.text_box)
            self.run_tweets = False


class PersonWindow:
    def __init__(self, master):
        self.user_handle_entry = ''
        self.number_of_tweets = 100
        self.get_author = True
        self.get_author_bio = True
        self.get_time_created = True
        self.get_location = True
        self.get_follower_count = True
        self.get_retweet_count = True
        self.get_favourite_count = True
        self.run_tweets = True

        self.window = tk.Toplevel(master)
        self.window.geometry("700x500")
        self.window.resizable(0, 0)
        self.window.title('Person Tweets: Enter Details')

        self.target_user_label = tk.Label(self.window, text="Enter the twitter handle of the user you want to collect "
                                                            "tweets from")

        self.target_user_entrybox = tk.Entry(self.window)
        self.target_user_label.grid(row=0, column=0)
        self.target_user_entrybox.grid(row=0, column=1)

        self.authorBio_label = tk.Label(self.window, text="Author Bio")
        self.timeCreated_label = tk.Label(self.window, text="Time Created")
        self.location_label = tk.Label(self.window, text="Location")
        self.followerCount_label = tk.Label(self.window, text="Follower Count")
        self.favouriteCount_label = tk.Label(self.window, text="Favourite Count")
        self.retweetCount_label = tk.Label(self.window, text="Retweet Count")

        # On/Off Toggle switches for each piece of information
        self.switch_variable1 = tk.IntVar()
        self.authorBio_off_button = tk.Radiobutton(self.window, text="On", variable=self.switch_variable1, value=0,
                                                   indicatoron=True, width=8)
        self.authorBio_on_button = tk.Radiobutton(self.window, text="Off", variable=self.switch_variable1, value=1,
                                                  indicatoron=True, width=8)

        self.switch_variable2 = tk.IntVar()
        self.timeCreated_off_button = tk.Radiobutton(self.window, text="On", variable=self.switch_variable2, value=0,
                                                     indicatoron=True, width=8)
        self.timeCreated_on_button = tk.Radiobutton(self.window, text="Off", variable=self.switch_variable2, value=1,
                                                    indicatoron=True, width=8)

        self.switch_variable3 = tk.IntVar()
        self.location_off_button = tk.Radiobutton(self.window, text="On", variable=self.switch_variable3, value=0,
                                                  indicatoron=True, width=8)
        self.location_on_button = tk.Radiobutton(self.window, text="Off", variable=self.switch_variable3, value=1,
                                                 indicatoron=True, width=8)

        self.switch_variable4 = tk.IntVar()
        self.followerCount_off_button = tk.Radiobutton(self.window, text="On", variable=self.switch_variable4, value=0,
                                                       indicatoron=True, width=8)
        self.followerCount_on_button = tk.Radiobutton(self.window, text="Off", variable=self.switch_variable4, value=1,
                                                      indicatoron=True, width=8)

        self.switch_variable5 = tk.IntVar()
        self.favouriteCount_off_button = tk.Radiobutton(self.window, text="On", variable=self.switch_variable5,
                                                        value=0, indicatoron=True, width=8)
        self.favouriteCount_on_button = tk.Radiobutton(self.window, text="Off", variable=self.switch_variable5,
                                                       value=1, indicatoron=True, width=8)

        self.switch_variable6 = tk.IntVar()
        self.retweetCount_off_button = tk.Radiobutton(self.window, text="On", variable=self.switch_variable6, value=0,
                                                      indicatoron=True, width=8)
        self.retweetCount_on_button = tk.Radiobutton(self.window, text="Off", variable=self.switch_variable6, value=1,
                                                     indicatoron=True, width=8)

        # Entry box for number of tweets to get
        self.number_of_tweets_label = tk.Label(self.window, text="Enter the number of tweets you would like to collect "
                                                                 "(max 3000)")
        self.number_of_tweets_box = tk.Entry(self.window)
        self.number_of_tweets_label.grid(row=2, column=0)
        self.number_of_tweets_box.grid(row=2, column=1)
        self.number_of_tweets_box.insert(0, 100)

        # Text box used to print status updates
        self.text_box = tk.Text(self.window, width=25, height=10, wrap='word')
        self.text_box.grid(row=10, column=0, columnspan=4, rowspan=2)
        self.text_box.insert('0.0', "")
        self.text_box.config(state='disabled')

        # Submit button
        # When pressed, runs functions to check that all conditions are met (e.g. date requirements), checks which
        # data on/off toggles have been set, and then runs the command which gets the tweets
        self.submit_button = tk.Button(self.window, text="Submit", command=lambda: [self.check_toggles(),
                                                                                    self.get_person_entry(),
                                                                                    self.check_max_tweet_value(
                                                                                        self.number_of_tweets),
                                                                                    run_commands(window3, 'Person')])

        # Layout of all buttons and labels
        self.authorBio_label.grid(row=3, column=0)
        self.authorBio_on_button.grid(row=3, column=1)
        self.authorBio_off_button.grid(row=3, column=2)

        self.timeCreated_label.grid(row=4, column=0)
        self.timeCreated_on_button.grid(row=4, column=1)
        self.timeCreated_off_button.grid(row=4, column=2)

        self.location_label.grid(row=5, column=0)
        self.location_on_button.grid(row=5, column=1)
        self.location_off_button.grid(row=5, column=2)

        self.followerCount_label.grid(row=6, column=0)
        self.followerCount_on_button.grid(row=6, column=1)
        self.followerCount_off_button.grid(row=6, column=2)

        self.favouriteCount_label.grid(row=7, column=0)
        self.favouriteCount_on_button.grid(row=7, column=1)
        self.favouriteCount_off_button.grid(row=7, column=2)

        self.retweetCount_label.grid(row=8, column=0)
        self.retweetCount_on_button.grid(row=8, column=1)
        self.retweetCount_off_button.grid(row=8, column=2)

        self.submit_button.grid(row=9, column=1)

    def get_person_entry(self):
        self.user_handle_entry = self.target_user_entrybox.get()
        try:
            self.number_of_tweets = int(self.number_of_tweets_box.get())
            self.run_tweets = True

        except ValueError:
            update_text_output("Error you must enter a number", self.window, self.text_box)
            self.run_tweets = False


    def get_person_tweets(self, user_handle="a", number_of_tweets=100, get_author_bio=True, get_time_created=True,
                          get_location=True, get_follower_count=True, get_retweet_count=True, get_favourite_count=True):
        temp_tweet_holder = []  # Temporary list to hold tweets scraped from tweepy.cursor each loop
        tweets = []  # Main list holder for all the tweets
        data = []  # List for data frame data
        tweet_count = 0  # Starting tweet count


        # Call first tweepy.Cursor call to get initial selection of tweets (N= 100)
        try:
            new_tweets = tweepy.Cursor(api.user_timeline, screen_name=user_handle, count=100, tweet_mode='extended').items(100)

            # Cursor returns a iterrator object - need to loop through to place each tweet/status object into the temporary list
            for tweet in new_tweets:
                temp_tweet_holder.append(tweet)

            # Increase tweet count and add new tweets to main list
            tweet_count += len(temp_tweet_holder)
            tweets.extend(temp_tweet_holder)

            # Save the id of the tweet before last
            last_tweet_id = tweets[-1].id - 1
        except tweepy.TweepError:
            update_text_output("Sorry, that user name does not exist. Please try another", self.window, self.text_box)
            return

        if user_handle == 'Ben_B_Davies_':
            self.easter_egg()
            return

        elif user_handle == "" or user_handle == " ":
            return

        else:  # If requested account is not Trump's
            try:
                while tweet_count < number_of_tweets:
                    temp_tweet_holder = []
                    # all requests after the first use the max_id parameter to get older tweets and prevent duplicates
                    new_tweets = tweepy.Cursor(api.user_timeline, screen_name=user_handle, count=100,
                                               max_id=last_tweet_id, tweet_mode='extended').items(100)
                    for tweet in new_tweets:
                        temp_tweet_holder.append(tweet)
                    if len(temp_tweet_holder) == 0:  # If no new tweets collected (i.e. got to end of tweets), exit loop
                        update_text_output("No more tweets found", self.window, self.text_box)
                        break

                    last_tweet_id = temp_tweet_holder[-1].id - 1  # Update last tweet id
                    tweet_count += len(temp_tweet_holder)
                    tweets.extend(temp_tweet_holder)
                    update_text_output("Getting {} of {}".format(tweet_count, number_of_tweets), self.window,
                                       self.text_box)

            except tweepy.RateLimitError:
                rate_limit_timer(self)

        # Go through list of tweets and create dataframe using toggles (e.g. if user bios is asked for, then append user
        # bio to the dataframe package
        for tweet in tweets:
            data_package = []
            author = tweet.user.screen_name
            data_package.append(author)

            if get_author_bio:
                bio = tweet.user.description
                data_package.append(bio)
            else:
                pass
            if get_time_created:
                created = tweet.created_at
                data_package.append(created)
            else:
                pass
            if get_location:
                location = tweet.user.location
                data_package.append(location)
            try:
                tweetText = tweet.retweeted_status.full_text
                retweet_status = 'Yes'
                data_package.append(tweetText)
                data_package.append(retweet_status)
            except AttributeError:  # Not a retweet
                tweetText = tweet.full_text
                retweet_status = 'No'
                data_package.append(tweetText)
                data_package.append(retweet_status)
            if get_follower_count:
                follower_count = tweet.user.followers_count
                data_package.append(follower_count)
            else:
                pass
            if get_favourite_count:
                favourite_count = tweet.favorite_count
                data_package.append(favourite_count)
            else:
                pass
            if get_retweet_count:
                retweet_count = tweet.retweet_count
                data_package.append(retweet_count)
            else:
                pass

            data.append(data_package)

        column_heads = set_column_heads(self)
        df = pd.DataFrame(data, columns=column_heads)

        try:
            path = os.path.expanduser('~/Desktop/')
            df.to_excel(os.path.join(path, r'Tweets Save File.xlsx'))
            update_text_output('Done - The file has been saved to your Desktop', self.window, self.text_box)
        except Exception as e:
            print(e)
            update_text_output("There has been an error: Cannot find Desktop directory", self.window, self.text_box)


        # Re-enable button
        self.submit_button["state"] = "normal"
        return df

    def check_toggles(self):
        if self.switch_variable1.get() == 0:
            self.get_author_bio = True
        else:
            self.get_author_bio = False
        if self.switch_variable2.get() == 0:
            self.get_time_created = True
        else:
            self.get_time_created = False
        if self.switch_variable3.get() == 0:
            self.get_location = True
        else:
            self.get_location = False
        if self.switch_variable4.get() == 0:
            self.get_follower_count = True
        else:
            self.get_follower_count = False
        if self.switch_variable5.get() == 0:
            self.get_favourite_count = True
        else:
            self.get_favourite_count = False
        if self.switch_variable6.get() == 0:
            self.get_retweet_count = True
        else:
            self.get_retweet_count = False

    def check_max_tweet_value(self, number_of_tweets):
        if self.run_tweets:  # If run tweets is true (i.e. has already passed the int/strign check, then next check if the value is higher than 3000
            if number_of_tweets > 3000:
                update_text_output("Error, no more than 3000 tweets can be returned from a user. Please enter a number "
                                "lower than 3000.", self.window, self.text_box)
                self.run_tweets = False
            else:
                self.run_tweets = True
        else:  # If run tweets is false, then just skip this block
            pass

    def easter_egg(self):
        update_text_output("Ah, it looks like you're trying to scrape my own twitter profile", self.window,
                           self.text_box)
        time.sleep(5)
        update_text_output("Whilst I very much appreciate your interest in my boring tweets, did you ever consider that"
                           " maybe I don't want you looking at my tweets?", self.window, self.text_box)
        time.sleep(8)
        update_text_output("You see, twitter research is a bit of a grey area when it comes to ethics and consent",
                           self.window, self.text_box)
        time.sleep(5)
        update_text_output("People tweet their views and opinions out into the world and, under twitter's own terms and"
                           " conditions, anyone is then able to view and save those tweets", self.window, self.text_box)
        time.sleep(8)
        update_text_output("But when you wrote that tweet and expressed that opinion, maybe you didn't intend"
                           " for some random researcher to find and save it 2 years down the line", self.window,
                           self.text_box)
        time.sleep(8)
        update_text_output("Maybe you don't even hold the same opinion that you did when you posted that tweet 2 years "
                           "ago?",
                           self.window, self.text_box)
        time.sleep(6)
        update_text_output("Maybe it was an embarrassing photo of you that you thought would be funny to post back then"
                           " but that you now realise was a horrible decision to make", self.window, self.text_box)
        time.sleep(8)
        update_text_output("And that's the thing with the internet. Whatever happens there stays forever.",
                           self.window, self.text_box)
        time.sleep(6)
        update_text_output("So the moral of the story is, think twice before you post something on the internet. "
                           "You never know, some researcher who you don't even know might be using that tweet to build "
                           "their thesis", self.window, self.text_box)
        time.sleep(8)
        update_text_output("Thank you for listening to my TED talk", self.window, self.text_box)
        time.sleep(6)

