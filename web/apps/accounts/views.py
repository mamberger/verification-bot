from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from accounts.models import Accounts, Completed, Mailing, PassportFile, MultiAccounts, DropAccount, BanList
from referals.models import Referals
from telegram_api.app import send_message
from config import blank_referals
from .mixins import change_status_func


@login_required
def new_all_view(request, show_type):
    if show_type == 'all' or show_type == 'incoming':
        queryset = Accounts.objects.filter(new_status='Входящая')
    elif show_type == 'my':
        queryset = Accounts.objects.filter(worker=request.user)
    elif show_type == 'accepted':
        queryset = Accounts.objects.filter(new_status='Одобрена')
    elif show_type == 'active':
        queryset = Accounts.objects.filter(Q(new_status='Входящая') | Q(new_status='Принята') | Q(new_status='Одобрена'))
    elif show_type == 'archive':
        queryset = Accounts.objects.filter(Q(new_status='Отклонена') | Q(new_status='Выплачена'))
    else:
        return HttpResponse(f'accounts.views Error: Unknown show_type "{show_type}". Line: 14')
    return render(request, "users/cabinet/accounts/show.tpl", {"accounts": queryset, "show_type": show_type})

# старая вьюха для показа страницы с заявками
@login_required
def all_view(request, show_type):
    if show_type == "all":
        if request.user.get_group() == "Администратор":
            get_all_objects = Accounts.objects.all().order_by('-id')
            return render(request, "users/cabinet/accounts/show.tpl", {"accounts": get_all_objects})
        
        else: 
            return redirect("/accounts/my")

    elif show_type == "my":
        get_my_completed = Completed.objects.filter(registrator_id = request.user.id).order_by('-id')
        my_accounts = list()
        for completed_account in get_my_completed:
            my_accounts.append(completed_account.account_id)
        return render(request, "users/cabinet/accounts/show.tpl", {"accounts": my_accounts})

    elif show_type == "new":
        get_new_accounts = Accounts.objects.filter(status="None").order_by('-id') | Accounts.objects.filter(status="drop").order_by("-id")
        return render(request, "users/cabinet/accounts/show.tpl", {"accounts": get_new_accounts})

    elif show_type == "completed":
        get_completed_accounts = Accounts.objects.filter(status=1).order_by('-id') | Accounts.objects.filter(status="drop_done").order_by("-id")
        return render(request, "users/cabinet/accounts/show.tpl", {"accounts": get_completed_accounts})

    elif show_type == "banlist":
        get_banned_accounts = BanList.objects.all()
        return render(request, "users/cabinet/accounts/banlist.tpl", {"get_banned_accounts": get_banned_accounts})
    else:
        return HttpResponse('Server Error')


