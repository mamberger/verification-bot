{% extends 'common/base.tpl' %}
{% block title %}Создать заявку{% endblock %}


{% block content %}
    {% include "common/header.tpl" %}
    <div class="container">
        <h2>
            Создать заявку
        </h2>
        <hr />
        {% if error %}
            <div class="alert alert-danger">
                {{ error }}
            </div>
        {% endif %}
        <form action="#" method="POST" enctype="multipart/form-data">
            <div class="row">
                <div class="col-md-6">
                    <div class="form-group">
                        <label>
                            <b>Телеграм ник:</b>
                        </label>
                        <input name="tg_username" class="form-control" type="text" required>
                        <small class="text-muted">
                            *вводите без @
                        </small>
                    </div>

                    <div class="form-group">
                        <label>
                            <b>Имя:</b>
                        </label>
                        <input name="first_name" class="form-control" type="text" required>
                    </div>
                     <div class="form-group">
                        <label>
                            <b>Фамилия:</b>
                        </label>
                        <input name="last_name" class="form-control" type="text" required>
                    </div>
                    <div class="form-group">
                        <label>
                            <b>Отчество:</b>
                        </label>
                        <input name="patronymic" class="form-control" type="text" value="не указано">
                    </div>
                    <div class="form-group">
                        <label>
                            <b>Страна:</b>
                        </label>
                        <select name="country" class="form-control">
                            <option value="Украина">Украина</option>
                            <option value="Россия">Россия</option>
                            <option value="Казахстан">Казахстан</option>
                        </select>
                    </div>

                    <div class="form-group">
                        <label>
                            <b>Область:</b>
                        </label>
                        <input name="region" class="form-control" required>
                    </div>

                    <div class="form-group">
                        <label>
                            <b>Город:</b>
                        </label>
                        <input name="city" class="form-control" required>
                    </div>

                    <div class="form-group">
                        <label>
                            <b>Адресс:</b>
                        </label>
                        <input name="address" class="form-control" required>
                    </div>

                    <div class="form-group">
                        <label>
                            <b>Дата рождения:</b>
                        </label>
                        <input name="birthday" class="form-control" required>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="form-group">
                        <label>
                            <b>Документ:</b>
                        </label>
                        <select name="document_type" class="form-control">
                            <option value="ID паспорт">
                                ID паспорт
                            </option>
                            <option value="Пластиковая карта">
                                Пластиковая карта
                            </option>
                            <option value="Загранпаспорт">
                                Загранпаспорт
                            </option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label>
                            <b>Реквизиты:</b>
                        </label>
                        <input name="credit_card" class="form-control" required>
                    </div>

                    <div class="form-group">
                        <label>
                            <b>Вид оплаты:</b>
                        </label>
                        <select name="type_payment" class="form-control">
                            <option value="100">100грн.</option>
                            <option value="300">300грн.</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label>
                            <b>Фото паспорта</b>
                        </label>
                        <input name="passport_photo" class="form-control" type="file" accept="image/*" />
                    </div>
                    <button class="btn btn-success" type="submit">
                        Создать
                    </button>
                </div>
            </div>
        </form>
    </div>
{% endblock %}