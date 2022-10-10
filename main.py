# pip install pyTelegramBotAPI
import telebot
import config
import requests
import server
import sqlite3

# requirements.txt

# pip freeze в терминал и копировате в файл

# connect = sqlite3.connect('subsc.db', check_same_thread=False)
# cursor = connect.cursor()
#
# cursor.execute("""CREATE TABLE IF NOT EXISTS "users" (
# 	"id"	INTEGER NOT NULL
# );""")
# connect.commit()
#
# cursor.execute("""CREATE TABLE IF NOT EXISTS "subscribes" (
# 	"user_id"	INTEGER NOT NULL,
# 	"category_id"	INTEGER NOT NULL,
# 	PRIMARY KEY("user_id","category_id")
# );""")
# connect.commit()
#
# cursor.execute("""CREATE TABLE IF NOT EXISTS "categories" (
# 	"id"	INTEGER NOT NULL,
# 	"name"	INTEGER NOT NULL UNIQUE,
# 	PRIMARY KEY("id" AUTOINCREMENT)
# );""")
# connect.commit()

arrCateg = ["business", "entertainment", "general", "health", "science", "sports", "technology"]

bot = telebot.TeleBot(config.bot_token)
a = requests.get(
    "https://newsapi.org/v2/top-headlines?apiKey=589f962b1856423b9c7467a2a6497704&country=ru&category=sports&pageSize=5")

server.fillCateg(arrCateg)

i = 0
while i < (len(arrCateg)):
    #     res = cursor.execute("""SELECT categories.name FROM categories WHERE name=:name""",
    #                          {"name": arrCateg[i]}).fetchone()
    #     if res == None:
    #         cursor.execute("""INSERT INTO categories (name) VALUES (:name)""", {"name": arrCateg[i]})
    #         connect.commit()

    # print(arrCateg[i])
    @bot.message_handler(commands=[arrCateg[i]])
    def subUs(message):
        server.addUser(message.from_user.id)
        id = arrCateg.index(message.text.replace('/', '', 1)) + 1
        print("id", i)
        if server.subUser(message, id):
            bot.send_message(message.from_user.id, "вы подписались")
        else:
            bot.send_message(message.from_user.id, "вы уже подписаны")


    @bot.message_handler(commands=["UN_" + arrCateg[i]])
    def unsubUs(message):
        server.addUser(message.from_user.id)
        id = arrCateg.index(message.text.replace('/UN_', '', 1)) + 1
        print("id unsub", id)
        # bot.send_message(message.from_user.id, id)
        if server.unsubUser(message, id):
            bot.send_message(message.from_user.id, "вы отписались")
        else:
            bot.send_message(message.from_user.id, "вы не были подписаны")


    # print(i)
    @bot.message_handler(commands=["news_" + arrCateg[i]])
    def showNews(message):
        server.addUser(message.from_user.id)
        id = arrCateg.index(message.text.replace('/news_', '', 1))
        print("show",arrCateg.index(message.text.replace('/news_', '', 1))+1)
        print("arr", arrCateg[id])

        # res = cursor.execute("""SELECT user_id, category_id FROM subscribes WHERE user_id=:user_id AND category_id=:cat_id""",
        #                     {"user_id": message.from_user.id, "cat_id": id+1}).fetchone()
        res = server.checkSub(message, id)
        print("res", res)
        if res != None:
            news = getNews(arrCateg[id])
            for j in news.json()['articles']:
                # print([j['title'] + j['url']])
                #     bot.send_message(message.from_user.id, [i['title'] + i['url']])
                bot.send_message(message.from_user.id, [j['title'] + "\n" + j['url']])
        else:
            bot.send_message(message.from_user.id, "вы не подписаны на эту категорию")
            # j+=1


    i += 1


def getNews(categ):
    return requests.get(
        f"https://newsapi.org/v2/top-headlines?apiKey={config.api_Key}&country=ru&category={categ}&pageSize=3")


# async def on_startup():
#     user_should_be_notified = 5263766165
#     await bot.send_message(user_should_be_notified, 'Бот запущен')
# if __name__ == '__main__':
#     executor.start(dp, on_startup())
#     executor.start_polling(dp, skip_updates=True)


# business entertainment general health science sports technology


