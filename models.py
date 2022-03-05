import sqlite3, config

class Account:
    def __init__(self, 
                    tg_id=None, 
                    tg_username=None,  
                    document_type=None,
                    
                    first_name=None,
                    patronymic=None, 
                    last_name=None,
                    country=None, 
                    region=None, 
                    city=None,
                    address=None,
                    date_birthday=None,
                    credit_card=None,
                    balance=0,

                    type_payment=None
                     ):

        self.tg_id = tg_id
        self.tg_username = tg_username
        self.document_type = document_type
        
        self.first_name = first_name
        self.patronymic = patronymic
        self.last_name = last_name
        self.country = country
        self.region = region
        self.city = city
        self.address = address
        self.date_birthday = date_birthday
        self.credit_card = credit_card
        self.balance = balance
        self.type_payment = type_payment


        self.connection = sqlite3.connect(config.db_file, check_same_thread=False)




    @staticmethod
    def dict_factory(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    def select_where(self, field, param):
        self.connection.row_factory = self.dict_factory
        cursor = self.connection.cursor()
        query = f"SELECT * FROM accounts WHERE `{field}` = '{param}'"
        cursor.execute(query)
        return cursor.fetchall()


    def paid_account(self, tg_id_param, price):
        cursor = self.connection.cursor()
        query = f"SELECT `balance` FROM `accounts` WHERE `tg_id` = '{tg_id_param}'"
       # print(query)
        cursor.execute(query)
        referal_account_balance = cursor.fetchone()[0]
        referal_account_balance += 100
        
        query = f"UPDATE `accounts` SET `balance`='{referal_account_balance}' WHERE `tg_id` = '{tg_id_param}'"
        cursor.execute(query)
        self.connection.commit()


    def save(self):
        print(f"~USER: {self.tg_username} is saving~")
        cursor = self.connection.cursor()
        query = f"INSERT INTO accounts (`tg_id`, `tg_username`, `first_name`, \
        `patronymic`, `last_name`, `country`, `region`, `city`, `address`, `date_birthday`, `document_type`, `credit_card`, `balance`, `type_payment`) \
         VALUES ('{self.tg_id}', '{self.tg_username}', '{self.first_name}', \
             '{self.patronymic}', '{self.last_name}', '{self.country}', '{self.region}', \
            '{self.city}', '{self.address}', '{self.date_birthday}', '{self.document_type}', '{self.credit_card}', '{self.balance}', '{self.type_payment}'  \
         ); "


        cursor.execute(query)
        self.connection.commit()

    
    def update(self):
        cursor = self.connection.cursor()
        query = f"UPDATE `accounts` SET `credit_card`='{self.credit_card}' WHERE `tg_id`='{self.tg_id}' "
        cursor.execute(query)

        self.connection.commit() 

    def updateById(self, column, value, tg_id):
        cursor = self.connection.cursor()
        query = f"UPDATE accounts SET `{column}` = '{value}' WHERE `tg_id` = '{tg_id}' "
        cursor.execute(query)

        self.connection.commit()

    def get_column_by_id(self, column, tg_id):
        cursor = self.connection.cursor()
        query = f"SELECT `{column}` FROM `accounts` WHERE `tg_id`='{tg_id}'"
        cursor.execute(query)

        return cursor.fetchone()[0]

    def get_object(self, tg_id):
        self.connection.row_factory = self.dict_factory
        cursor = self.connection.cursor()
        query = f"SELECT * FROM `accounts` WHERE `tg_id` = '{tg_id}'"
        cursor.execute(query)

        account_info = cursor.fetchone()
        self.tg_id = account_info['tg_id']
        self.tg_username = account_info['tg_username']
        self.document_type = account_info['document_type']
        
        self.first_name = account_info['first_name']
        self.patronymic = account_info['patronymic']
        self.last_name = account_info['last_name']
        self.country = account_info['country']
        self.region = account_info['region']
        self.city = account_info['city']
        self.address = account_info['address']
        self.date_birthday = account_info['date_birthday']
        self.credit_card = account_info['credit_card']
        self.balance = account_info['balance']
        self.type_payment = account_info['type_payment']

    def show(self):
        print(f"[tg_id]: {self.tg_id}")
        print(f"[tg_username]: {self.tg_username}")
        print(f"[document_type]: {self.document_type}")

        print(f"[first_name]: {self.first_name}")
        print(f"[patronymic]: {self.patronymic}")
        print(f"[last_name]: {self.last_name}")
        print(f"[country]: {self.country}")
        print(f"[region]: {self.region}")
        print(f"[city]: {self.city}")
        print(f"[address]: {self.address}")
        print(f"[birthday]: {self.date_birthday}")

        print(f"[balance]: {self.balance}")



class Referal:
    def __init__(self, from_id=None, to_id=None):

        self.from_id = from_id
        self.to_id = to_id

        self.connection = sqlite3.connect(config.db_file, check_same_thread=False)


    @staticmethod
    def dict_factory(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    def select_where_unique(self, from_id, to_id):
        cursor = self.connection.cursor()
        query = f"SELECT * FROM `referals` WHERE `from_id`='{from_id}' AND `to_id`='{to_id}'"
        cursor.execute(query)
        return cursor.fetchall()


    def save(self):
        cursor = self.connection.cursor()
        query = f"INSERT INTO referals (`from_id`, `to_id`) VALUES('{self.from_id}', '{self.to_id}')"
        cursor.execute(query)

        self.connection.commit()

    def select_where(self, from_id):
        self.connection.row_factory = self.dict_factory
        cursor = self.connection.cursor()
        query = f"SELECT * FROM `referals` WHERE `from_id`='{from_id}'"
        cursor.execute(query)
        return cursor.fetchall()



class Mailing:
    def __init__(self,
                        id=None,
                        tg_id=None,
                        tg_username=None,
                        tg_chat_id=None,
                        create=None):
    
        self.id = id
        self.tg_id = tg_id
        self.tg_username = tg_username
        self.tg_chat_id = tg_chat_id
        self.create = create

        self.connection = sqlite3.connect(config.db_file, check_same_thread=False)

    @staticmethod
    def dict_factory(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d


    def select_where(self, tg_id):
        self.connection.row_factory = self.dict_factory
        cursor = self.connection.cursor()
        query = f"SELECT * FROM `accounts_mailing` WHERE `tg_id`='{tg_id}'"
        cursor.execute(query)
        return cursor.fetchall()

    def save(self):
        cursor = self.connection.cursor()
        query = f"INSERT INTO `accounts_mailing`(`tg_id`, `tg_username`, `tg_chat_id`, `create`) VALUES('{self.tg_id}', '{self.tg_username}', '{self.tg_chat_id}', '{self.create}') " 
        cursor.execute(query)

        self.connection.commit()


class PassportFile:

    def __init__(self, 
                        id=None,
                        tg_id=None,
                        path=None):
    
        self.id = id
        self.tg_id = tg_id
        self.path = path
        
        self.connection = sqlite3.connect(config.db_file, check_same_thread=False)


    @staticmethod
    def dict_factory(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    def save(self):
        cursor = self.connection.cursor()
        query = f"INSERT INTO `accounts_passportfile`(`tg_id`, `path`) VALUES('{self.tg_id}', '{self.path}') " 
        cursor.execute(query)

        self.connection.commit()


    def select_where(self, tg_id):
        self.connection.row_factory = self.dict_factory
        cursor = self.connection.cursor()
        query = f"SELECT * FROM `accounts_passportfile` WHERE `tg_id`='{tg_id}'"
        cursor.execute(query)
        return cursor.fetchall()