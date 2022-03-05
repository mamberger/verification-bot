{% extends 'common/base.tpl' %}

{% block title %}
    Личный кабинет 
{% endblock %}

{% block content %}
    {% include 'common/header.tpl' %}
    <div class="container">
        <h2>
            {{ user.first_name }} {{ user.last_name }}
        </h2>
        <p>
            {{ user.get_group }}
        </p>

        <br />

        <h2>
            Статистика
        </h2>
        <hr />
        <h4 align="center"></h4>
            {% if user.get_group == "Администратор" %}
                <div class="row">
                    <div class="col-md-4">
                        <div class="card">
                            <div class="card-body">
                                <h5 class="card-title">Всего заявок</h5>
                                <hr />
                                <h6 class="card-subtitle md-2 text-muted">
                                    Кол-во заявок в настоящий момент:
                                </h6>
                                {{ all_accounts_count }}
                            </div>
                        </div>
                    </div>
                     <div class="col-md-4">
                        <div class="card">
                            <div class="card-body">
                                <h5 class="card-title">Всего принятых заявок</h5>
                                <hr />
                                <h6 class="card-subtitle md-2 text-muted">
                                    Кол-во принятых заявок:
                                </h6>
                                {{ completed_accounts_count }}
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="card">
                            <div class="card-body">
                                <h5 class="card-title">Всего сотрудников</h5>
                                <hr />
                                <h6 class="card-subtitle md-2 text-muted">
                                    Кол-во сотрудников:
                                </h6>
                                {{ all_users_count }}
                            </div>
                        </div>
                    </div>
                </div>
                <h2>
                    Сегодня
                </h2>
                <hr />
                <div class="row">
                     <div class="col-md-4">
                        <div class="card">
                            <div class="card-body">
                                <h5 class="card-title">Принято заявок</h5>
                                <hr />
                                <h6 class="card-subtitle md-2 text-muted">
                                    Принято заявок за сегодня:
                                </h6>
                                {{ today_completed_accounts_count }}
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="card">
                            <div class="card-body">
                                <h5 class="card-title">За вчера</h5>
                                <hr />
                                <h6 class="card-subtitle md-2 text-muted">
                                    Принято заявок за вчера:
                                </h6>
                                {{ yesterday_completed_accounts_count }}
                            </div>
                        </div>
                    </div>
                </div>
                <br />
                
                <h2>
                    Регистраторы
                </h2>
                <hr />
                <div class="row">
                    {% for registrator in registrator_completed_accounts %}
                        <div class="col-md-4">
                            <div class="card">
                                <div class="card-body">
                                    <h5 class="card-title">
                                        <a href="https://t.me/{{ registrator.tg_username }}">
                                            @{{ registrator.tg_username }}
                                        </a>
                                    </h5>
                                    <hr />
                                    <h6 class="card-subtitle md-2 text-muted">
                                        Выполнено заявок:
                                    </h6>
                                    {{ registrator.count }}
                                </div>
                            </div>
                        </div>
                    {% endfor %}
                </div>
                <br />
                
                <h2>
                    Дроповоды
                </h2>
                <hr />
                <div class="row">
                    {% for drop_user in drop_users %}
                        <div class="col-md-4">
                            <div class="card">
                                <div class="card-body">
                                    <h5 class="card-title">
                                        <a href="https://t.me/{{ droup_user.tg_username }}">
                                            @{{ drop_user.tg_username }}
                                        </a>
                                    </h5>
                                    <hr />
                                    <h6 class="card-subtitle text-muted md-2">
                                        Добавил заявок: 
                                    </h6>
                                    {{ drop_user.count }}
                                </div>
                            </div>
                        </div>
                    {% endfor %}
                </div>
                <br />
                <h2>
                    Администраторы
                </h2>
                <hr />
                <div class="row">
                    {% for admin_user in admin_users %}
                        <div class="col-md-4">
                            <div class="card">
                                <div class="card-body">
                                    <h5 class="card-title">
                                        <a href="https://t.me/{{ admin_user.tg_username }}">
                                            @{{ admin_user.tg_username }}
                                        </a>
                                    </h5>
                                    <hr />
                                    <h6 class="card-subtitle text-muted md-2">
                                        Принятых заявок: {{ admin_user.count }}
                                    </h6>
                                </div>
                            </div>
                        </div>
                    {% endfor %}
                </div>
                
        
            {% elif user.get_group == "Регистратор" %}
                <div class="row">
                    <div class="col-md-4">
                        <div class="card">
                            <div class="card-body">
                                <h5 class="card-title">
                                    Не принятых заявок
                                </h5>
                                <hr />
                                <h6 class="card-subtitle md-2 text-muted">
                                    Заявок не принятых: 
                                </h6>
                                {{ count_not_completed_accounts }} 
                        </div>
                    </div>
                    </div>
                    <div class="col-md-4">
                        <div class="card">
                            <div class="card-body">
                                <h5 class="card-title">
                                    Ваших принятых заявок
                                </h5>
                                <hr />
                                <h6 class="card-subtitle md-2 text-muted">
                                    Вы приняли: 
                                </h6>
                                {{ count_registrator_completed_accounts }} 
                        </div>
                    </div>
                    </div>
                    
                </div>
                <br />
                <h2>Ваши принятые заявки</h2>
                <hr />
                <table class="table table-light bg-light">
                    <thead>
                        <tr>
                            <th scope="col">#</th>
                            <th scope="col">Ник</th>
                            <th scope="col">Имя</th>
                            <th scope="col">Фамилия</th>
                            <th scope="col">Вид оплаты</th>
                            <th scope="col">Принята</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for account in registator_accounts %}
                            <tr>
                                <th scope="row">
                                    <a href="/accounts/view/{{ account.get_account.id }}">
                                        {{ account.get_account.id }}
                                    </a>
                                </th>
                                <td>
                                    <a href="https://t.me/{{ account.get_account.tg_username }}">
                                        @{{ account.get_account.tg_username }}
                                    </a>
                                </td>
                                <td>{{ account.get_account.first_name }}</td>
                                <td>{{ account.get_account.last_name }}</td>
                                <td>{{ account.get_account.type_payment }}</td>
                                <td>{{ account.get_account.get_completed_datetime }}</td>
                            </tr>
                        {% endfor%}
                    </tbody>
                </table>
            
            {% elif user.get_group == "Дроповод" %}
                <div class="row">
                    <div class="col-md-6">
                        <div class="card">
                            <div class="card-body">
                                <h5 class="card-title">
                                    Всего ваших заявок:
                                </h5>
                                <hr />
                                <h6 class="card-subtitle md-2 text-muted">
                                    Количество добавленных заявок:
                                </h6>
                                {{ count_drop_accounts }}
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="card">
                            <div class="card-body">
                                <h5 class="card-title">
                                    Всего принятых заявок
                                </h5>
                                <hr />
                                <h6 class="card-subtitle md-2 text-muted">
                                    Количество принятых ваших заявок:
                                </h6>
                                {{ count_completed_drop_accounts }}
                            </div>
                        </div>
                    </div>
                </div>
                <br />
                <h2>
                    Ваши заявки
                </h2>
                <hr />
                <table class="table table-light bg-light">
                    <thead>
                        <tr>
                            <th scope="col">#</th>
                            <th scope="col">Имя</th>
                            <th scope="col">Фамилия</th>
                            <th scope="col">Документ</th>
                            <th scope="col">Тип оплаты(грн.)</th>
                            <th scope="col">Статус</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for account in drop_accounts%}
                            <tr>
                                <th scope="row">
                                    <a href="/accounts/view/{{ account.get_account.id }}">
                                        {{ account.get_account.id }}
                                    </a>
                                </th>
                                <td>{{ account.get_account.first_name }}</td>
                                <td>{{ account.get_account.last_name }}</td>
                                <td>{{ account.get_account.document_type }}</td>
                                <td>{{ account.get_account.type_payment }}</td>
                                <td>
                                    {% if account.get_account.status == "drop_done" %}
                                        <p class="text-success">
                                            принят
                                        </p>
                                    {% else%}
                                        <p class="text-primary">
                                            в процессе
                                        </p>
                                    {% endif %}
                                </td>
                            </tr>
                        {% endfor %}
                    </tbody>
                </table>
            {% endif %}
        </h4>
    </div>
{% endblock %}