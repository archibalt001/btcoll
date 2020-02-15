# Разработал MrCreepTon специально для HackMySoftware (vk.com/hackmysoftware).
# Пожалуйста, не стирайте реквизиты, уважайте труд людей.

import requests
import json
import numpy as np
import random
import re
import threading

access_token = '7c9892b1de32dfe1aa795af3a13fa236caf8064d4a2a731441aba9e747db38dddbe09cf5798828bca075a' #Токен группы (должны быть права на сообщения)
public_key = '43ed55cb6ed63cfbcb7e16b9dd19713d' #API ключ от zvonok.com
group_id = '192023852' #ID группы (положительное число!)

#Название пранка, ид кампании Zvonok.com, ид аудио VK
pranks = [['Покупка спермы', '333358995', 'audio548061425_456239426'], ['Порнография на компе', '', '']]

keyboard_main = json.dumps({
    "one_time": False,
    "buttons": [
        [{
            "action":
            {
                "type": "text",
                "label": "Пранки"
            },
            "color": "primary"
        }],
        [{
            "action":
            {
                "type": "text",
                "label": "Ключи"
            },
            "color": "primary"
        }]
    ]
})

keyboard_pranks = json.dumps({
    "one_time": False,
    "buttons": [
        [{
            "action":
            {
                "type": "text",
                "label": pranks[0][0]
            },
            "color": "secondary"
        },
        {
            "action":
            {
                "type": "text",
                "label": pranks[1][0]
            },
            "color": "secondary"
        }],
        [{
            "action":
            {
                "type": "text",
                "label": pranks[2][0]
            },
            "color": "secondary"
        },
        {
            "action":
            {
                "type": "text",
                "label": pranks[3][0]
            },
            "color": "secondary"
        }],
        [{
            "action":
            {
                "type": "text",
                "label": pranks[4][0]
            },
            "color": "secondary"
        },
        {
            "action":
            {
                "type": "text",
                "label": pranks[5][0]
            },
            "color": "secondary"
        }],
        [{
            "action":
            {
                "type": "text",
                "label": 'Назад'
            },
            "color": "primary"
        }]
    ]
})

print('Call Prank Бот успешно запустился!\nРазработал MrCreepTon для vk.com/hackmysoftware')

def sendMessage(peerid, message, keyboard, attachment):
    r = 'https://api.vk.com/method/messages.send?access_token=' + access_token + '&peer_id=' + str(peerid) + '&random_id=' + str(np.int64(random.randint(10000, 1000000000000))) + '&group_id=' + group_id + '&v=5.52&message=' + str(message)
    if keyboard != None:
        r = r + '&keyboard=' + str(keyboard)
    if attachment != None:
        r = r + '&attachment=' + attachment
    requests.get(r)


def isWhiteListed(peerid):
    f = open('whitelist.txt', 'r')
    lines = f.readlines()
    for line in lines:
        line = line.split()
        try:
            if line[0] == str(peerid):
                return True
        except IndexError:
            print('index error')
    return False

def addToBase(id, keys):
    f = open('users.txt', 'a')
    f.write('\n' + str(id) + ' 0 ' + str(keys))
    f.close()

def setPrank(id, prank):
    f = open('users.txt', 'r')
    lines = f.readlines()
    f.close()
    done = ''
    for line in lines:
        data = line.split()
        try:
            if data[0] == str(id):
                done = done + data[0] + ' ' + str(prank) + ' ' + data[2] + '\n'
            else:
                done = done + line
        except IndexError:
            print('index error')
    f = open('users.txt', 'w')
    f.write(done)
    f.close()

def removeKey(id):
    f = open('users.txt', 'r')
    lines = f.readlines()
    f.close()
    done = ''
    for line in lines:
        data = line.split()
        try:
            if data[0] == str(id):
                done = done + data[0] + ' ' + data[1] + ' ' + str(int(data[2]) - 1) + '\n'
            else:
                done = done + line
        except IndexError:
            print('index error')
    f = open('users.txt', 'w')
    f.write(done)
    f.close()

def getPrank(id):
    f = open('users.txt', 'r')
    lines = f.readlines()
    for line in lines:
        line = line.split()
        try:
            if line[0] == str(id):
                return int(line[1])
        except IndexError:
            print('index error')
    return None

def getKeys(id):
    f = open('users.txt', 'r')
    lines = f.readlines()
    for line in lines:
        line = line.split()
        try:
            if line[0] == str(id):
                return int(line[2])
        except IndexError:
            print('index error')
    return None

def mainMenu(peerid):
    sendMessage(peerid, 'Добро пожаловать в главное меню!', keyboard_main, None)

