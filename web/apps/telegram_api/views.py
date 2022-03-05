from django.http import HttpResponse
from django.shortcuts import render


def show_ftp(request):
    return render(request, 'telegram_api/ftp.tpl')