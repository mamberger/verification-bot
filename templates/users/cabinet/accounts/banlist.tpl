{% extends "common/base.tpl" %}

{% block title %}Бан-лист{% endblock %}

{% block content %}
    {% include "common/header.tpl" %}
    <div class="container">
        <table class="table table-light bg-light">
            <thead>
                <th scope="col">#</th>
                <th scope="col">Telegram ID</th>
                <th scope="col">Администратор</th>
                <th scope="col">Причина</th>
            </thead>
            <tbody>
                {% for account in get_banned_accounts %}
                    <tr>
                        <td>{{ account.id }}</td>
                        <td>{{ account.tg_id }}</td>
                        <td>{{ account.admin.first_name }}</td>
                        <td>{{ account.reason }}</td>
                    </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
{% endblock %}