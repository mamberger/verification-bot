import blank
from django.db import models
from users.models import User


class Accounts(models.Model):
    id = models.AutoField(primary_key=True)
    tg_id = models.IntegerField(blank=True, null=True)
    tg_username = models.TextField(blank=True, null=True)  
    first_name = models.TextField(blank=True, null=True)  # This field type is a guess.
    patronymic = models.TextField(blank=True, null=True)
    last_name = models.TextField(blank=True, null=True)
    country = models.TextField(blank=True, null=True)  # This field type is a guess.
    region = models.TextField(blank=True, null=True)
    city = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    date_birthday = models.TextField(blank=True, null=True)
    document_type = models.TextField(blank=True, null=True)
    credit_card = models.IntegerField(blank=True, null=True)
    balance = models.IntegerField(blank=True, null=True)
    type_payment = models.IntegerField(blank=True, null=True)
    status = models.TextField(default=None)
    new_status = models.TextField(default='Входящая', blank=True, db_index=True) # новое поле для статусов заявки
    worker = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None) # поле в которое присваивается ид менеджера при статусе "Принята"
    comment = models.TextField(blank=True, null=True)
    chat_link = models.TextField(null=True)
    referer = models.IntegerField(blank=True, null=True)

    def get_multiaccount_status(self):
        try:
            result = MultiAccounts.objects.get(tg_id=self.tg_id)
            print(result.credit_card_field)
            return result
        except:
            return None

    def get_passport_file_status(self):
        try:
            result = PassportFile.objects.get(tg_id=self.tg_id)
            return result
        except:
            return None


    def get_datetime(self):
        try:
            result = Mailing.objects.get(tg_id=self.tg_id)
            datetime_create = result.create
            minute_format = datetime_create.minute
            if datetime_create.minute < 10:
                minute_format = "0"+str(datetime_create.minute)
            format_text = f"{datetime_create.hour}:{minute_format}"
            return format_text
        except Exception as e:
            return None

    def get_drop_datetime(self):
        try:
            result = Mailing.objects.get(tg_id=self.id)
            datetime_create = result.create
            minute_format = datetime_create.minute
            if datetime_create.minute < 10:
                minute_format = "0"+str(datetime_create.minute)
            format_text = f"{datetime_create.hour}:{minute_format}"
            return format_text

        except Exception as e:
            return None
    
    def get_datetime_object(self):
        if self.status == "drop" or self.status == "drop_done":
            try:
                print("drop")
                result = Mailing.objects.get(tg_id = self.id)
                datetime_create = result.create
                return datetime_create
            except Exception as e:
                print(e)
        else:
            try:
                print("def")
                result = Mailing.objects.get(tg_id = self.tg_id)
                datetime_create = result.create
                return datetime_create
            except:
                pass
            
    def get_drop_user(self):
        if self.status == "drop" or self.status == "drop_done":
            get_drop_account = DropAccount.objects.get(account_id=self.id)
            return get_drop_account.drop_user

    def get_completed_datetime(self):
        if self.status == "1" or self.status == "drop_done":
            get_completed_object = Completed.objects.get(account_id=self.id)
            datetime_create = get_completed_object.datetime
            minute_format = datetime_create.minute
            if datetime_create.minute < 10:
                minute_format = "0"+str(datetime_create.minute)
            format_text = f"{datetime_create.hour}:{minute_format}"
            return format_text

    class Meta:
        #managed = False # при ошибке во время миграций закомментируй эту строку
        db_table = 'accounts'


class Completed(models.Model):
    id = models.AutoField(primary_key=True)
    registrator_id = models.ForeignKey(User, on_delete=models.CASCADE)
    account_id = models.ForeignKey(Accounts, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50)
    link = models.CharField(max_length=50)
    instruction = models.TextField()

    def get_registrator_username(self):
        return "@"+User.objects.get(id=self.registrator_id.id).username

    def get_account(self):
        return self.account_id


class Mailing(models.Model):
    id = models.AutoField(primary_key=True)
    tg_id = models.IntegerField()
    tg_username = models.CharField(max_length=255)
    tg_chat_id = models.IntegerField()
    create = models.DateTimeField(auto_now_add=True, blank=True) 


class PassportFile(models.Model):
    id = models.AutoField(primary_key=True)
    tg_id = models.IntegerField()
    path = models.CharField(max_length=255)


class BanList(models.Model):
    id = models.AutoField(primary_key=True)
    tg_id = models.IntegerField()
    account_id = models.ForeignKey(Accounts, on_delete=models.CASCADE)
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.CharField(max_length=255)


class MultiAccounts(models.Model):
    id = models.AutoField(primary_key=True)
    tg_id = models.IntegerField()
    account_id = models.ForeignKey(Accounts, on_delete=models.CASCADE)
    first_last_field = models.CharField(max_length=15)
    credit_card_field = models.CharField(max_length=15)

    def get_similar_accounts(self):
        if self.first_last_field == "True":
            return Accounts.objects.filter(first_name=self.account_id.first_name, last_name=self.account_id.last_name)
    
        elif self.credit_card_field == "True":
            return Accounts.objects.filter(credit_card=self.account_id.credit_card)

# ВНИМАНИЕ!!!
# В ходе анализа кода, будешь видеть что при заявке дроповода, статусы drop, drop_done
# И в некоторые таблицы в tg_id пишем номер заявки.
class DropAccount(models.Model):
    id = models.AutoField(primary_key=True)
    account_id = models.IntegerField()
    drop_user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_account(self):
        return Accounts.objects.get(id=self.account_id)

