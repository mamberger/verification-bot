{% extends 'common/base.tpl' %}

{% block title %}
    Список пользователей
{% endblock %}

{% block content %}
    {% include 'common/header.tpl' %}

    <div class="container">
        <h3>
            Список сотрудников
        </h3>
        <a href="/user/add">
            <button class="btn btn-success">
                Добавить
            </button>
        </a>
        <table class="table table-light bg-light table-hover">
            <thead>
                <tr>
                    <th scope="col">
                        #
                    </th>
                    <th scope="col">
                        Имя
                    </th>
                    <th scope="col">
                        Фамилия
                    </th>
                    <th scope="col">
                        Почта
                    </th>
                    <th scope="col">
                        Роль
                    </th>
                    <th scope="col">
                        Действия
                    </th>
                </tr>
            </thead>
            <tbody>
                {% for user in users %}
                    <tr>
                        <th scope="row">{{ user.id }}</th>
                        <td>{{ user.first_name }}</td>
                        <td>{{ user.last_name }}</td>
                        <td>{{ user.email }}</td>
                        <td>{{ user.get_group }}</td>
                        <td>
                            <a class="text-danger" href="/user/delete/{{user.id}}">Уволить</a>
                        </td>
                    </tr>
                {% endfor %}
            </tbody>
        </table>

    </div>
{% endblock %}
