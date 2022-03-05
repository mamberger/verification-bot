"""""
v. 1
"""""

# Callback Handlers - 64 line
#


import telebot,re, urllib, logging
import config

import db_functions

from models import Account, Referal, Mailing, PassportFile
from datetime import datetime, date, timedelta

from bot_modules import referal_module

bot = telebot.TeleBot(config.token, parse_mode="Markdown", threaded=True)


#logger = telebot.logger
#telebot.logger.setLevel(logging.DEBUG)

"""
    Function: send_start
    Exec: cmd = /start
    NextStep: {
        not loggined = callback_handlers

    }
"""
@bot.message_handler(commands=['start'])
def send_start(message):
    hide_keyboard = telebot.types.ReplyKeyboardRemove(selective=False)
    bot.send_message(message.chat.id, f"Привет _{message.from_user.first_name} {message.from_user.last_name}_!", reply_markup=hide_keyboard)
    
    get_account = db_functions.select_where(table_name='accounts',field='tg_id', param=message.from_user.id)
    
    """"if len(get_account) == 1:
        if get_account[0]['status'] == "-1":
            bot.send_message(message.chat.id, "*Привет!* Ты не закончил регистрацию!")
            
            if get_account[0]['document_type'] is None:
                get_document_type(message)
            elif get_account[0]['credit_card'] is None:
                input_credit_card(message)

            elif get_account[0]['first_name'] is None:
                set_first_name(message)
            
            elif get_account[0]['patronymic'] is None:
                set_patronymic(message)


            elif get_account[0]['last_name'] is None:
                set_last_name(message)
                
            elif get_account[0]['country'] is None:
                    (message)
            
            elif get_account[0]['region'] is None:
                set_region(message)

            elif get_account[0]['city'] is None:
                set_city(message)
            
            elif get_account[0]['address'] is None:
                set_address(message)
            
            elif get_account[0]['date_birthday'] is None:
                set_birthday(message)

            elif get_account[0]['type_payment'] is None:
                set_type_payment(message)

            else:
                show_menu(message)

        else:
            show_menu(message)
    else:
    """""

    db_functions.init_user(message.chat.id, message.from_user.username)
    try:
        if int(message.text.split()[1]) != message.chat.id:
            db_functions.init_referal(from_id=message.text, to_id=message.chat.id)
        else:
            print("~is your tg id~")
            raise ValueError("~is your tg id~")
    except:
        print("~dont referal~")

    select_refer_register_markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    referal = telebot.types.InlineKeyboardButton("Привлечь людей", callback_data="go_to_referal")
    register = telebot.types.InlineKeyboardButton("Пройти регистрацию", callback_data="yeah_get_money")
    select_refer_register_markup.add(referal, register)

    show_start_inline = bot.send_message(message.chat.id, "*Ты хочешь заработать немного денег?!* \nХочешь привлечь друзей или зарегистрироваться за деньги? ", reply_markup=select_refer_register_markup)

#   -----------------Callback Handlers-----------------

#                     After /start
#   ___________________________________________________


def show_menu(message):
    menu_markup = telebot.types.ReplyKeyboardMarkup(row_width=1)
    balance = telebot.types.KeyboardButton("Мой баланс")
    referal = telebot.types.KeyboardButton("Мои рефералы")
    set_passportfile = telebot.types.KeyboardButton("Загрузить фото паспорта")
    menu_markup.add(balance, referal)

    passportfile_object = PassportFile().select_where(tg_id=message.chat.id)
    if len(passportfile_object) == 0:
        menu_markup.add(set_passportfile)

    bot.send_message(message.chat.id, "*Ваше меню:*", reply_markup=menu_markup)

