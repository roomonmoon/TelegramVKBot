from auth_data import TOKEN, BOT_TOKEN, user_id
from datetime import datetime
import telebot
import requests
import json
import time

def telegram_bot(BOT_TOKEN):
    bot = telebot.TeleBot(BOT_TOKEN)

    @bot.message_handler(commands=["start"])
    def start_message(message):
        bot.send_message(message.chat.id, "Привет! Если хочешь видеть информацию, просто напиши мне что-нибудь :)")

    @bot.message_handler(content_types=["text"])
    def send_text(message):
        if  len(message.text) < 10 and message.text.isdigit():
            try: 
                GetUsers = f'https://api.vk.com/method/users.get?user_id={message.text}&fields=last_seen,followers_count&access_token={TOKEN}&v=5.131'
                reqGetUsers = requests.get(GetUsers)
                srcGetUsers = reqGetUsers.json()
                dataGetUsers = srcGetUsers["response"][0]
                ID = dataGetUsers['id']
                fullname = dataGetUsers['first_name'] + ' ' + dataGetUsers['last_name']
                lastseen = datetime.utcfromtimestamp(dataGetUsers['last_seen']['time'] + 10800).strftime('%Y-%m-%d %H:%M')

                GetFollowers = f'https://api.vk.com/method/users.getFollowers?user_id={message.text}&access_token={TOKEN}&v=5.131'
                reqGetFollowers = requests.get(GetFollowers)
                srcGetFollowers = reqGetFollowers.json()
                dataGetFollowers = srcGetFollowers["response"]
                followersCount = dataGetFollowers['count']
                followers = dataGetFollowers['items']
                LastFollower = f'https://api.vk.com/method/users.get?user_id={followers[0]}&fields=last_seen,followers_count&access_token={TOKEN}&v=5.131'
                requestForLastFollower = requests.get(LastFollower)
                responseForLastFollower = requestForLastFollower.json()
                dataForLastFollower = responseForLastFollower['response'][0]
                fullnameLastFollower = dataForLastFollower['first_name'] + ' ' + dataForLastFollower['last_name']

                GetFriends = f'https://api.vk.com/method/friends.get?user_id={message.text}&access_token={TOKEN}&v=5.131'
                reqGetFriends = requests.get(GetFriends)
                srcGetFriends = reqGetFriends.json()
                dataGetFriends = srcGetFriends['response']
                friendsCount = dataGetFriends['count']
                friends = dataGetFriends['items']
                LastFriend = f'https://api.vk.com/method/users.get?user_id={friends[0]}&fields=last_seen,followers_count&access_token={TOKEN}&v=5.131'
                requestForLF = requests.get(LastFriend)
                responseForLF = requestForLF.json()
                dataForLF = responseForLF['response'][0]
                fullnameLF = dataForLF['first_name'] + ' ' + dataForLF['last_name']

                bot.send_message(message.chat.id, f"Имя пользователя: {fullname}\nID: {ID}\nПоследний раз был в сети: {lastseen}\nОбщее кол-во друзей: {friendsCount}\nПоследний друг: {fullnameLF}\nОбщее кол-во подписчиков: {followersCount}\nПоследний подписчик: {fullnameLastFollower}\n\nДанные на {datetime.now().strftime('%Y-%m-%d %H:%M')}")
            except Exception as ex:
                bot.send_message(message.chat.id, "Что-то пошло не так!")
        else:
           bot.send_message(message.chat.id, "Неправильный ID!")
    bot.polling()
def main():
    telegram_bot(BOT_TOKEN)

if __name__ == '__main__':
    main()