# def addUser(id):
#     result = cursor.execute("""SELECT users.id FROM users WHERE id=:id""", {"id": id}).fetchone()
#     if result == None:
#         cursor.execute("""INSERT INTO users (id) VALUES (:id)""", {"id": id})
#         connect.commit()


# начать
@bot.message_handler(commands=['start'])
def start_chat(message):
    bot.send_message(message.from_user.id, {
        "привет, я новостной бот, я могу рассказать тебе о некоторых новостях. для того чтобы начать выбери категорию на какую подписаться: /" +
        ' /'.join(arrCateg) + "\nлюбое нажатие на название темы приведет к подписке"})


# новости
@bot.message_handler(commands=['news'])
def send_news(message):
    # bot.reply_to(message, "Howdy, how are you doing?")
    # f'https://newsapi.org/v2/top-headlines?apiKey={api_Key}&category={k[0]}&pageSize=10'
    server.addUser(message.from_user.id)
    bot.send_message(message.from_user.id,
                     "выберите, из какой категории хотите узнать новости: /news_" + ' /news_'.join(
                         server.subInfo(message)))


# информация
@bot.message_handler(commands=['my_subscribes'])
def send_subInfo(message):
    bot.send_message(message.from_user.id, "вы подписаны на: " + ', '.join(server.subInfo(message)))


# def subInfo(message):
#     result = cursor.execute("""SELECT categories.name FROM categories, subscribes WHERE subscribes.user_id LIKE :user_id AND subscribes.category_id == categories.id""",
#         {"user_id": message.from_user.id}).fetchall()
#     arr=[]
#     for i in result:
#         arr.append(i[0])
#     return arr

# подписаться
@bot.message_handler(commands=['subscribes'])
def sub(message):
    bot.send_message(message.from_user.id, {"для подписки доступны темы: /" + ' /'.join(
        arrCateg) + "\n любое нажатие на название темы приведет к подписке!!"})


# def subUser(message, cat_id):
#     server.addUser(message.from_user.id)
#     # result = cursor.execute("""SELECT user_id, category_id FROM subscribes WHERE user_id=? AND category_id=?""" , (message.from_user.id,cat_id)).fetchone()
#     result = cursor.execute("""SELECT user_id, category_id FROM subscribes WHERE user_id=:user_id AND category_id=:cat_id""",
#                             {"user_id": message.from_user.id, "cat_id": cat_id}).fetchone()
#
#     if result == None:
#         cursor.execute("""INSERT INTO subscribes (user_id, category_id) VALUES (:user_id, :cat_id)""",
#                        {"user_id": message.from_user.id, "cat_id": cat_id})
#         connect.commit()
#         return True
#     else:
#         return False


# отписаться
@bot.message_handler(commands=['unsubscribes'])
def unsub(message):
    bot.send_message(message.from_user.id, {"чтобы отписаться выберите тему: /UN_" + ' /UN_'.join(
        server.subInfo(message)) + "\n любое нажатие на название темы приведет к отписке!!"})


# def unsubUser(message, cat_id):
#     addUser(message.from_user.id)
#     result = cursor.execute("""SELECT user_id, category_id FROM subscribes WHERE user_id=:user_id AND category_id=:cat_id""",
#                             {"user_id": message.from_user.id, "cat_id": cat_id}).fetchone()
#     if result != None:
#         cursor.execute("""DELETE FROM subscribes WHERE category_id=:cat_id and user_id=:user_id""", {"cat_id": cat_id, "user_id": message.from_user.id})
#         connect.commit()
#         return True
#     else:
#         return False


# помощь
# @bot.message_handler(func=lambda message: True)
@bot.message_handler(commands=['help'])
def get_help(message):
    bot.send_message(message.from_user.id, "для того чтобы получить новости напиши /news\n"
                                           "для того чтобы подписаться /subscribes\n"
                                           "для отписки /unsubscribes\n"
                                           "для просмотра ваших подписок /my_subscribes")


def echo_all(message):
    server.addUser(message.from_user.id)
    bot.send_message(message.from_user.id, "я не могу понять, если нужна помощь напиши \n /help ")


@bot.message_handler(content_types=['text'])
def say_smt(message):
    # if message.text.lower() == "привет":
    #     bot.send_message(message.from_user.id, "Привет")
    # else:
    echo_all(message)


bot.polling()
