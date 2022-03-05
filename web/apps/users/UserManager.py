from django.contrib.auth.models import BaseUserManager

"""
Django требует, чтобы кастомные пользователи определяли свой собственный
класс Manager. Унаследовавшись от BaseUserManager, мы получаем много того
же самого кода, который Django использовал для создания User (для демонстрации).
"""

class UserManager(BaseUserManager):

    def create_user(self,first_name, last_name, username, email, password=None):
        if username is  None:
            raise TypeError("Пользователь должен иметь свой никнейм!")

        if email is None:
            raise TypeError("Пользователь должен иметь адресс электронной почты!")


        user = self.model(username=username,first_name=first_name, last_name=last_name, email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user


    """ Создает и возввращет пользователя с привилегиями суперадмина. """
    def create_superuser(self, username, email, password):
        
        if password is None:
            raise TypeError("Суперпользователь не может не содержать пароля!")

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()


        return user