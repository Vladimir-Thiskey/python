'''Одноразовый парсер'''
from time import sleep
import requests
import json
import jsonlines
from random import randint


def Capchaa():
    ya_payload = "некий пейлод"
    ya_url = 'https://captcha-api.yandex.ru/check'

    ya_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
    }

    ya_res = requests.post(ya_url, headers=ya_headers, data=ya_payload)

    res = ya_res.json()
    #print('Получен ключ от Яндекс:', res['spravka'])
    print('Получен ключ от Яндекс')

    return res['spravka']


url = 'https://admin.leader-id.ru/api/v4/auth/login?'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive'
}

body = {
        'captcha': Capchaa(),
        "email": "логин",
        "password": "пароль"
    }

response = requests.post(url, data=json.dumps(body), headers=headers) #json.dumps() преобразует словарь в json

if response.ok:
    print('Успешный успех')
    headers["Authorization"] = 'Bearer ' + response.json()["data"]["access_token"]
    sleep(10)

dictionary = {}
out = jsonlines.open('output.jsonl', mode='a')

for page in range(1, 3062):
    print('Parsing page ', page)
    user_url = f'https://admin.leader-id.ru/api/v4/admin/users?sort=registration&paginationPage={page}&paginationSize=1000'
    response_user = requests.get(user_url, headers=headers)
    users = response_user.json()["data"]["_items"]

    prev_user = ' '

    for user in users:
        dictionary['original_full_name'] = user["name"]

        if user["photo"] == "Не указано":
            dictionary['photo_url'] = None
        else:
            dictionary['photo_url'] = user["photo"]

        dictionary['email'] = user["email"]

        dictionary['phone'] = user["phone"]

        if user["telegram"] == "Не указано":
            dictionary['telegram_url'] = None
        else:
            dictionary['telegram_url'] = user["telegram"]

        if user["employment"]['company'] == "Не указано":
            dictionary['current_company_name'] = None
        else:
            dictionary['current_company_name'] = user["employment"]['company']

        if user["employment"]['position'] == "Не указано":
            dictionary['profession'] = None
        else:
            dictionary['profession'] = user["employment"]['position']

        dictionary['address'] = user["address"]

        if user["lastSeen"] == "Не указано":
            dictionary['updated_at'] = None
        else:
            date = user["lastSeen"].split(' ')
            dictionary['updated_at'] = date[0] + 'T' + date[1]

        if dictionary['original_full_name'] != prev_user:
            out.write(dictionary)

        prev_user = dictionary['original_full_name']

    sleep(randint(2, 4))

out.close()