@bot.callback_query_handler(func=lambda call: call.data in ["yeah_get_money", "go_to_referal"])
def select_register_referal_handler(call):
    if(call.data == "yeah_get_money"):
        age_markup = telebot.types.InlineKeyboardMarkup(row_width=1)
        yes = telebot.types.InlineKeyboardButton("Да", callback_data="yeah_18")
        no = telebot.types.InlineKeyboardButton("Нет", callback_data="no_18")
        age_markup.add(yes, no)

        bot.send_message(call.message.chat.id, "Для регистрации подходят люди старше 18 лет, у которых есть при себе документ, удостоверяющий личность. (Тебе есть 18 лет?)", 
            reply_markup=age_markup
        )

    elif(call.data == "go_to_referal"):
        db_functions.set_value('accounts', call.message.chat.id, "status", "ref_account:-1")
        bot.send_message(call.message.chat.id, "*Отлично!* Реферальная заявка будет создана после ввода некоторых данных:")
        
        referal_set_first_name(call.message)
#   ___________________________________________________

#                  Callback select country
#   ___________________________________________________
@bot.callback_query_handler(func=lambda call: call.data in ["Украина", "Россия", "Казахстан"])
def select_country(call):
    db_functions.set_value(
                            table_name="accounts",
                            tg_id=call.message.chat.id,
                            column="country",
                            value=call.data
    )
    
    set_region(call.message)
#   ___________________________________________________

#                   Callback select where will
#                        verification
#   ___________________________________________________
@bot.callback_query_handler(func=lambda call: call.data in ["now_verification", "later_verification"])
def select_time_verification(call):
    if call.data == "now_verification":
        blank_photo = open('telegram_assets/blank.jpg', 'rb')
        bot.send_photo(call.message.chat.id, blank_photo)
        label_verification_photo = bot.send_message(call.message.chat.id, "Для подтверждения своих данных ,которые Вы предоставили  нужно приложить Фото документа на фоне переписки с ботом (где видно последнее сообщение)  как на примере выше.")
        bot.register_next_step_handler(label_verification_photo, download_verification_photo)

    else:
        bot.send_message(call.message.chat.id, "*Хорошо, ваша заявка будет создана.*\nПозже вы сможете загрузить документы в личном кабинете.")
        finish_proccess(call.message)


def get_document_type(message):
    select_document_markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    id_passport = telebot.types.InlineKeyboardButton("ID паспорт", callback_data="have_id_pass")
    licenses = telebot.types.InlineKeyboardButton("Права пластиковые", callback_data="have_licenses")
    custom_pass = telebot.types.InlineKeyboardButton("Загранпаспорт", callback_data="have_custom_pass")
    select_document_markup.add(id_passport, licenses, custom_pass)

    bot.send_message(message.chat.id, "Для граждан Украины подходят ID паспорт, права пластиковые, загранпаспорт. (что у тебя есть? )", 
        reply_markup=select_document_markup
    )


