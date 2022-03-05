{% extends 'common/base.tpl' %}
{% block title %}
    Авторизация
{% endblock %}

{% block head %}
    {% load static %}
    <link rel="stylesheet" href="{% static 'css/login.css' %}">
{% endblock %}

{% block content %}
<div class="wrapper fadeInDown">
  <div id="formContent">
      <div class="fadeIn first">
        <h4>Авторизация</h4>
    </div>
    <hr />
    {% if error %}
      <div class="alert alert-danger" role="alert">
        {{ error }}
      </div>
    {% endif %}
    <form action="/form/user/login" method="POST">
      {% csrf_token %}
      <input type="email" class="fadeIn second" name="email" placeholder="E-mail" required/>
      <input type="password" lass="fadeIn third" name="password" placeholder="Пароль" required/>
      <input type="submit" class="fadeIn fourth" value="Войти">
    </form>

  </div>
</div>
{% endblock %}