def validNumber(number):
    number = number.replace('-', '')
    number = number.replace('(', '')
    number = number.replace(')', '')
    number = number.replace(' ', '')
    if number.startswith('+7'):
        number = number.split('+7')
        try:
            #print(str(len(number[1])))
            if len(number[1]) != 10:
                return None
            else:
                return '+7' + number[1]
        except IndexError:
            return None
    elif number.startswith('8'):
        h = slice(1, 11)
        try:
            print(number[h])
            if len(number[h]) != 10:
                return None
            else:
                return '+7' + number[h]
        except IndexError:
            return None
    return None


def isInBase(id):
    f = open('users.txt', 'r')
    lines = f.readlines()
    for line in lines:
        line = line.split()
        try:
            if line[0] == str(id):
                return True
        except IndexError:
            print('index error')
    return False

def call(peerid, number, prank):
    print('[ID: '+str(peerid)+'] Начало пранка')
    campaign_id = ''
    callid = ''
    end = False
    for i in range(0, 7):
        if prank == i:
            campaign_id = pranks[i][1]
            r = requests.post('https://calltools.ru/lk/cabapi_external/api/v1/phones/call/?campaign_id=' + campaign_id + '&phone=+' + number + '&public_key=' + public_key)
            data = json.loads(r.text)
            callid = data['call_id']
    while True:
        r = requests.get('https://calltools.ru/lk/cabapi_external/api/v1/phones/calls_by_phone/?campaign_id=' + campaign_id + '&phone=+' + number + '&public_key=' + public_key)
        data = json.loads(r.text)
        for i in range(0, len(data)):
            if data[i]['call_id'] == callid:
                if data[i]['status'] == 'compl_finished':
                    end = True
                    sendMessage(peerid, 'Пранк успешно завершен!\n\nПослушать: ' + data[i]['recorded_audio'], keyboard_main, None)
                    break
                elif data[i]['status'] == 'attempts_exc':
                    end = True
                    sendMessage(peerid, 'Жертва не взяла трубку!', keyboard_main, None)
                    break
        if end:
            break
while True:
    r = requests.get('https://api.vk.com/method/messages.getLongPollServer?access_token=' + access_token + '&ts=1&v=5.52')
    ts = str(json.loads(r.text)['response']['ts'])
    key = str(json.loads(r.text)['response']['key'])
    server = str(json.loads(r.text)['response']['server'])
    r = requests.get('https://' + server + '?act=a_check&key=' + key + '&ts=' + ts + '&wait=1&mode=2&version=3')
    data = json.loads(r.text)['updates']
    for message in data:
        if message[0] == 4:
            msg = str(message[5])
            if not isWhiteListed(message[3]):
                sendMessage(message[3], 'Вас нет в списке юзеров!', keyboard_main, None)
                print('[ID: '+str(message[3])+'] Отсутствие в списке юзеров')
            else:
                if not isInBase(message[3]):
                    addToBase(message[3], 5)
                    sendMessage(message[3], 'Вы отсутствовали в БД. Вам выдано 5 ключей', keyboard_main, None)
                    print('[ID: '+str(message[3])+'] Новый юзер')

                prank = False
                for i in range(0, 6):
                    if msg == pranks[i][0]:
                        prank = True
                        setPrank(str(message[3]), i)
                        sendMessage(message[3], 'Установлен пранк: ' + pranks[i][0] + '\nТеперь укажите номер, и мы сразу позвоним!', keyboard_main, 'audio' + pranks[i][2])
                        break
                if prank:
                    break
                if msg == 'Пранки':
                    attach = ''
                    for i in range(0, len(pranks)):
                        attach = attach + 'audio' + pranks[i][2] + ','
                    sendMessage(message[3], 'Выберите желаемый пранк', keyboard_pranks, attach)
                elif msg == 'Ключи':
                    sendMessage(message[3], 'У вас: ' + str(getKeys(str(message[3]))) + ' ключей', keyboard_main, None)
                else:
                    try:
                        try:
                            number = validNumber(msg)
                            if number == None:
                                mainMenu(str(message[3]))
                            else:
                                if getKeys(str(message[3])) == 0:
                                    sendMessage(message[3], 'Упс! У вас кончились ключи! Попросите у создателя еще!', keyboard_main, None)
                                else:
                                    removeKey(str(message[3]))
                                    sendMessage(str(message[3]), 'Звоним на номер ' + number + ' пранком ' + pranks[getPrank(str(message[3]))][0], keyboard_main, None)
                                    x = threading.Thread(target = call, args = (message[3], number, getPrank(str(message[3]))))
                                    x.start()
                        except phonenumbers.phonenumberutil.NumberParseException:
                            mainMenu(str(message[3]))
                    except IndexError:
                        mainMenu(str(message[3]))
