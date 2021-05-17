from spotify_worker import Spotify_Worker
from telebot import TeleBot, types
from scrapper import get_links
import pandas as pd
import pickle
from config import *


spotify_worker = Spotify_Worker()
bot = TeleBot(TOKEN)
data = pd.read_csv('data.csv')
model = pickle.load(open('model.pkl', 'rb'))


@bot.message_handler(commands=['start'])
def start_handler(message):
    markup = types.ReplyKeyboardMarkup(
        resize_keyboard=True, one_time_keyboard=True)
    item_playlist = types.KeyboardButton('За плейлістом')
    item_tracks = types.KeyboardButton('За треками')
    markup.add(item_playlist, item_tracks)

    bot.send_message(message.chat.id, GREETING_MESSAGE,
                     parse_mode='html')
    bot.send_message(
        message.chat.id, GREETING_QUESTION, reply_markup=markup)


@bot.message_handler(content_types=['text'])
def choice_handler(message):
    if message.text == 'За плейлістом':
        bot.send_message(message.from_user.id,
                         PLAYLIST_PROMPT)
        bot.register_next_step_handler(message, playlist_handler)
    elif message.text == 'За треками':
        bot.send_message(message.from_user.id,
                         TRACKS_PROMPT)
        bot.register_next_step_handler(message, tracks_handler)


def playlist_handler(message):
    if message.text == '/start':
        start_handler(message)
        return

    try:
        songs = spotify_worker.search_tracks_from_playlist(message.text)
        result = spotify_worker.recommend_songs(songs, data, model)
    except:
        bot.send_message(
            message.chat.id, PLAYLIST_ERROR)
        bot.register_next_step_handler(message, playlist_handler)
        return

    recommendation_sender(message, result)


def tracks_handler(message):
    # Split the songs
    if ';' in message.text:
        songs = message.text.split(';')
        songs_ed = [song.strip() for song in songs]
    else:
        songs_ed = [message.text.strip()]

    # Get a list of recommended songs
    result = spotify_worker.recommend_songs(songs_ed, data, model)

    recommendation_sender(message, result)


def recommendation_sender(message, result):
    # Build the markup for the user
    markup = types.InlineKeyboardMarkup(row_width=2)

    for result_item in result:
        song = result_item['name']
        artists = eval(result_item['artists'])

        artists_str = ', '.join(artists)
        track_str = f'{artists_str} - {song}'

        if len(track_str) > 64:
            continue
        try:
            callback_data = (result_item['id'], track_str)
            markup.add(types.InlineKeyboardButton(
                track_str, callback_data=result_item["id"]))
        except:
            continue

    bot.send_message(message.chat.id, RECOMMENDATIONS_MESSAGE,
                     reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        track_id = call.data

        track_info = data[data['id'] == track_id].iloc[0]

        artists_str = ', '.join(eval(track_info['artists']))
        track_str = f'{artists_str} - {track_info["name"]}'

        url = f'https://open.spotify.com/track/{track_id}'
        links = get_links(url)

        keyboard = types.InlineKeyboardMarkup()

        for link in links:
            keyboard.add(types.InlineKeyboardButton(
                text=link, url=links[link]))

        bot.send_message(call.message.chat.id, track_str,
                         reply_markup=keyboard)


bot.polling(none_stop=True)