@bot.callback_query_handler(func=lambda call: True)
def callback_handerl(call):
    if(call.data == "yeah_18"):
        get_document_type(call.message)
        
    elif(call.data == "have_id_pass"):
        db_functions.set_value(
                                table_name='accounts', 
                                tg_id=call.message.chat.id, 
                                column='document_type', 
                                value="ID паспорт")

        input_credit_card(call.message)

    elif(call.data == "have_licenses"):
        db_functions.set_value(
                                        table_name='accounts', 
                                        tg_id=call.message.chat.id, 
                                        column='document_type', 
                                        value="Пластиковая карта")
        input_credit_card(call.message)

    
    elif(call.data == "have_custom_pass"):
        db_functions.set_value(
                                table_name='accounts', 
                                tg_id=call.message.chat.id, 
                                column='document_type', 
                                value="Загранпаспорт")

        input_credit_card(call.message)


    elif(call.data == "select_payment_100"):
        db_functions.set_value(
                                table_name='accounts', 
                                tg_id=call.message.chat.id, 
                                column='type_payment', 
                                value="100")

        set_verification_time(call.message)

                

    elif(call.data == "select_payment_300"):
        db_functions.set_value(
                                table_name='accounts', 
                                tg_id=call.message.chat.id, 
                                column='type_payment', 
                                value="300")
        time_verification_markup = telebot.types.InlineKeyboardMarkup(row_width=1)
        now = telebot.types.InlineKeyboardButton("Сейчас", callback_data="now_verification")
        later = telebot.types.InlineKeyboardButton("Позже", callback_data="later_verification")
        time_verification_markup.add(now, later)

        bot.send_message(call.message.chat.id, "Готов сейчас пройти верефикацию с документами?\n*Ссылка на регистрицию действует 15 минут...*",
            reply_markup = time_verification_markup
        )

    elif(call.data == "back_to_main_menu"):
        menu_markup = telebot.types.ReplyKeyboardMarkup(row_width=1)
        balance = telebot.types.KeyboardButton("Мой баланс")
        referal = telebot.types.KeyboardButton("Мои рефералы")
        set_passportfile = telebot.types.KeyboardButton("Загрузить фото паспорта")
        menu_markup.add(balance, referal)

        passportfile_object = PassportFile().select_where(tg_id=call.message.chat.id)
        if len(passportfile_object) == 0:
            menu_markup.add(set_passportfile)

        bot.send_message(call.message.chat.id, "*Ваше меню:*", reply_markup=menu_markup)
    
    
    elif(call.data == "go_to_withdraw"):
        withdraw_module(call.message)



    elif(call.data == "yeah_valid_credit_card"):
        hide_keyboard = telebot.types.ReplyKeyboardRemove(selective=False)

        bot.send_message(call.message.chat.id, "create order to withdraw")

    elif(call.data == "no_valid_credit_card"):
        label_new_credit_card = bot.send_message(call.message.chat.id, "Введите новый номер карты:")
        bot.register_next_step_handler(label_new_credit_card, input_new_credit_card)


def download_verification_photo(message):
    if message.content_type == "document":
        document_id = message.document.file_id
        file_info = bot.get_file(document_id)
        path_file = "static/tg_documents/"+str(message.chat.id)+".jpg"
        data = urllib.request.urlretrieve(f'http://api.telegram.org/file/bot{config.token}/{file_info.file_path}', path_file)
        
        PassportFile(tg_id=message.chat.id, path=path_file).save()
        

        finish_proccess(message)  

    elif message.content_type == "photo":
        photo_id = message.photo[-1].file_id
        photo_info = bot.get_file(photo_id)
        path_file = "static/tg_documents/"+str(message.chat.id)+".jpg"
        data = urllib.request.urlretrieve(f'http://api.telegram.org/file/bot{config.token}/{photo_info.file_path}', path_file)
        PassportFile(tg_id=message.chat.id, path=path_file).save()
        
        finish_proccess(message)

def input_credit_card(message):
    label_credit = bot.send_message(message.chat.id, "*Введите свою банковскую карту для выплаты вам денег:*")
    bot.register_next_step_handler(label_credit, set_credit_card)

def set_first_name(message):
    label_first_name = bot.send_message(message.chat.id, "*Имя* как в документе:")
    bot.register_next_step_handler(label_first_name, input_first_name)

def set_last_name(message):
    label_last_name = bot.send_message(message.chat.id, "*Фамилия* как в документе:")
    bot.register_next_step_handler(label_last_name, input_last_name)



def set_patronymic(message):
    get_document_type = db_functions.select_param_account(message.chat.id, "document_type")
    if get_document_type['document_type'] != "Загранпаспорт":
        label_patronymic = bot.send_message(message.chat.id, "*Отчество* как в документе:")
        bot.register_next_step_handler(label_patronymic, input_patronymic)
    else:
        db_functions.set_value(
                                table_name="accounts",
                                tg_id=message.chat.id,
                                column="patronymic",
                                value="не указано"
        )
        
        set_last_name(message)




def set_credit_card(message):
    check_validate = re.match(config.pattern_credit_card, message.text)
    multi_get_account_credit_card = db_functions.select_where(table_name="accounts", field="credit_card", param=message.text)
    if check_validate:    
        db_functions.set_value('accounts', message.chat.id, "credit_card", message.text)
        bot.send_message(message.chat.id, "Перепишите ваши данные как в документе, который вы выбрали выше.")
        set_first_name(message)

    else:
        label_error = bot.send_message(message.chat.id, "_Номер карты не корректный!_\nПовторите ещё раз:")
        bot.register_next_step_handler(label_error, set_credit_card)

