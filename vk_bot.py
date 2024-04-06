import random
from random import randrange
from Constant import TOKEN_GR, TOKEN_USER, TOKEN_GR2, TOKEN_GR3
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from ap_vk_users import VK_Users
from base import Metod

vk = vk_api.VkApi(token=TOKEN_GR)
longpoll = VkLongPoll(vk)
ap = VK_Users(TOKEN_USER)
bd = Metod()


def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message,  'random_id': randrange(10 ** 7),})

def show_us(): #показывает кандидата
    # us = random.choice(DATA_US)
    us = bd.get_user_random(q_inf[0])
    us_info = ap.get_user_info(us)
    us_url = f'https://vk.com/id{us}'
    write_msg(event.user_id, f'{us_info[1]} {us_info[2]}')
    photos = ap.photos_user(g_id)
    write_msg(event.user_id, photos[0])
    # добавить фото
    # добавляем в избранное или удаляем из DATA_US



for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            request = event.text
            q_id = event.user_id
            q_inf = ap.get_user_info(event.user_id)
            print(q_inf)
            if q_inf[4] == 2: q_sex = 1
            else: q_sex = 2

            goest_in_bd = bd.add_quests(q_inf[0]) # есть или нет в списке bd добавить гостя
            if goest_in_bd == False:   #если гостя нет
                write_msg(event.user_id, f"Привет, {q_inf[1]}!")
                write_msg(event.user_id, "Формируется база подходящих тебе кандидатов....ждите")
                DATA_US = ap.data_users(q_sex, q_inf[3], q_inf[5])
                bd.add_users(q_inf[0],DATA_US)
                write_msg(event.user_id, "Для просмотра отправь сообщение - 'СЛЕДУЮЩИЙ'")
                write_msg(event.user_id, "Для просмотра избранного, отправь сообщение - 'ИЗБРАННОЕ'")
            write_msg(event.user_id, "Для просмотра кандидата набери команду 'СЛЕДУЮЩИЙ'")
            if request.upper() == 'СЛЕДУЮЩИЙ':
                show_us()

            elif request.upper() == 'ИЗБРАННОЕ':
                pass
                # добавить список из базы
