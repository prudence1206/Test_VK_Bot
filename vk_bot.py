import random
from random import randrange
from Constant import TOKEN_GR, TOKEN_USER, TOKEN_GR2, TOKEN_GR3
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from ap_vk_users import VK_Users
from base import Metod, create_tables

vk = vk_api.VkApi(token=TOKEN_GR)
longpoll = VkLongPoll(vk)
ap = VK_Users(TOKEN_USER)
bd = Metod()
create_tables()

def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message,  'random_id': randrange(10 ** 7),})


def show_us(): #показывает кандидата
    photos = 'NONE'
    while photos == 'NONE':     # проверяет наличие фото у кандидатов
        us = bd.get_user_random(q_inf[0])
        print(us)
        us_info = ap.get_user_info(us)
        print(us_info)
        us_url = f'https://vk.com/id{us}'
        photos = ap.photos_user(us_info[0]) # если вернет NONE, хорошо бы заодно удалить
    print(us_info)
    write_msg(event.user_id, f'{us_info[1]} {us_info[2]}')
    write_msg(event.user_id, f'{us_url}')
    write_msg(event.user_id, photos[0])
    write_msg(event.user_id, photos[1])
    write_msg(event.user_id, photos[2])
    write_msg(event.user_id, "Для просмотра следующего кандидата набери команду 'ПОИСК'")
    write_msg(event.user_id, "Для просмотра избранного, набери команду - 'ИЗБРАННОЕ'")
    # добавляем в избранное или удаляем из DATA_US

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            request = event.text
            q_inf = ap.get_user_info(event.user_id)  # получаем инфу по гостю
            # print(q_inf)
            if q_inf[4] == 2: q_sex = 1    # меняем пол на противоположный
            else: q_sex = 2
            goest_in_bd = bd.add_quests(q_inf[0]) # есть или нет в базе (если нет то добавляет)
            if goest_in_bd == False:   #если гостя нет формируем базу юзеров
                write_msg(event.user_id, f"Привет, {q_inf[1]}!")
                write_msg(event.user_id, "Формируется база подходящих тебе кандидатов....ждите")
                # DATA_US = ap.data_users(q_sex, q_inf[3], q_inf[5])  # вытаскиваем id юзеров из API VK (по критериям)
                DATA_US = ap.data_users(1, 2, 1986)
                bd.add_users(q_inf[0],DATA_US)                     # записываем в базу
                # write_msg(event.user_id, "Для просмотра отправь сообщение - 'СЛЕДУЮЩИЙ'")
                write_msg(event.user_id, "Для просмотра следующего кандидата набери команду 'ПОИСК'")
                write_msg(event.user_id, "Для просмотра избранного, набери команду - 'ИЗБРАННОЕ'")

            # print(event.text)
            if request.upper() == 'ПОИСК':
                show_us()

            elif request.upper() == 'ИЗБРАННОЕ':
                pass
                # добавить список из базы
