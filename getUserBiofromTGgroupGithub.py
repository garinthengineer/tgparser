from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.functions.users import GetFullUserRequest
import time
import os, time, datetime, pickle

# if datetime.datetime.today().weekday() < 5:
if True:
    api_id =  # Вставить свой Id
    api_hash =  # Вставить свой hash
    phone =  # Телефон в формате +7...

    client = TelegramClient(phone, api_id, api_hash)
    client.connect()

    # При первом подключении запросит код, код придет вам в телеграм

    if not client.is_user_authorized():
        client.send_code_request(phone)
        client.sign_in(phone, input('Enter the code: '))

    # Запросить свои чаты

    chats = []
    last_date = None
    chunk_size = 200
    groups=[]

    result = client(GetDialogsRequest(
                 offset_date=last_date,
                 offset_id=0,
                 offset_peer=InputPeerEmpty(),
                 limit=chunk_size,
                 hash = 0
             ))
    chats.extend(result.chats)

    
    # Отфильтровать группы
    for chat in chats:
        try:
            if (chat.megagroup == True or chat.gigagroup == True) or chat.boradcast == True:
                groups.append(chat)
        except:
            continue

    # Получить нужную группу по ID, посмотрите нужный айдишник в массиве groups, который мы создали на предыдущем этапе
    for g in groups:
        if g.id == # Вставить айди группы сюда
            p = client.get_participants(g)
            print("doing {}".format(g.id))

    # Получить полную информацию о каждом юзере в группе. (Может занять некоторое время, так как между запросами стоит таймаут в одну секунду
    number = len(p)
    done = 0
    users = []
    
    for u in p:
        ufull = client(GetFullUserRequest(u))
        done += 1
        print("{} to go. Doing {}".format(number-done, ufull.users[0].id))
        users.append(ufull)
        time.sleep(1)

    # Вывести Имя, Фамилию и bio (если есть, на экран)
    count = 0
    for u in users:
        if u.full_user.about is not None:
            count += 1
            print("{}. {} {}: {}".format(count,u.users[0].first_name, u.users[0].last_name, u.full_user.about))

    # Сохранить в файл, для дальнейшей работы
    with open('usersfulinfo.pkl', 'wb') as f:
        pickle.dump(users, f)

