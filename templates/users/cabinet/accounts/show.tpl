{% extends 'common/base.tpl' %}
{% block title %}
    Список заявок
{% endblock %}
{% load static %}
<link rel="stylesheet" href="{% static 'css/my.css' %}">
{% block content %}
    {% include 'common/header.tpl' %}
    <div class="container">
        <h4>
            Заявки
        </h4>
        <div class="btn-group" role="group" aria-label="Basic radio toggle button group">
              <input type="radio" class="btn-check" onclick="window.location.href = '/accounts/incoming';" name="btnradio" id="btnradio1" autocomplete="off" {% if show_type == 'incoming'%}checked{% endif %}>
              <label class="btn btn-outline-dark" for="btnradio1">Входящие</label>
              {% if user.get_group == "Регистратор" %}
              <input type="radio" class="btn-check" onclick="window.location.href = '/accounts/my';" name="btnradio" id="btnradio2" autocomplete="off"{% if show_type == 'my'%}checked{% endif %}>
              <label class="btn btn-outline-dark" for="btnradio2">Мои</label>
              {% endif %}
              <input type="radio" class="btn-check" onclick="window.location.href = '/accounts/accepted';" name="btnradio" id="btnradio3" autocomplete="off"{% if show_type == 'accepted'%}checked{% endif %}>
              <label class="btn btn-outline-dark" for="btnradio3">Одобрено</label>

              <input type="radio" class="btn-check" onclick="window.location.href = '/accounts/active';" name="btnradio" id="btnradio4" autocomplete="off"{% if show_type == 'active'%}checked{% endif %}>
              <label class="btn btn-outline-dark" for="btnradio4">Активные</label>

              <input type="radio" class="btn-check" onclick="window.location.href = '/accounts/archive';" name="btnradio" id="btnradio5" autocomplete="off"{% if show_type == 'archive'%}checked{% endif %}>
              <label class="btn btn-outline-dark" for="btnradio5">Архив</label>
        </div>
        <div class="row">
            <div class="col-md-6">
                {% comment %}<p>
                    Статусы:
                    <small class="text-danger">
                        подозрение на мульти аккаунт
                    </small>
                    ;
                    <small class="text-success">
                        принято
                    </small>
                    ;
                    <small class="text-warning">
                        не загруженно фото
                    </small
                </p>{% endcomment %}
            </div>
        </div>
        
        <table class="table table-light table-hover">
            <thead>
                <tr>
                    <th scope="col">
                        №
                    </th>
                    <th scope="col">
                        Telegram
                    </th>
                    <th scope="col">
                        Имя
                    </th>
                    <th scope="col">
                        Фамилия
                    </th>
                    <th scope="col">
                        Статус
                    </th>
                    <th scope="col">
                        Создана
                    </th>
                    <th scope="col">
                        Регистратор
                    </th>
                     <th scope="col">
                        Действия
                    </th>
                </tr>
            </thead>
            <tbody>
                {% for account in accounts %}
                    {% comment %}<tr {% if account.new_status == 'Отклонена'%} class="table-danger"{% elif account.new_status == 'Принята' %}class="table-warning"{% elif account.new_status == 'Одобрена' %}class="table-primary"{% elif account.new_status == 'Выплачена' %}class="table-success"{% endif %}>{% endcomment %}
                    <tr {% if account.new_status == 'Входящая' %}class="table-warning"{% endif %}>
                    <td>{% if account.id is None %}-{% else %}{{ account.id }}{% endif %}</td>
                    <td><a href="https://t.me/{{ account.tg_username }}" target="_blank">
                             @{{account.tg_username}}</a>  {%if account.first_name%}{{ account.first_name}}{%else%}{%endif%}

                    </td>
                    <td>{% if account.first_name is None %}-{% else %}{{ account.first_name }}{% endif %}</td>
                    <td>{% if account.last_name is None %}-{% else %}{{ account.last_name }}{% endif %}</td>
                    <td>
                    <div class="dropdown">
                      <button class="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton1" data-bs-toggle="dropdown" aria-expanded="false">
                        {{ account.new_status }}
                      </button>
                      <ul class="dropdown-menu" aria-labelledby="dropdownMenuButton1">
                        <li><a class="dropdown-item" href="/accounts/change__status/{{ account.pk }}/Входящая/0">Входящяя</a></li>
                        <li><a class="dropdown-item" href="/accounts/change__status/{{ account.pk }}/Принята/0">Принята</a></li>
                        {% comment %}<li><a class="dropdown-item" href="/accounts/change__status/{{ account.pk }}/Отклонена/0">Отклонена</a></li>{% endcomment %}
                        {% comment %}<li><a class="dropdown-item" href="/accounts/change__status/{{ account.pk }}/Одобрена/0">Одобрена</a></li>{% endcomment %}
                        {% comment %}<li><a class="dropdown-item" href="/accounts/change__status/{{ account.pk }}/Выплачена/0">Выплачена</a></li>{% endcomment %}
                      </ul>
                    </div>
                    </td>
                    <td>{{ account.get_datetime_object.day }}-{{ account.get_datetime_object.month }}-{{ account.get_datetime_object.year }} {{ account.get_datetime_object.hour }}:{{ account.get_datetime_object.minute }}</td>
                    <td>{% if account.worker is None %}-{% else %}{{ account.worker }}{% endif %}</td>
                    <td>
                        <div class="btn-group">
                          <a {%if account.chat_link %}href="{{ account.chat_link }}" target="_blank" {%else%}{%endif%} target="_blank" class="btn btn-outline-dark">
                            <img src="{% static 'admin/img/chat_accounts.png' %}" width="20" height="20" class="account_icon" alt="">
                          </a>
                          <a href="/accounts/view/{{ account.id }}" class="btn btn-outline-dark">
                            <img src="{% static 'admin/img/info.png' %}" width="20" height="20" class="account_icon" alt="">
                          </a>
                        </div>
                    </td>
                    {% comment %}
                    {% if account.get_multiaccount_status != None %} class="table-danger" {% endif %}
                    {% if account.get_passport_file_status == None and account.status != "ref_account:1" and account.status != "ref_account:-1" and account.status != "drop" and account.status != "drop_done" %} class="table-warning" {% endif%}
                    {% if account.status == '1' or account.status == "drop_done" %} class="table-success" {% endif %}
                    >
                        <td>
                            <small>
                                {% if account.status == "drop" or account.status == "drop_done" %}
                                    {{ account.get_drop_datetime }}
                                {% else %}
                                    {{ account.get_datetime }}
                                {% endif %}
                            </small>
                        </td>
                        <th scope="row"> {{ account.id }}</th>
                        <td>
                            <a href="https://t.me/{{ account.tg_username }}" target="_blank">
                                @{{ account.tg_username }}
                            </a>
                        </td>
                        {% if account.status == "None" or account.status == "1" %}
                            <td>{{ account.first_name }}</td>
                            <td>{{ account.last_name }}</td>
                            <td>{{ account.document_type }}</td>
                            <td>{{ account.type_payment }}</td>
                            <td>
                                <a href="/accounts/view/{{ account.id }}">
                                    Подробнее
                                </a>
                            </td>
                        {% elif account.status == "-1" %}
                            <td>
                                <p class="text-warning">
                                    в процессе
                                </p>
                            </td>
                            <td></td>
                            <td></td>
                            <td></td>
                            <td>
                                <a href="/accounts/delete/{{ account.id }}" class="text-danger">
                                    <p class="text-danger">Удалить</a>
                                </a>
                            </td>
                        {% elif account.status == "ref_account:1" %}
                            <td>{{ account.first_name }}</td>
                            <td>{{ account.last_name }}</td>
                            <td>
                                <p class="text-primary">
                                    Реферальная заявка
                                </p>
                                <td></td>
                                <td>
                                    <a href="/accounts/view/{{ account.id }}">
                                        Подробнее
                                    </a>
                                </td>

                            </td>
                        {% elif account.status == "ref_account:-1" %}
                            <td>
                            <p class="text-primary">
                                Реферальная заявка <span class="text-warning">(в процессе)</span>
                            </p>
                            </td>
                            <td></td>
                            <td>
                            </td>

                            </td>
                        {% elif account.status == "drop" or account.status == "drop_done" %}
                            <td>{{ account.first_name }}</td>
                            <td>{{ account.last_name }}</td>
                            <td>{{ account.document_type }}</td>
                            <td>{{ account.type_payment }}</td>
                            <td>
                                <a href="/accounts/view/{{ account.id }}">
                                    Подробнее
                                </a>
                            </a>
                            
                        {% endif %}
                    {% endcomment %}
                    </tr>
                {% endfor %}




            </tbody>

        </table>
    </div>

{% endblock %}
