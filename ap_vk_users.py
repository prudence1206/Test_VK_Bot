import requests
from pprint import pprint
from Constant import TOKEN_USER


class VK_Users:
    def __init__(self, TOKEN_USER):
        self.URL_API = 'https://api.vk.com/method'
        self.TOKEN_USER = TOKEN_USER


    def data_users(self, sex, city, year):
        age_from = 2019-year
        age_to = 2029-year
        params = {
            'access_token': self.TOKEN_USER,
            'sort': 0,
            'count': 1000,
            'has_photo': 1,
            'v': 5.199,
            'fields': 'city,sex,counters',
            'birth_year': year,
            'age_from': age_from,
            'age_to': age_to,
            'city': city,  # идентификатор города
            'sex': sex
        }
        data_users = []
        response = requests.get(f'{self.URL_API}/users.search', params=params)
        data = response.json()['response']['items']
        for user in data:
            try:
                if user['sex'] == sex and user['city']['id'] == 2 :
                    data_users.append(user['id'])
                    # print('ok')
            except:
                pass
        return data_users


    def get_user_info(self, user_vk):
        params = {
            'access_token': self.TOKEN_USER,
            'user_ids': user_vk,
            'fields': 'city,sex,bdate',
            'v': 5.199
            }
        response = requests.get(f'{self.URL_API}/users.get', params=params)
        user_info = response.json()['response'][0]
        user_info = [user_info['id'], user_info['first_name'], user_info['last_name'],
                     user_info['city']['id'], user_info['sex'], user_info['bdate'][5:]]
        return user_info


    def photos_user(self, user_vk):
        params = {
            'access_token': self.TOKEN_USER,
            'user_id': user_vk,
            'extended': 1,
            'v': 5.199
            }
        photos = {}
        response = requests.get(f'{self.URL_API}/photos.getUserPhotos', params=params)
        user_photos = response.json()['response']['items']
        for photo in user_photos:
             photos.update({photo['likes']['count']: photo['sizes'][-2]['url']})
        sort_photos = sorted(photos.items())
        photos = sort_photos[-3:]
        return  (photos[0][1], photos[1][1], photos[2][1])



# ap = VK_Users(TOKEN_USER)
# sex = 1
# city = 2
# year = 1986
# data_qoest = ap.data_users(sex, city, year)
# pprint(data_qoest)
# user_vk = 711878878
# user_vk = 809529828
# print(ap.get_user_info(user_vk))
# pprint(data_qoest[0])
# user_vk = 567469497
# api.count_photos(data_qoest)
# pprint(ap.photos_user(user_vk))