def set_country(message):
    select_country_markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    ukraine = telebot.types.InlineKeyboardButton("Украина", callback_data="Украина")
    russia = telebot.types.InlineKeyboardButton("Россия", callback_data="Россия")
    kaz = telebot.types.InlineKeyboardButton("Казахстан", callback_data="Казахстан")
    select_country_markup.add(ukraine, russia, kaz)

    label_country = bot.send_message(message.chat.id, "*Страна:*", reply_markup=select_country_markup)

def set_region(message):
    label_region = bot.send_message(message.chat.id, "*Область:*")
    bot.register_next_step_handler(label_region, input_region)

def set_city(message):
    label_city = bot.send_message(message.chat.id, "*Город:*")
    bot.register_next_step_handler(label_city, input_city)

def set_address(message):
    label_address = bot.send_message(message.chat.id, "*Адресс:*")
    bot.register_next_step_handler(label_address, input_address)


def set_birthday(message):
    label_datebirthday = bot.send_message(message.chat.id, "*Дата рождения.* Формат: _день-месяц-год_")
    bot.register_next_step_handler(label_datebirthday, input_datebirthday)

def set_type_payment(message):
    select_payment_markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    payment_100 = telebot.types.InlineKeyboardButton("100грн.", callback_data="select_payment_100")
    payment_300 = telebot.types.InlineKeyboardButton("300грн.", callback_data="select_payment_300")
    select_payment_markup.add(payment_100, payment_300)


    bot.send_message(message.chat.id, "Есть 2 варианта оплаты:\n*Сразу после регистрации - 100 грн.* \n *До 7 дней - 300грн.*",
        reply_markup=select_payment_markup
    )


def set_verification_time(message):
    time_verification_markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    now = telebot.types.InlineKeyboardButton("Сейчас", callback_data="now_verification")
    later = telebot.types.InlineKeyboardButton("Позже", callback_data="later_verification")
    time_verification_markup.add(now, later)

    bot.send_message(message.chat.id, "Готов сейчас пройти верефикацию с документами?\n*Ссылка на регистрицию действует 15 минут...*",
        reply_markup = time_verification_markup
    )

def input_first_name(message):
    db_functions.set_value(
                            table_name='accounts', 
                            tg_id=message.chat.id, 
                            column='first_name',
                            value=message.text)
    
    set_patronymic(message)


def input_patronymic(message):
    db_functions.set_value(
                            table_name="accounts",
                            tg_id=message.chat.id,
                            column="patronymic",
                            value=message.text
    )
    label_last_name = bot.send_message(message.chat.id, "*Фамилия* как в документе:")
    bot.register_next_step_handler(label_last_name, input_last_name)

def input_last_name(message):
    multi_get_account_with_last_name = db_functions.select_where(table_name="accounts", field="last_name", param=message.text)
    print("Last_name: ", len(multi_get_account_with_last_name))
    db_functions.set_value(
                            table_name="accounts",
                            tg_id=message.chat.id,
                            column="last_name",
                            value=message.text

    )
    set_country(message)
    
def input_region(message):
    db_functions.set_value(
                            table_name="accounts",
                            tg_id=message.chat.id,
                            column="region",
                            value=message.text
    )

    set_city(message)


def input_city(message):
    db_functions.set_value(
                                table_name="accounts",
                                tg_id=message.chat.id,
                                column="city",
                                value=message.text
        )    
    set_address(message)

def input_address(message):
    db_functions.set_value(
                            table_name="accounts",
                            tg_id=message.chat.id,
                            column="address",
                            value=message.text
    )    
    set_birthday(message)