@login_required
def detail_view(request, account_id):
    if request.method == "POST":
        select_account = Accounts.objects.get(id=account_id)
        comment = request.POST['account_comment']
        select_account.comment = comment
        select_account.save()
        # if select_account.status == "drop":
        #     select_account.status = "drop_done"
        # else:
        #     select_account.status = 1
        # select_account.save()
        #
        # new_completed = Completed.objects.create(
        #     registrator_id = request.user,
        #     account_id = select_account,
        #     status = "Принят",
        #     link = request.POST['link'],
        #     instruction = request.POST['instruction']
        # )
        #
        # content_message_invite = f"Вашу заявку принял @{request.user.username}. \n Вы можете обращяться к нему если возникнут вопросы."
        # send_message(account_id = select_account.id, text=content_message_invite)
        #
        # content_message_instructions = f"*Перейдите по ссылке:* [перейти...]({request.POST['link']}) \n*Инструкция*: \n{request.POST['instruction']}"
        # send_message(account_id = select_account.id, text = content_message_instructions)

        return redirect("/accounts/view/"+str(select_account.id))


    if request.user.get_group() == "Администратор":
        try:
            referal_username = None
            account_detail = Accounts.objects.get(id=account_id) 
            try:
                referal_object = Referals.objects.get(to_id=account_detail.tg_id)
                referal_tg_id = referal_object.from_id
                referal_account = Accounts.objects.get(tg_id=referal_tg_id)
                referal_username = referal_account.tg_username
            except:
                referal_username = "нет"
            
            get_status = Completed.objects.filter(account_id=account_id)
            try:
                if account_detail.status == "drop" or account_detail.status == "drop_done":
                    get_passport_file = PassportFile.objects.get(tg_id=account_detail.id)
                else:
                    get_passport_file = PassportFile.objects.get(tg_id=account_detail.tg_id)

            except Exception as e:
                print(e)
                get_passport_file = None

            if account_detail.status == "ref_account:1":
                try:
                    get_referals_by_account = Referals.objects.filter(from_id=account_detail.tg_id)
                    count_referals_by_account = len(get_referals_by_account)
                except:
                    get_referals_by_account = None




            return render(request, "users/cabinet/accounts/detail.tpl", {"user":request.user, "account": account_detail, "referal_username": referal_username, "status": get_status, "passportfile": get_passport_file, "blank_referals": blank_referals})
        except Exception as e:
            print(e)
            return HttpResponse("Заявки не найдено!")
    
    elif request.user.get_group() == "Регистратор":
        try:
            check_completed = Completed.objects.get(account_id = account_id)

            if check_completed.registrator_id.id == request.user.id:
                try:
                    referal_username = None
                    account_detail = Accounts.objects.get(id=account_id) 
                    try:
                        referal_object = Referals.objects.get(to_id=account_detail.tg_id)
                        referal_tg_id = referal_object.from_id
                        referal_account = Accounts.objects.get(tg_id=referal_tg_id)
                        referal_username = referal_account.tg_username
                    except:
                        referal_username = "нет"
                    
                    get_status = Completed.objects.filter(account_id=account_id)
                    try:
                        if account_detail.status == "drop" or account_detail.status == "drop_done":
                            get_passport_file = PassportFile.objects.get(tg_id=account_detail.id)
                        else:
                            get_passport_file = PassportFile.objects.get(tg_id=account_detail.tg_id)
        
                    except Exception as e:
                        print(e)
                        get_passport_file = None

                    print("passportfile: ", get_passport_file)
                    return render(request, "users/cabinet/accounts/detail.tpl", {"user":request.user, "account": account_detail, "referal_username": referal_username, "status": get_status, "passportfile": get_passport_file, "blank_referals": blank_referals})
                except Exception as e:
                    print(e)
                    return HttpResponse("Заявки не найдено!")
            else:
                return redirect("/accounts/new/")
        except:
            try:
                referal_username = None
                account_detail = Accounts.objects.get(id=account_id) 
                try:
                    referal_object = Referals.objects.get(to_id=account_detail.tg_id)
                    referal_tg_id = referal_object.from_id
                    referal_account = Accounts.objects.get(tg_id=referal_tg_id)
                    referal_username = referal_account.tg_username
                except:
                    referal_username = "нет"
                
                get_status = Completed.objects.filter(account_id=account_id)
                
                try:
                    if account_detail.status == "drop" or account_detail.status == "drop_done":
                        get_passport_file = PassportFile.objects.get(tg_id=account_detail.id)
                    else:
                        get_passport_file = PassportFile.objects.get(tg_id=account_detail.tg_id)
    
                except Exception as e:
                    print(e)
                    get_passport_file = None

                print("passportfile: ", get_passport_file)
                return render(request, "users/cabinet/accounts/detail.tpl", {"user":request.user, "account": account_detail, "referal_username": referal_username, "status": get_status, "passportfile": get_passport_file, "blank_referals": blank_referals})
            except Exception as e:
                print(e)
                return HttpResponse("Заявки не найдено!")

    elif request.user.get_group() == "Дроповод":
        try:
            check_completed = DropAccount.objects.get(account_id = account_id)

            if check_completed.drop_user_id.id == request.user.id:
                try:
                    referal_username = None
                    account_detail = Accounts.objects.get(id=account_id) 
                    try:
                        referal_object = Referals.objects.get(to_id=account_detail.tg_id)
                        referal_tg_id = referal_object.from_id
                        referal_account = Accounts.objects.get(tg_id=referal_tg_id)
                        referal_username = referal_account.tg_username
                    except:
                        referal_username = "нет"
                    
                    get_status = Completed.objects.filter(account_id=account_id)
                    try:
                        if account_detail.status == "drop" or account_detail.status == "drop_done":
                            get_passport_file = PassportFile.objects.get(tg_id=account_detail.id)
                        else:
                            get_passport_file = PassportFile.objects.get(tg_id=account_detail.tg_id)
        
                    except Exception as e:
                        print(e)
                        get_passport_file = None

                    print("passportfile: ", get_passport_file)
                    return render(request, "users/cabinet/accounts/detail.tpl", {"user":request.user, "account": account_detail, "referal_username": referal_username, "status": get_status, "passportfile": get_passport_file, "blank_referals": blank_referals})
                except Exception as e:
                    print(e)
                    return HttpResponse("Заявки не найдено!")
            else:
                return redirect("/accounts/new/")
        except:
            try:
                referal_username = None
                account_detail = Accounts.objects.get(id=account_id) 
                try:
                    referal_object = Referals.objects.get(to_id=account_detail.tg_id)
                    referal_tg_id = referal_object.from_id
                    referal_account = Accounts.objects.get(tg_id=referal_tg_id)
                    referal_username = referal_account.tg_username
                except:
                    referal_username = "нет"
                
                get_status = Completed.objects.filter(account_id=account_id)
                
                try:
                    if account_detail.status == "drop" or account_detail.status == "drop_done":
                        get_passport_file = PassportFile.objects.get(tg_id=account_detail.id)
                    else:
                        get_passport_file = PassportFile.objects.get(tg_id=account_detail.tg_id)
    
                except Exception as e:
                    print(e)
                    get_passport_file = None

                print("passportfile: ", get_passport_file)
                return render(request, "users/cabinet/accounts/detail.tpl", {"user":request.user, "account": account_detail, "referal_username": referal_username, "status": get_status, "passportfile": get_passport_file, "blank_referals": blank_referals})
            except Exception as e:
                print(e)
                return HttpResponse("Заявки не найдено!")



