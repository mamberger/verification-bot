{% extends 'common/base.tpl' %}
{% block title %}
    Заявка #{{ account.id }}
{% endblock %}

{% block head %}
    {% load static %}
    <link rel="stylesheet" href="{% static 'css/detail_account.css' %}" />
{% endblock %}
<link href="{% static 'css/bootstrap.min.css' %}" rel="stylesheet">

{% block content %}
    {% include 'common/header.tpl' %}
    <div class="container">
        {% if account.get_multiaccount_status %}
            <div class="alert alert-danger">
                <b>
                    Подозрение!
                </b>
                <br />
                Данная заявка похожа на остальные 
                {% if account.get_multiaccount_status.first_last_field == "True" %}
                    именем и фамилией!
                {% elif account.get_multiaccount_status.credit_card_field == "True" %}
                    банковской картой!
                {% endif %}
                <br />
                <b>
                    Похожие заявки:
                </b>
                {% for similar_account in account.get_multiaccount_status.get_similar_accounts %}
                    {% if forloop.last %}
                        
                    {% else %}
                        <a href="/accounts/view/{{ similar_account.id }}">
                            Заявка №{{ similar_account.id }}
                        </a>
                    {% endif %}
                {% endfor %}
            </div>
        {% endif %}
        
        <h3>
            {% comment %}Данные о {% if account.status == "ref_account:1" %} реферальной {% endif %}заявке #{{account.id}}
            {% endcomment %}
            Заявка {{ account.id }} - {{ account.first_name }} {{ account.last_name }}
        </h3>{% comment %}
        <p class="text-muted">
            Была добавлена: 
            {{ account.get_datetime_object.day }}-{{ account.get_datetime_object.month }}-{{ account.get_datetime_object.year }} | {{ account.get_datetime_object.hour }}:{{ account.get_datetime_object.minute }}
        </p>{% endcomment%}
        {% comment %}
        <a href="/accounts/setbalance/{{ account.id }}">
            <button class="btn btn-success">
                Установить баланс
            </button>
        </a>
        {% if user.get_group == "Администратор" %}
            <a href="/accounts/delete/{{ account.id }}">
                <button class="btn btn-danger">
                    Удалить
                </button>
            </a>
            <a href="/accounts/banlist/add/{{ account.id }}">
                <button class="btn btn-danger">
                    Забанить
                </button>
            </a>
        {% endif %}{% endcomment %}
        <br />

        {% if account.status == "ref_account:1" %}
            <div id="list-params" class="row">
                <div class="col-md-6">
                    <ul class="list-group">
                        <li class="list-group-item">
                            <a href="https://t.me/{{ account.tg_username }}" target="_blank">
                                @{{account.tg_username}}
                            </a>
                        </li>
                        <li class="list-group-item">
                            <b>Имя: </b> {{ account.first_name }}
                        </li>
                         <li class="list-group-item">
                            <b>Фамилия: </b> {{ account.last_name }}
                        </li>

                         <li class="list-group-item">
                            <b>Баланс: </b> {{ account.balance }}
                        </li>
                    </ul>
                </div>
                <div class="col-md-6">
                    <ul class="list-group">
                        <li class="list-group-item">
                            <b>Всего привёл: </b>
                            {{ count_referals_by_account }}
                        </li>
                        <li class="list-group-item">
                            <b>Реферальная ссылка: </b>
                            <a href="https://{{ blank_referals }}{{account.tg_id}}">
                                {{ blank_referals }}{{account.tg_id}}
                            </a>
                        </li>
                    </ul> 
                </div>
            </div>
        {% else %}
        <div id="list-params" class="row">
            <div class="col-md-6">
               <ul class="list-group">
                    <li class="list-group-item">
                        <b>Телеграм ник и имя:</b>
                        <a href="https://t.me/{{ account.tg_username }}" target="_blank">
                             @{{account.tg_username}} {{ account.first_name}}
                        </a>
                    </li>
                     <li class="list-group-item">
                        <b>Имя:</b> {{ account.first_name }}
                    </li>
                    <li class="list-group-item">
                        <b>Отчество:</b> {{ account.patronymic }}
                    </li>
                    <li class="list-group-item">
                        <b>Фамилия:</b> {{ account.last_name }}
                    </li>
                    <li class="list-group-item">
                        <b>Страна:</b> {{ account.country }}
                    </li>
                    <li class="list-group-item">
                        <b>Область:</b> {{ account.region }}
                    </li>
                    <li class="list-group-item">
                        <b>Город:</b> {{ account.city }}
                    </li>
                    <li class="list-group-item">
                        <b>Адресс:</b> {{ account.address }}
                    </li>
                    <li class="list-group-item">
                        <b>Дата рождения:</b> {{ account.date_birthday }}
                    </li>
                    <li class="list-group-item">
                        <b>Документ:</b> {{ account.document_type }}
                    </li>
                    
                </ul>
                <br />
                 <ul class="list-group">
                    <li class="list-group-item">
                        {% comment %}<b> Фото паспорта </b>{% endcomment %}
                        <hr />
                        {% if passportfile %}
                            <img width="400" height="300" src="/{{ passportfile.path }}" />
                            <br />
                            <br />
                        {% else %}
                            Фото ещё не было загружено.
                        {% endif %}
                    </li>
                </ul>
            </div>

            <div class="col-md-6">
                <div class="custom_button_group">
                    <button type="button" class="btn btn-outline-dark" onclick="myFunction()">
                        <img src="{% static 'admin/img/copy.png' %}" width="20" height="15" alt="" style="vertical-align:middle">
                        Копировать
                    </button>
                    <button type="button" class="btn btn-outline-dark" {%if account.chat_link %}onclick="openNewWin('{{ account.chat_link }}')"{% endif %}>
                        <img src="{% static 'admin/img/chat.png' %}" width="20" height="15" alt="" style="vertical-align:middle">
                        Чат
                    </button>
                    <button type="button" class="btn btn-outline-danger" data-bs-toggle="modal" data-bs-target="#exampleModal">
                        <img src="{% static 'admin/img/delete.png' %}" width="20" height="15" alt="" style="vertical-align:middle">
                        Удалить
                    </button>
                </div>
                <br>
                <ul class="list-group">
                    <li class="list-group-item">
                        <b>Статус:</b> {{ account.new_status }}<br>
                        <div class="dropdown">
                          <button class="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton1" data-bs-toggle="dropdown" aria-expanded="false">
                            Изменить статус
                          </button>
                          <ul class="dropdown-menu" aria-labelledby="dropdownMenuButton1">
                            <li><a class="dropdown-item" href="/accounts/change__status/{{ account.pk }}/Входящая/1">Входящяя</a></li>
                            <li><a class="dropdown-item" href="/accounts/change__status/{{ account.pk }}/Принята/1">Принята</a></li>
                            <li><a class="dropdown-item" href="/accounts/change__status/{{ account.pk }}/Отклонена/1">Отклонена</a></li>
                            <li><a class="dropdown-item" href="/accounts/change__status/{{ account.pk }}/Одобрена/1">Одобрена</a></li>
                            <li><a class="dropdown-item" href="/accounts/change__status/{{ account.pk }}/Выплачена/1">Выплачена</a></li>
                          </ul>
                        </div>
                    </li>
                    <li class="list-group-item">
                        <b>Время создания:</b> {{ account.get_datetime_object.day }}-{{ account.get_datetime_object.month }}-{{ account.get_datetime_object.year }} {{ account.get_datetime_object.hour }}:{{ account.get_datetime_object.minute }}

                    </li>
                    <li class="list-group-item">
                        <b>Стоимость заявки:</b> {{ account.type_payment }}
                    </li>
                    <li class="list-group-item">
                        <b>Регистратор:</b> {{ account.worker }}
                    </li>
                    {% comment %}<li class="list-group-item">
                        <b>Реквизиты:</b> {{ account.credit_card }}
                    </li>{% endcomment %}
                    {% comment %}<li class="list-group-item">
                        <b>Баланс:</b> {{ account.balance }}
                    </li>{% endcomment %}
                     <li class="list-group-item">
                        <b>Реферал:</b> 
                        {% if referal_username == "нет" %}
                            Не имеется
                        {% else %}
                            <a href="https://t.me/{{ referal_username }}" target="_blank">
                                @{{ referal_username }}
                            </a>
                        {% endif %}
                    </li>
                    {% comment %}<li class="list-group-item">
                        <b>Статус:</b> {% if status|length != 0 %} {{ status.0.status  }}  {% else %} Не принят {% endif %}
                    </li>{% endcomment %}
                    {% comment %}{% if status|length != 0 %}
                        <li class="list-group-item">
                            <b>Регистратор:</b> 
                            <a href="https://t.me/@{{ status.0.get_registrator_username }}" target="_blank">
                                {{ status.0.get_registrator_username }}
                            </a>
                        </li>
                    {% endif %}{% endcomment %}
                    {% if account.status == "drop" or account.status == "drop_done" %}
                        <li class="list-group-item">
                            <b>Дроповод: </b>
                            <a href="https://t.me/{{ account.get_drop_user.username }}" target="_blank">
                                @{{ account.get_drop_user.username }}
                            </a>
                        </li>
                    {% endif %}
                    <li class="list-group-item">
                        <b>Реферальный платеж:</b>
                    </li>
                    <li class="list-group-item">
                        <div class="form-group">
                            <form method="post">
                                <label>
                                <b>Комментарий: </b>
                                </label>
                                <br>
                                <textarea name="account_comment" class="form-control" rows='7' required>{% if account.comment is None%}{% else %}{{ account.comment }}{% endif %}</textarea><br>
                                <button type="submit" class="btn btn-secondary">Сохранить комментарий</button>
                            </form>
                        </div>
                    </li>
                </ul>
                <br />
                {% comment %}{% if user.get_group != "Дроповод" %}
                <ul class="list-group">
                    <li class="list-group-item">
                        <form action="" method="POST">
                            <div class="form-group">
                                <label>
                                    <b>Ссылка: </b>
                                </label>
                                <input name="link" {% if account.status == "1" or account.status == "drop_done" %} disabled value="{{ status.0.link }}" {% endif %} class="form-control" required/>
                            </div>
                            <div class="form-group">
                                <label>
                                    <b>Инструкция: </b>
                                </label>
                                <textarea {% if account.status == "1" or account.status == "drop_done" %} disabled{% endif %} name="instruction" class="form-control" required>
                                    {% if account.status == "1" %}
                                        {{ status.0.instruction }}
                                    {% endif %}
                                </textarea>
                            </div>
                            {% if account.status == "1" or account.status == "drop_done" %}
                                <small>
                                    Заявка уже была принята
                                </small>
                                <br />
                            {% endif %}
                            <button class="btn btn-success" type="submit" {% if account.status == "1" or passportfile == None or account.status == "drop_done"%} disabled{% endif %} >
                                Принять
                            </button>
                            <br />
                            {% if passportfile == None %}
                                <small>Заявка не может быть принята без верификации паспорта!</small>
                            {% endif %}
                        </form>
                    </li>
                </ul>
                {% endif %}
                {% endcomment %}

            </div>
        </div>
        {% endif %}
    </div>

    <div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
      <div class="modal-dialog modal-sm">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="exampleModalLabel">Удаление заявки {{account.id}}</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            Заявка {{account.id}} от {{account.tg_username}} будет удалена навсегда.
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Отмена</button>
            <button type="button" class="btn btn-danger" onclick="window.location.href = '/accounts/view/delete__account/{{account.id}}';">Подтверждаю</button>
          </div>
        </div>
      </div>
    </div>
{% endblock%}

<!-- Ниже скрипт для копирования данных о заявке в буфер. Онклик висит на кнопке скопировать -->
<!-- Ещё Ниже скрипт для модального окна (подтверждение при удалении заявки) -->
{% block scripts %}
<script>
  function myFunction() {
      navigator.clipboard.writeText('{{ account.id }}\n{{ account.first_name }}\n{{ account.patronymic }}\n{{ account.last_name }}\n{{account.country}}\n{{account.region}}\n{{account.city}}\n{{account.address}}\n{{account.date_birthday}}\n{{account.document_type}}\n{{account.tg_username}}\n{{account.get_drop_user}}');
}
</script>
<script>
var myModal = document.getElementById('myModal')
var myInput = document.getElementById('myInput')

myModal.addEventListener('shown.bs.modal', function () {
  myInput.focus()
})

</script>
<script language="JavaScript">
<!-- hide
function openNewWin(url) {
  myWin= open(url);
}
// -->
</script>
{% endblock scripts %}

