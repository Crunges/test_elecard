# -*- encoding: utf-8 -*-
import requests
import json
from config import *


Player_ID = 0
Group_ID = 0


def log(response): #Функция добавления результата запроса в лог
  with open('log.py','a') as l:
    l.write (str(response.status_code) + '\n')


def Authorization(): #Авторизация на сайте
  response = requests.post(f'{url}/api/login_check', data=json.dumps(login), headers=headers) #Запрос на авторизацию
  log(response)
  json_data = json.loads(response.text)
  Auth = json_data["response"]["token"]
  Auth = f'Bearer {Auth}'
  headers['Authorization'] = Auth #Добавляем ключ в заголовки
  print(response.status_code) #Узнаем статус запроса


def New_Group(): #Добавить новую группу
  response = requests.post(f'{url}/api/v1/media_group', data=json.dumps(group), headers=headers) #Запрос на создание группы
  log(response)
  json_data = json.loads(response.text) #Получаем id
  global Group_ID
  Group_ID = json_data["response"]["id"]
  player_group["mediaGroup"] = Group_ID
  print(response.status_code)
  print('Group ID: ',Group_ID)



def New_Player(): #Добавить новый плейер
  response = requests.post(f'{url}/api/v1/media_player', data=json.dumps(player), headers=headers) #Запрос на создание плеера
  log(response)
  response_id = requests.get(f'{url}/api/v1/media_player?pagination=true&page=1&limit=20&sort[name]=asc',headers=headers) # Запрос на получение id
  log(response)
  json_data = json.loads(response_id.text) #Получаем id
  global Player_ID
  Player_ID = json_data["response"]["media_player"][0]['id']
  print('Player ID: ',Player_ID)
  print(response.status_code)


def Add_In_Group(): # Добавить плеер в группу
  response = requests.put(f'{url}/api/v1/media_player?id={Player_ID}', data=json.dumps(player_group), headers=headers) # Запрос на добавление
  log(response)
  print(response.status_code)


def Delete_Player(): #Удалить плеер
  response = requests.delete(f'{url}/api/v1/media_player?id={Player_ID}', headers=headers) # Запрос на удаление
  log(response)
  print(response.status_code)


def Delete_Group(): #Удалить группу
  response = requests.delete(f'{url}/api/v1/media_group?id={Group_ID}', headers=headers) # Запрос на удаление
  log(response)
  print(response.status_code)


Authorization()
New_Group()
New_Player()
Add_In_Group()
Delete_Player()
Delete_Group()