from auth_data import login, password, bot_token
from datetime import datetime
import telebot
import vk_api
import requests
import json

vk_session = vk_api.VkApi(f'{login}', f'{password}')
vk_session.auth()

vk = vk_session.get_api()

def telegram_bot(bot_token):
    bot = telebot.TeleBot(bot_token)

    @bot.message_handler(commands=["start"])
    def start_message(message):
        bot.send_message(message.chat.id, "Привет! Пришли ID :)")

    @bot.message_handler(content_types=["text"])
    def send_text(message):
        if len(message.text) < 10 and message.text.isdigit():
            messageID = message.text
            try:
                getUsers = vk.users.get(user_id=f"{messageID}", fields='last_seen,followers_count,photo_200_orig',)[0]
                userID = getUsers['id']
                userPhoto = getUsers['photo_200_orig']
                fullname = getUsers['first_name'] + ' ' + getUsers['last_name']
                lastseen = datetime.utcfromtimestamp(getUsers['last_seen']['time'] + 10800).strftime('%Y-%m-%d %H:%M')

                GetFollowers = vk.users.getFollowers(user_id=f"{messageID}")
                followersCount = GetFollowers['count']
                followers = GetFollowers['items']
                LastFollower = vk.users.get(user_id=f"{followers[0]}", fields='id, first_name, last_name')[0]
                IDLastFollower = followers[0]
                fullnameLastFollower = LastFollower['first_name'] + ' ' + LastFollower['last_name']

                GetFriends = vk.friends.get(user_id=f"{messageID}")
                friendsCount = GetFriends['count']
                friends = GetFriends['items']
                LastFriend = vk.users.get(user_id=f"{friends[0]}", fields='id, first_name, last_name')[0]
                IDLastFriend = LastFriend['id']
                fullnameLF = LastFriend['first_name'] + ' ' + LastFriend['last_name']

                bot.send_message(message.chat.id, 
f"ID пользователя: {userID}\nИмя пользователя: {fullname}\nПоследний раз в сети: {lastseen}\n\nОбщее кол-во друзей: {friendsCount}\nОбщее кол-во подписчиков: {followersCount}\n\nПоследний друг: {fullnameLF}\nПоследний подписчик: {fullnameLastFollower}\n{userPhoto}"
                )       
            except Exception as ex: 
                bot.send_message(message.chat.id, "Что-то пошло не так!")
        else:
            bot.send_message(message.chat.id, "Невалидный ID!")
    bot.polling()

def main():
    telegram_bot(bot_token)

if __name__ == '__main__':
    main()