def input_datebirthday(message):
    try:
        date_birthday = datetime.strptime(message.text, "%d-%m-%Y")
        # Convert datetime to date date_birthday.  
        age = int((date.today() - date_birthday.date()) / timedelta(days=365.2425))
        if age < 18:
            db_functions.delete_record('accounts', 'tg_id', message.chat.id)
            print("try delete")
            referal_markup = telebot.types.InlineKeyboardMarkup(row_width=1)
            go_to_referal = telebot.types.InlineKeyboardButton("Привлечь людей", callback_data="go_to_referal")
            referal_markup.add(go_to_referal)
            bot.send_message(message.chat.id, "*Регистрацию могут пройти только если вам есть 18 лет!*\nМожете заработать на реферальной системе.", reply_markup=referal_markup)
        else:
            db_functions.set_value(
                                    table_name="accounts",
                                    tg_id=message.chat.id,
                                    column="date_birthday",
                                    value=message.text
            ) 
            set_type_payment(message)
            
          
    except ValueError:
        label_error = bot.send_message(message.chat.id, "*Неверный формат даты!* Повторите ещё раз.")
        bot.register_next_step_handler(label_error, input_datebirthday)


def finish_proccess(message):
    db_functions.set_value(table_name="accounts", tg_id=message.chat.id, column="balance", value=0)
    db_functions.set_value(table_name="accounts", tg_id=message.chat.id, column="status", value="None")

    check_referal = db_functions.select_param_wtgid(table_name="referals", where="to_id", value=message.chat.id, param="from_id")
    print(check_referal)

    # Check multi accounts...
    get_first_name = db_functions.select_param_account(message.chat.id, "first_name")
    get_last_name = db_functions.select_param_account(message.chat.id, "last_name")
    get_credit_card = db_functions.select_param_account(message.chat.id, "credit_card")
    
    multi_get_account_with_first_last_name = db_functions.select_where_and(
        table_name="accounts",
        field="first_name",
        param = get_first_name['first_name'],
        second_field = "last_name",
        second_param = get_last_name['last_name']
    )


    count_multi_account_first_and_last = len(multi_get_account_with_first_last_name)
    if count_multi_account_first_and_last > 1:
        print(count_multi_account_first_and_last)
        get_account_id = db_functions.select_param_account(message.chat.id, "id")['id']
        db_functions.init_multiaccounts(message.chat.id, get_account_id, first_last_field=False, credit_card_field=False)
        db_functions.set_value('accounts_multiaccounts', message.chat.id, 'first_last_field', True)

    multi_get_account_with_credit_card = db_functions.select_where(
                                            table_name='accounts', 
                                            field="credit_card", 
                                            param=get_credit_card['credit_card'])    

   
    count_credit_card = len(multi_get_account_with_credit_card)

    if count_credit_card > 1:
        get_account_id = db_functions.select_param_account(message.chat.id, "id")['id']
        check_multi_record = len(db_functions.select_where('accounts_multiaccounts', 'tg_id', message.chat.id))
        if check_multi_record >= 1:
            db_functions.set_value('accounts_multiaccounts', message.chat.id, 'credit_card_field', True)
        else:
            db_functions.init_multiaccounts(message.chat.id, get_account_id)
            db_functions.set_value('accounts_multiaccounts', message.chat.id, 'credit_card_field', True)


    check_mailing = len(Mailing().select_where(message.chat.id))
    if check_mailing == 0:
        print("create mailing")
        mailing = Mailing(tg_id = message.chat.id, tg_username=message.from_user.username,
                tg_chat_id = message.chat.id, create=datetime.now()
            )
        mailing.save()


    bot.send_message(message.chat.id, f"Всё, готово! \nТеперь ожидайте когда вашу заявку примет наш сотрудник с инструкцией. *Перейти в меню*: /start")



