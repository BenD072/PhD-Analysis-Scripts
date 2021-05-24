import threading
import tkinter as tk


def build_new_window(window_type, master_window):
    new_window = window_type(master_window)
    return new_window


def update_text_output(text, window_to_update, text_box_name):
    text_box_name.config(state='normal')
    text_box_name.delete('0.0', tk.END)
    text_box_name.insert('0.0', text)
    text_box_name.config(state='disabled')
    window_to_update.update()


def run_commands(window_to_run, flag):
    window_to_run.submit_button["state"] = "disabled"
    if window_to_run.run_tweets and flag == 'Phrase':
        thread = threading.Thread(target=window_to_run.get_phrase_tweets, args=(window_to_run.get_author,
                                                                                window_to_run.get_author_bio,
                                                                                window_to_run.get_time_created,
                                                                                window_to_run.get_location,
                                                                                window_to_run.get_follower_count,
                                                                                window_to_run.get_retweet_count,
                                                                                window_to_run.get_favourite_count,
                                                                                window_to_run.search_term,
                                                                                window_to_run.number_of_tweets,
                                                                                window_to_run.entered_start_date,
                                                                                window_to_run.entered_end_date, 'en',
                                                                                None))
        thread.start()
    elif window_to_run.run_tweets and flag == 'Person':
        thread = threading.Thread(target=window_to_run.get_person_tweets, args=(window_to_run.user_handle_entry,
                                                                                window_to_run.number_of_tweets,
                                                                                window_to_run.get_author_bio,
                                                                                window_to_run.get_time_created,
                                                                                window_to_run.get_location,
                                                                                window_to_run.get_follower_count,
                                                                                window_to_run.get_retweet_count,
                                                                                window_to_run.get_favourite_count))
        thread.start()
    else:
        pass

    window_to_run.submit_button["state"] = "normal"
