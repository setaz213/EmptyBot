import vk_api
import requests
import pymysql
import pymysql.cursors
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import time
import threading as her
import json
import re
import random

global vk
global longpoll
global true
global false

true = True
false = False


def conn():
    con = pymysql.connect('localhost', 'root', '', 'Empty',cursorclass=pymysql.cursors.DictCursor)
    #con = pymysql.connect('node84046-empty.mircloud.ru', 'root', 'VSNrrr74711', 'Empty',cursorclass=pymysql.cursors.DictCursor)
    return con

def getCurrentTime():
    t = time.strftime("%d.%m.%Y %H:%M:%S", time.localtime())
    return t

vk_session = vk_api.VkApi(token='4f01f40c2c2f9213ce9f31609015476f762d760ba80c6c78adc704d166f9a764e60d097edb3917ab31e55')
longpoll = VkBotLongPoll(vk_session, 194551980)
vk = vk_session.get_api()
print(getCurrentTime(),' авторизация успешна!')

def message_send(message,user_id,keyb=None,att=None):
    try:
        itog = vk.messages.send(random_id=0,peer_id = user_id,message=message,keyboard=keyb,attachment=att)
        return itog
    except Exception as err:
        print(getCurrentTime(),' message_send error:',err)

def chat_kick(args,fwd,peer_id):
    users = ' '.join(args).replace(', ',',').split(',')
    cant_remove = []
    not_found = []
    if len(users) > 0 and users != ['']:
        for user in users:
            try:
                if user.isdigit():
                    user_id = int(user)
                elif '[' in user and ']' in user and '|' in user and ('id' in user or 'club' in user):
                    user_id = int(re.findall(r'\d+', user)[0])
                    if '[club' in user:
                        user_id *= -1
            except:
                pass
            try:
                if user_id != 194551980:
                    oks = vk.messages.removeChatUser(chat_id=peer_id-2000000000,member_id=user_id)
                else:
                    pass

            except vk_api.exceptions.ApiError as vk_error:
                error_code = vk_error.error['error_code']
                if error_code == 15:
                    cant_remove.append(user_id)
                elif error_code == 935:
                    not_found.append(user_id)


    elif len(fwd) > 0:
        for user in fwd:
            user_id = user['from_id']
            peer_id = peer_id-2000000000
            try:
                if user_id != 194551980:
                    oks = vk.messages.removeChatUser(chat_id=peer_id-2000000000,member_id=user_id)
                else:
                    pass
            except vk_api.exceptions.ApiError as vk_error:
                error_code = vk_error.error['error_code']
                if error_code == 15:
                    cant_remove.append(user_id)
                elif error_code == 935:
                    not_found.append(user_id)

    print(cant_remove,not_found)
def main():
    print(getCurrentTime(), ' main() запущен!')
    con = conn()
    print(getCurrentTime(),' подключение к БД успешно!\n')

    while True:
        try:
            for event in longpoll.listen():
                if event.type == VkBotEventType.MESSAGE_NEW:
                    user_id = event.object.from_id
                    peer_id = event.object.peer_id
                    message = event.object.text.strip(' ')
                    print(message)
                    if len(message)>0:
                        if message[0] == '!' and peer_id not in []:
                            message = message.replace('!','',1).strip(' ')
                            command = message.split(' ')[0]
                            args = message.replace(command,'',1).strip(' ').split(' ')

                            if command in ['кик','kick']:
                                chat_kick(args,event.object.fwd_messages,peer_id)

        except Exception as err:
            print(getCurrentTime(),' main() error: ',err)
            continue

if __name__ == '__main__':
    maincode = her.Thread(target=main)
    maincode.start()