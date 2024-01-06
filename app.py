from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest, GetRepliesRequest, SendMessageRequest
from telethon.tl.types import MessageReplies
from telethon.tl.custom.message import Message
from telethon.tl.functions.users import GetFullUserRequest
import datetime
import time

file1 = open('user.txt', 'r')
telegram_client = file1.readlines()

api_id = int(telegram_client[0])
api_hash = telegram_client[1].replace("\n", "")
phone_number = telegram_client[2]
password = telegram_client[3]

client = TelegramClient("ins", api_id, api_hash)

client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone_number)
    print(phone_number)
    try:
        client.sign_in(phone_number, code=input('KOD: '), password=password)
    except:
        if password != "0":
            client.sign_in(password=password)





channels_file = open('channels.txt', 'r')
all_channels = channels_file.readlines()


emojis = ['👉', '🇺🇸', '🪙', '⚠️']


message_file = open('msg.txt', 'r')
msg_lines = message_file.readlines()
client_message = ''
for line in msg_lines:
    client_message += line


client_message = client_message.replace("{show}", emojis[0])
client_message = client_message.replace("{flag}", emojis[1])
client_message = client_message.replace("{coin}", emojis[2])
client_message = client_message.replace("{danger}", emojis[3])


users_file = open('user_ids.txt', 'r')
messaged_users = users_file.readlines()
users_file.close()
for i in range(len(messaged_users)):
    messaged_users[i] = messaged_users[i].replace("\n", "")



sleep_file = open('sleep.txt', 'r')
sleep_time = float((sleep_file.readlines())[0])
sleep_file.close()



for channel_username in all_channels:
    try:
        channel_entity=client.get_entity(channel_username)
        if not channel_entity:
            raise Exception
    except:
        print("Wrong channel username", channel_username)
        continue
    post_nr = 0

    for message in client.iter_messages(channel_entity):
        post_nr += 1
        try:
            result = client(GetRepliesRequest(
                peer=message.sender_id,
                msg_id=message.id,
                offset_id=0,
                offset_date=(datetime.date.today() + datetime.timedelta(days=1)),
                add_offset=0,
                limit=100,
                max_id=0,
                min_id=0,
                hash=0
            ))
            client.send_message(entity=channel_entity, message=client_message, comment_to=message, parse_mode='html')
        except Exception as e:
            print("Unsuccessful", e)
            print("Message:", message)
        time.sleep(sleep_time)
        if post_nr == 2:
            break
    print("Successful!")