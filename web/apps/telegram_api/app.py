import requests

token = "2088176622:AAEE7qtK3XOJxbbK9mbwMoNpMXDN7bbh_fc"
TG_URL = "https://api.telegram.org/bot"+token

from accounts.models import Accounts, Mailing


def send_message(account_id, text):
    try:
        get_account = Accounts.objects.get(id=account_id)
        get_chat_id = Mailing.objects.get(tg_id=get_account.tg_id).tg_chat_id
        #print(get_account)
        
        body = {
            "chat_id": get_account.tg_id,
            "text": text,
            "parse_mode": "Markdown"
        }
        reponse = requests.get(TG_URL+"/sendMessage", data = body)
        print(response)
    except Exception as e:
        print(e)