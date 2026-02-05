from datetime import datetime, timezone
import locale
import requests

def unix_to_date(unix_timestamp):
    return datetime.fromtimestamp(unix_timestamp, tz=timezone.utc)

months_ru = [
    "января", "февраля", "марта", "апреля", "мая", "июня",
    "июля", "августа", "сентября", "октября", "ноября", "декабря"
]

locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')



def get_chat_avito(user_id, MAX = 100, MESSAGE_LIMIT = 100):
    last_date = None
    total_messages = 0
    offset = 0


    while total_messages < MAX:
        print('New zapros')
        remaining_messages = MAX - total_messages
        limit = min(remaining_messages, MESSAGE_LIMIT)

        url = f'https://api.avito.ru/messenger/v3/accounts/ID/chats/{user_id}/messages/?offset={offset}&limit={limit}'  # Chat URL
                    #https://api.avito.ru/messenger/v3/accounts/{user_id}/chats/{chat_id}/messages/
            # Headers with authorization token
        headers = {
            'Authorization': f'Bearer NONE'  # Authorization header with Bearer token
        }

        # Send GET request to fetch chats

        response = requests.get(url, headers=headers)
        response.encoding = "utf-8"
        status_code = response.status_code
        print(status_code)

        response_body = response.json()
        #print(response_body)
        if 'messages' not in response_body or len(response_body['messages']) == 0:
            break
        try:
            #print(type(response_body['messages']))
            offset += len(response_body['messages'])
            total_messages  += len(response_body['messages'])


            for i in response_body['messages'][::-1]:
                #print(i['created'])
                current_date = unix_to_date(i['created'])
                if current_date != last_date:
                    print(f"{current_date.day} {months_ru[current_date.month - 1]}")  # Выводим дату в формате "день месяц"
                    last_date = current_date  # Обновляем последнюю дату

                if i['type'] == 'text':
                    razdel = ''
                    if i['direction'] == 'in':
                        razdel = '--------->'
                    else: razdel = '<---------'

                    print(razdel  , i['content']['text'])
                    print(current_date.strftime('%H:%M'))
        except:
            raise

get_chat_avito('ID',MAX=100 )
