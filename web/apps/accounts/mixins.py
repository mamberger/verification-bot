from .models import Accounts
from users.models import User
from telegram_api.app import send_message


def change_status_func(worker, account_id, status):
    account = Accounts.objects.get(pk=account_id)
    access = False
    admin = User.objects.get(pk=worker)
    # Проверка прав на операцию
    if status == 'Входящая':
        access = check_1(admin, account, worker)
    # ----
    elif status == 'Принята':
        access = check_2(admin, account)
    # ----
    elif status == 'Отклонена':
        access = check_3(admin, account, worker)
    # ----
    elif status == 'Одобрена':
        access = check_3(admin, account, worker)
    elif status == 'Выплачена':
        access = check_4(admin, account, worker)
    # Действие
    if access:
        if status == 'Входящая':
            account.worker = None # При переводе во входящие снимаем с заявки воркера (менеджера)
        if status == 'Принята': # При переводе в Принятые назначаям менеджером того, кто назначил статус
            account.worker = admin
            message_to_client(worker, account_id)
        account.new_status = status
        account.save()
    else:
        pass #сообщить об ошибке доступа.


# Проверка прав на назначение Входящего статуса
def check_1(admin, account, worker):
    access = False
    if admin.get_group() == 'Администратор' or account.worker == worker:
        access = True
    if account.new_status == 'Принята' or account.new_status == 'Отклонена':
        pass
    else:
        access = False
    return access


# Проверка прав на назначение Принятого статуса
def check_2(admin, account):
    access = False
    if admin.get_group() == 'Регистратор':# or admin.get_group() == 'Администратор':
        access = True
    if account.new_status != 'Входящая':
        access = False
    return access


# Проверка прав на назначение Отклоненного и Одобренного статусов (потому что условия одинаковые для проверки)
def check_3(admin, account, worker):
    access = False
    if account.worker == worker or admin.get_group() == 'Администратор':
        access = True
    if account.new_status != 'Принята':
        access = False
    return access


# Проверка прав на назначение статуса Выплачено
def check_4(admin, account, worker):
    access = False
    if admin.get_group() == 'Администратор':
        access = True
    if account.new_status != 'Одобрена':
        access = False
    return access


# Оповещает клиента об изменении статуса его заявки
def message_to_client(worker, account_id):
    worker_username = User.objects.get(pk=worker)
    worker_username = worker_username.username
    content_message_invite = f"Вашу заявку принял @{worker_username}. \n Вы можете обращяться к нему если возникнут вопросы."
    send_message(account_id=account_id, text=content_message_invite)

    # content_message_instructions = f"*Перейдите по ссылке:* [перейти...]({request.POST['link']}) \n*Инструкция*: \n{request.POST['instruction']}"
    # send_message(account_id=select_account.id, text=content_message_instructions)
