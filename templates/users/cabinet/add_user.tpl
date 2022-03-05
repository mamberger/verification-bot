{% extends 'common/base.tpl' %}

{% block title %} 
    Добавить сотрудника
{% endblock %}

{% block content %}
    {% include 'common/header.tpl' %}
    <div class="container">
        <h3>
            Добавить сотрудника
        </h3>
        <hr />
        {% if error %}
            <div class="alert alert-danger">
                {{ error }}
            </div>
        {% endif %}
        <form action="/form/user/add" method="POST">
            <div class="row">
                <div class="col-md-6">
                    <div class="form-group">
                        <label>Имя</label>
                        <input name="first_name" class="form-control" placeholder="Иван" required/>
                    </div>
                    <div class="form-group">
                        <label>Фамилия</label>
                        <input name="last_name" class="form-control" placeholder="Пупкин" required/>
                    </div>
                    <div class="form-group">
                        <label>Почта</label>
                        <input type="email" name="email" class="form-control" placeholder="ivanpupkin@mail.ru" required/>
                    </div>
            </div>
            <div class="col-md-6">
                <div class="form-group">
                    <label>
                        Телеграм ник
                    </label>
                    <input name="username" class="form-control" placeholder="vasypupkin" required/>
                </div>
                <div class="form-group">
                    <label>
                        Роль
                    </label>
                    <select name="group" class="form-control">
                        <option value="Регистратор">Регистратор</option>
                        <option value="Администратор">Администратор</option>
                        <option value="Дроповод">Дроповод</option>
                    </select>
                </div>
                 <div class="form-group">
                    <label>
                        Пароль
                    </label>
                    <input name="password" class="form-control" required/>
                </div>
            </div>
            </div>
            <button type="submit" class="btn btn-success">Добавить</button>
        </form>
    </div>
{% endblock %}