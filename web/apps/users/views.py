from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from datetime import datetime, timedelta

from django.shortcuts import render, redirect

from users.models import User
from accounts.models import Accounts, Completed, DropAccount

#from main import API_send_message

class LoginView(TemplateView):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("/user")
        else:
            return render(request, "users/login.tpl")


class CabinetView(LoginRequiredMixin, TemplateView):
    login_url = "/login"
    redirect_field_name = None
    
    def get(self, request):
        if request.user.get_group() == "Администратор":
            all_accounts_count = len(Accounts.objects.all())
            completed_accounts_count = len(Accounts.objects.filter(status="1"))
            completed_accounts = Completed.objects.all()
            all_users_count = len(User.objects.all())
            users = User.objects.all()

            registrator_accounts_count = list()
            admin_accounts_count = list()
            drop_accounts_count = list()
            for i in range(all_users_count):
                if users[i].get_group() == "Регистратор":
                    registrator_accounts_count.append(
                        {"id": users[i].id, "tg_username": users[i].username, "count": len(Completed.objects.filter(registrator_id=users[i].id)), "group": users[i].get_group()}
                    )
                
                elif users[i].get_group() == "Администратор":
                    admin_accounts_count.append(
                        {"id": users[i].id, "tg_username": users[i].username, "count": len(Completed.objects.filter(registrator_id=users[i].id)), "group": users[i].get_group()}
                    )
            
                elif users[i].get_group() == "Дроповод":
                    drop_accounts_count.append(
                        {"id": users[i].id, "tg_username": users[i].username, "count": len(DropAccount.objects.filter(drop_user_id=users[i].id)), "group": users[i].get_group()}
                    )
            
            
            now_date = datetime.now()
            today_completed_accounts_count = len(Completed.objects.filter(datetime__day=now_date.day, 
                        datetime__month=now_date.month, 
                        datetime__year=now_date.year))

            previous_day = (now_date - timedelta(days=1))
            yesterday_completed_accounts_count = len(Completed.objects.filter(datetime__day = previous_day.day, 
                    datetime__month=previous_day.month,
                    datetime__year=previous_day.year
            ))
            return render(request, "users/cabinet/index.tpl", {"user": request.user, 
                "all_accounts_count":all_accounts_count, 
                "completed_accounts_count": completed_accounts_count,
                "all_users_count": all_users_count,
                "registrator_completed_accounts": registrator_accounts_count,
                "admin_users": admin_accounts_count,
                "drop_users": drop_accounts_count,
                "today_completed_accounts_count": today_completed_accounts_count,
                "yesterday_completed_accounts_count": yesterday_completed_accounts_count
                 })

        elif request.user.get_group() == "Регистратор":
            count_not_completed_accounts = len(Accounts.objects.filter(status="None"))
            count_registrator_completed_accounts = len(Completed.objects.filter(registrator_id=request.user.id))

            registrator_accounts = Completed.objects.filter(registrator_id=request.user.id).order_by('-id')

            return render(request, "users/cabinet/index.tpl", 
            {
                "count_not_completed_accounts": count_not_completed_accounts,
                "count_registrator_completed_accounts": count_registrator_completed_accounts,
                "registator_accounts": registrator_accounts
            })

        elif request.user.get_group() == "Дроповод":
            drop_accounts = DropAccount.objects.filter(drop_user=request.user.id)
            count_completed_drop_accounts = 0
            for account in drop_accounts:
                if account.get_account().status == "drop_done":
                    count_completed_drop_accounts+=1
                else:
                    break

            return render(request, "users/cabinet/index.tpl", 
                {
                    "drop_accounts": drop_accounts,
                    "count_drop_accounts": len(drop_accounts),
                    "count_completed_drop_accounts": count_completed_drop_accounts
                }
            )

class ListView(LoginRequiredMixin, TemplateView):
    login_url = "/login"
    redirect_field_name = None
    template_name = "users/cabinet/show_all.tpl"

    def get(self, request):
        if request.user.get_group() == "Администратор":
            get_all_users = User.objects.all()
            return render(request, self.template_name, {"users": get_all_users})


class AddView(LoginRequiredMixin, TemplateView):
    login_url = "/login"
    redirect_field_name = None
    template_name = "users/cabinet/add_user.tpl"

    def get(self, request):
        if request.user.get_group() == "Администратор":
            return render(request, self.template_name)
    

def delete_user(request, user_id):
    if request.user.get_group() == "Администратор":
        try:
            User.objects.get(id = user_id).delete()
        
        except:
            pass
        return redirect("/user/list")
        