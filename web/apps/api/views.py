from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import connection
from accounts.models import PassportFile
from .serializers import AccountSerializer, CardSerializer


def row_to_object(row):
    object_template = {
        "id": 100,
        "tg_id": 228,
        "tg_username": "azaza",
        "first_name": "alisher",
        "patronymic": "patronymic",
        "last_name": "last_name",
        "country": "russia",
        "region": "russia",
        "city": "russia",
        "address": "russia",
        "date_birthday": "russia",
        "document_type": "document_type",
        "credit_card": 228228228,
        "balance": 0,
        "type_payment": 1,
        "status": "None"
    }
    answer = []
    for index, value in enumerate(row):
        object = {}
        object["id"] = value[0]
        object["tg_id"] = value[1]
        object["tg_username"] = value[2]
        object["first_name"] = value[3]
        object["patronymic"] = value[4]
        object["last_name"] = value[5]
        object["country"] = value[6]
        object["region"] = value[7]
        object["city"] = value[8]
        object["address"] = value[9]
        object["date_birthday"] = value[10]
        object["document_type"] = value[11]
        object["credit_card"] = value[12]
        object["balance"] = value[13]
        object["type_payment"] = value[14]
        object["status"] = value[15]
        object["referer"] = value[16]
        answer.append(object)
    return answer


class RequestChecking(APIView):
    def get(self, request):
        req_id = request.GET.get('tg_id')
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM accounts where `tg_id` = '{req_id}'")
            row = cursor.fetchall()
        object = row_to_object(row)
        serializing_data = {
            'status': True if len(row) > 0 else False,
            'accounts': object if len(row) > 0 else []
        }

        data = AccountSerializer(data=serializing_data)
        data.is_valid(True)
        return Response({'data': data.data})


class RequestCreate(APIView):
    def post(self, request):
        tg_id = request.data.get('tg_id')
        tg_username = request.data.get('tg_username')
        first_name = request.data.get('first_name')
        patronymic = request.data.get('patronymic')
        last_name = request.data.get('last_name')
        country = request.data.get('country')
        region = request.data.get('region')
        city = request.data.get('city')
        address = request.data.get('address')
        date_birthday = request.data.get('date_birthday')
        document_type = request.data.get('document_type')
        credit_card = request.data.get('credit_card')
        balance = request.data.get('balance')
        type_payment = request.data.get('type_payment')
        referer = request.data.get('referer')
        status = request.data.get('status')
        with connection.cursor() as cursor:
            cursor.execute(
                f"INSERT INTO "
                f"`accounts`"
                f"(`tg_id`, `tg_username`, `first_name`, `patronymic`, `last_name`, `country`, `region`, `city`, "
                f"`address`,`date_birthday`, `document_type`, `credit_card`, `balance`, `type_payment`, `status`, `referer`, `new_status`) "
                f"VALUES"
                f"('{tg_id}', '{tg_username}', '{first_name}', '{patronymic}', '{last_name}', '{country}', '{region}', '{city}',"
                f"'{address}', '{date_birthday}', '{document_type}', '{credit_card}', '{balance}', '{type_payment}', '{status}', '{referer}', 'Входящая')")
            cursor.execute(f"SELECT * FROM accounts where `tg_id` = '{tg_id}'")
            id = cursor.fetchone()[0]
        return Response({'status': True, 'id': id})


class RequestStatusChange(APIView):
    def put(self, request):
        # id = request.data.get('id')
        # tg_id = request.data.get('tg_id')
        # tg_username = request.data.get('tg_username')
        # first_name = request.data.get('first_name')
        # patronymic = request.data.get('patronymic')
        # last_name = request.data.get('last_name')
        # country = request.data.get('country')
        # region = request.data.get('region')
        # city = request.data.get('city')
        # address = request.data.get('address')
        # date_birthday = request.data.get('date_birthday')
        # document_type = request.data.get('document_type')
        # credit_card = request.data.get('credit_card')
        # balance = request.data.get('balance')
        # type_payment = request.data.get('type_payment')
        # referer = request.data.get('referer')
        # status = request.data.get('status')
        query = "UPDATE `accounts` SET "
        for index, key in enumerate(list(request.data.keys())):
            if(index == len(list(request.data.keys()))-1):
                query += f"`{key}`='{request.data.get(key)}' "
            else:
                query += f"`{key}`='{request.data.get(key)}', "
        query+= f"WHERE `id`='{request.data.get('id')}'"
        with connection.cursor() as cursor:
            cursor.execute(query)
            connection.commit()
        return Response({'status': True})


class CardChecking(APIView):
    def get(self, request):
        card = request.GET.get('card')
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM accounts where `credit_card` = '{card}'")
            row = cursor.fetchall()
        object = row_to_object(row)
        serializing_data = {
            'status': True if len(row) > 0 else False,
            'accounts': object if len(row) > 0 else []
        }

        data = CardSerializer(data=serializing_data)
        data.is_valid(True)
        return Response({'data': data.data})


class ReferalsChecking(APIView):
    def get(self, request):
        data = {}
        with connection.cursor() as cursor:
            cursor.execute("SELECT type_payment FROM referals")
            types = cursor.fetchall()
        for type_ in types:
            data[str(type_[0])] = 0


        to_id = request.GET.get('to_id')
        status = request.GET.get('status')
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM `referals` WHERE `to_id`='{to_id}' AND `status`='{status}'")
            referals = cursor.fetchall()

        for referal in referals:
            if(str(referal[4]) in data.keys()):
                data[str(referal[4])] = data[str(referal[4])] + 1
            # with connection.cursor() as cursor:
            #     cursor.execute(f"SELECT * FROM accounts where `tg_id` = '{referal[2]}'")
            #     row = cursor.fetchall()
            # account_referal = row_to_object(row)
            #
            # if (str(account_referal[0]['type_payment']) in data.keys()):
            #     data[str(account_referal[0]['type_payment'])] = data[str(account_referal[0]['type_payment'])] + 1

        return Response(data)


class ReferalCreate(APIView):
    def post(self, request):
        from_id = request.data.get('from_id')
        to_id = request.data.get('to_id')
        status = request.data.get('status')
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM `referals` WHERE `to_id`='{to_id}' AND `from_id`='{from_id}'")
            referals = cursor.fetchall()
        if(len(referals) > 0):
            return Response({'status': False})
        type_payment = request.data.get('type_payment')
        with connection.cursor() as cursor:
            cursor.execute(
                f"INSERT INTO "
                f"`referals`"
                f"(`from_id`, `to_id`, `status`, `type_payment`)"
                f"VALUES"
                f"('{from_id}', '{to_id}', '{status}', '{type_payment}')")
            cursor.execute(f"SELECT * FROM referals where `from_id` = '{from_id}'")
            id = cursor.fetchone()[0]
        return Response({'status': True, 'id': id})

class PhotoUpdate(APIView):
    def post(self, request):
        tg_id = request.data.get('tg_id')
        path = request.data.get('url')
        passport = PassportFile.objects.create(tg_id=tg_id, path=path)
        return Response({'status': True})

