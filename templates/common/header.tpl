{% load static %}
<link rel="stylesheet" href="{% static 'css/my.css' %}">
<style>
   .my_a {
    text-decoration: none; /* Убираем подчёркивание */
    color: black;
   }
   .my_a:active {
   color: 000#;
   }
</style>
<nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <div class="container">
        <a class="navbar-brand" href="/accounts/incoming">Admin</a>
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav">
            <li class="nav-item">
                <a class="nav-link" href="/user">
                    Статистика
                </a>
            </li>
            {% if request.user.get_group == "Регистратор" %}
                <li class="nav-item">
                    <a class="nav-link" href="/accounts/incoming">
                        Заявки
                    </a>
                </li>
            {% endif %}
            {% if request.user.get_group == "Администратор" %}
                <li class="nav-item">
                    <a class="nav-link" href="/accounts/incoming">
                        Заявки
                    </a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="/user/list">
                        Рефералы
                    </a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="/user/list">
                        Сотрудники
                    </a>
                </li>
                {% comment %}
                <li class="nav-item">
                    <a class="nav-link" href="/accounts/banlist">
                        Бан-лист
                    </a>
                </li>
                {% endcomment %}
            {% endif %}
            {% if request.user.get_group == "Дроповод" %}
                <li class="nav-item">
                    <a class="nav-link" href="/drop/create">
                        Создать заявку
                    </a>
                </li>
            {% endif %}
            {% comment %}
                <li class="nav-item">
                    <a class="nav-link" href="/user/logout">
                        Выйти
                    </a>
                </li>
            </ul>
            {% endcomment %}
        </div>
        <a href="/user/logout" class="logout_icon">
            <img src="{% static 'admin/img/logout.png' %}" width="33" height="33" alt="">
        </a>
    </div>
</nav>