@bot.message_handler(content_types=['text'])
def menu_options(message):
    if(message.text ==  "Мой баланс"):
        balance_method_markup = telebot.types.InlineKeyboardMarkup(row_width=1)
        change_number_card = telebot.types.InlineKeyboardButton("Изменить реквизиты", callback_data="no_valid_credit_card")
        balance_method_markup.add(change_number_card)
        
        balance = db_functions.select_param_account(message.chat.id, "balance")
        bot.send_message(message.chat.id, f"Ваш баланс: *{balance['balance']}* грн.", reply_markup=balance_method_markup)

    elif(message.text == "Мои рефералы"):
        referals = Referal().select_where(message.chat.id)

        one_hundred_payment_list = list()
        three_hundred_payment_list = list()
        for referal in referals:
            account_referal = Account().select_where('tg_id', referal['to_id'])[0]
            
            if account_referal['type_payment'] == 100:
                one_hundred_payment_list.append(account_referal)
            elif account_referal['type_payment'] == 300:
                three_hundred_payment_list.append(account_referal)
            
        
        one_hundred_payment_count = len(one_hundred_payment_list)
        three_hundred_payment_count = len(three_hundred_payment_list)
        bot.send_message(message.chat.id, f"*Ваши рефералы:*\n_Оплата 100грн.: {one_hundred_payment_count}_\n_Оплата 300грн.: {three_hundred_payment_count}_\n_Всего: {one_hundred_payment_count+three_hundred_payment_count}_")
        
        generate_referal_link = config.blank_referals+str(message.chat.id)
        bot.send_message(message.chat.id, f"Ваша реферальная ссылка:\n[{generate_referal_link}]({generate_referal_link})")

    elif(message.text == "Загрузить фото паспорта"):
        blank_photo = open('telegram_assets/blank.jpg', 'rb')
        bot.send_photo(message.chat.id, blank_photo)
        label_verification_photo = bot.send_message(message.chat.id, "Для подтверждения своих данных ,которые Вы предоставили  нужно приложить Фото документа на фоне переписки с ботом (где видно последнее сообщение)  как на примере выше.")
        bot.register_next_step_handler(label_verification_photo, download_verification_photo)
    
def select_balance_option(message):
    if(message.text == "Заказать выплату"):
        withdraw_module(message)

def withdraw_module(message):
    change_credit_markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    yes = telebot.types.InlineKeyboardButton("Да", callback_data="yeah_valid_credit_card")
    no = telebot.types.InlineKeyboardButton("Нет", callback_data="no_valid_credit_card")
    change_credit_markup.add(yes, no)

    get_credit_card = Account().get_column_by_id(column="credit_card", tg_id=message.chat.id)
    bot.send_message(message.chat.id, f"Ваши реквизиты: *{get_credit_card}* \nВерно?", reply_markup=change_credit_markup)


def input_new_credit_card(message):

    check_validate = re.match(config.pattern_credit_card, message.text)
    if check_validate:
        Account().updateById(column="credit_card", value=message.text, tg_id=message.chat.id)

        bot.send_message(message.chat.id, "_Ваши реквизиты успешно обновлены!_")    
    else:
        label_error = bot.send_message(message.chat.id, "_Номер карты не корректный.\nПоробуйте ещё раз_")
        bot.register_next_step_handler(label_error, input_new_credit_card)


def referal_set_first_name(message):
    label_set_first_name = bot.send_message(message.chat.id, "Введите ваше *имя*: ")
    bot.register_next_step_handler(label_set_first_name, referal_input_first_name)

def referal_input_first_name(message):
    db_functions.set_value('accounts', message.chat.id, "first_name", message.text)

    referal_set_last_name(message)

def referal_set_last_name(message):
    label_set_first_name = bot.send_message(message.chat.id, "Введите вашу *фамилию*: ")
    bot.register_next_step_handler(label_set_first_name, referal_input_last_name)
 
def referal_input_last_name(message):
    db_functions.set_value('accounts', message.chat.id, "last_name", message.text)

    db_functions.set_value('accounts', message.chat.id, "balance", 0)
    
    mailing = Mailing(tg_id = message.chat.id, tg_username=message.from_user.username,
                tg_chat_id = message.chat.id, create=datetime.now()
            )
    mailing.save()
    

    db_functions.set_value('accounts', message.chat.id, "status", "ref_account:1")
    bot.send_message(message.chat.id, "*Отлично* Ваша реферальная заявка была создана. \nМожете перейти в ваше меню: /start")



bot.polling(non_stop=True)