@login_required
def delete_view(request, account_id):
    if request.user.get_group() == "Администратор":
        try:
            account_object = Accounts.objects.get(id=account_id)
            passportfile_object = None
            if account_object.status == "drop" or account_object.status == "drop_done":
                passportfile_object = PassportFile.objects.get(tg_id=account_object.id).delete()
                mailing_object = Mailing.objects.get(tg_id=account_object.id).delete()
                dropaccount_object = DropAccount.objects.get(account_id = account_object.id).delete()
            else:
                passportfile_object = PassportFile.objects.get(tg_id=account_object.tg_id).delete()
            try:
                referal_object = Referals.objects.get(to_id=account_object.tg_id).delete()
            except Exception as e:
                print(e)
            if account_object.status == "1":
                completed_object = Completed.objects.get(account_id=account_object.id).delete()
            
            print("ok")
            account_object.delete()
            mailing_object = Mailing.objects.get(tg_id=account_object.tg_id).delete()


        except Exception as e:
            print(e)
            return redirect("/accounts/all")
        
        get_all_objects = Accounts.objects.all()
        return redirect("/accounts/all")


@login_required
def take_view(request, account_id):
    return render(request, "users/cabinet/accounts/take.tpl")

@login_required
def setbalance_view(request, account_id):
    if request.method == "POST":
        account = Accounts.objects.get(id=account_id)
        account.balance = request.POST['balance']
        account.save()
        return redirect("/accounts/view/"+str(account_id))

    get_account = Accounts.objects.get(id=account_id)
    balance_account = get_account.balance
    return render(request, "users/cabinet/accounts/setbalance.tpl", {"balance_account": balance_account})

@login_required
def ban_add_view(request, account_id):
    if request.user.get_group() == "Администратор":
        account_detail = Accounts.objects.get(id=account_id)
        BanList.objects.create(
            tg_id = account_detail.tg_id,
            account_id = account_detail,
            admin = request.user,
            reason = "Мультиаккаунт"
        )
        return redirect('/accounts/banlist/')
    
    else:
        return redirect("/user")


@login_required
def change_status_view(request, account_id, status, detail):
    worker = request.user.id
    change_status_func(worker, account_id, status)
    if detail:
        return redirect(f'/accounts/view/{account_id}')
    else:
        return redirect(f'/accounts/all')

@login_required
def delete_account(request, account_id):
    if request.user.get_group() != "Администратор":
        return redirect(f'/accounts/view/{account_id}')
    target = Accounts.objects.get(pk=account_id)
    target.delete()
    return redirect('/accounts/all')
