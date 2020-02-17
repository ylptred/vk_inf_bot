import vk_api
import random
from vk_api.longpoll import VkLongPoll
from vk_api.longpoll import VkEventType
import sqlite3

conn = sqlite3.connect("db.db")
c = conn.cursor()

vk_session = vk_api.VkApi(token='token')

longpoll = VkLongPoll(vk_session)

vk = vk_session.get_api()

global Random


def random_id():
    Random = 0
    Random += random.randint(0, 100000000)
    return Random


def check_if_exists(user_id):
    c.execute("SELECT * FROM users WHERE user_id=%d" % user_id)
    result = c.fetchone()
    if result is None:
        return False
    return True


def register_new_user(user_id):
    c.execute("INSERT INTO users(user_id, state) VALUES (%d, '')" % user_id)
    conn.commit()
    c.execute("INSERT INTO user_info(user_id, user_wish, user_image) VALUES (%d, 0, '')" % user_id)
    conn.commit()


def get_user_existance(user_id):
    c.execute("SELECT user_wish FROM user_info WHERE user_id=%d" % user_id)
    result = c.fetchone()
    return result[0]


def get_user_state(user_id):
    c.execute("SELECT state FROM users WHERE user_id = {}".format(event.user_id))
    result = c.fetchone()
    return result[0]


def set_user_existance(user_id, user_wish):
    c.execute("UPDATE user_info SET user_wish=%d WHERE user_id=%d" % (user_wish, user_id))
    conn.commit()


def set_user_state(user_id, state):
    c.execute("UPDATE users SET state='{}' WHERE user_id={}".format(state, user_id))
    conn.commit()


def change():
    while True:
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                print(event.user_id, ' ', 'Написал сообщение длиной ', len(event.text), ' ', 'message: ', event.text)
                if event.text.count('-') >= 1 or event.text.count('–') >= 1:
                    set_user_state(event.user_id, event.text)
                    vk.messages.send(
                        user_id=event.user_id,
                        random_id=random_id(),
                        message='Спасибо, вы успешно заменили треки',
                        keyboard=open('all_on.json', 'r', encoding="UTF-8").read()
                    )
                    return
                elif event.text.lower() == 'не редактировать список':
                    vk.messages.send(
                        user_id=event.user_id,
                        random_id=random_id(),
                        message='Ок',
                        keyboard=open('all_on.json', 'r', encoding="UTF-8").read()
                    )
                    return


def add():
    while True:
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                print(event.user_id, ' ', 'Написал сообщение длиной ', len(event.text), ' ', event.text)
                if event.text.count('-') >= 1 or event.text.count('–') >= 1:
                    var = get_user_state(event.user_id) + '\n' + event.text
                    set_user_state(event.user_id, var)
                    set_user_existance(event.user_id, 1)
                    vk.messages.send(
                        user_id=event.user_id,
                        random_id=random_id(),
                        message='Спасибо, вы успешно дополнили свой список',
                        keyboard=open('all_on.json', 'r', encoding="UTF-8").read()
                    )
                    return
                elif event.text.lower() == 'не дополнять список':
                    vk.messages.send(
                        user_id=event.user_id,
                        random_id=random_id(),
                        message='Ок',
                        keyboard=open('all_on.json', 'r', encoding="UTF-8").read()
                    )
                    return


print('Я живой!')
while True:
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            print(event.user_id, ' ', 'Написал сообщение длиной ', len(event.text), ' ', event.text)

            if not check_if_exists(event.user_id):
                register_new_user(event.user_id)

            if event.text.lower() == 'отредактировать список' and get_user_existance(event.user_id) == 1:
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=random_id(),
                    message='Отправьте, пожалуйста, новый список в нужном формате',
                    keyboard=open('no_change.json', 'r', encoding="UTF-8").read()
                )
                change()
            elif event.text.lower() == 'отредактировать список' and get_user_existance(event.user_id) == 0:
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=random_id(),
                    message='Вообще-то Вы не отправили еще ни одного трека',
                    keyboard=open('all_on.json', 'r', encoding="UTF-8").read()
                )
            elif event.text.lower() == 'дополнить список':
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=random_id(),
                    message='Отправьте, пожалуйста, трек, который я должен добавить',
                    keyboard=open('no_extra.json', 'r', encoding="UTF-8").read()
                )
                add()
            elif event.text.lower() == 'помощь':
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=random_id(),
                    message='Привет!'
                            '\n'
                            'Я - бот(Версия 1.2) 11А для сбора треков на выпускной.'
                            '\n'
                            'Напиши мне, пожалуйста, >=2 трека(медляки + обычные) в таком формате:'
                            '\n'
                            '"ДЕТИ RAVE - Хороводы в Аду'
                            '\n'
                            'Скриптонит - Это Любовь"'
                            '\n'
                            'Спасибо)'
                            '\n'
                            '\n'
                            'Создатель: @ylptred'
                            '\n'
                            'Мой GitHub: https://github.com/ylptred',
                    keyboard=open('all_on.json', 'r', encoding="UTF-8").read()
                )

            elif event.text.count('-') >= 1 or event.text.count('–') >= 1:

                if get_user_existance(event.user_id) == 0:
                    set_user_existance(event.user_id, 1)
                    set_user_state(event.user_id, event.text)
                    vk.messages.send(
                        user_id=event.user_id,
                        random_id=random_id(),
                        message='Спасибо! Ваши треки приняты)',
                        keyboard=open('all_on.json', 'r', encoding="UTF-8").read()
                    )

            else:
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=random_id(),
                    message='Перечитайте, пожалуйста, правила)',
                    keyboard=open('all_on.json', 'r', encoding="UTF-8").read()
                )