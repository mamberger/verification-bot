<!DOCTYPE html>
<html lang="ru">
    <head>
        <title>{% block title %}{% endblock %} | Verification</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        {% load static %}
        <link rel="stylesheet" href="{% static 'css/bootstrap.min.css' %}">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
	<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-ka7Sk0Gln4gmtz2MlQnikT1wXgYsOg+OMhuP+IlRH9sENBO0LRn5q+8nbTov4+1p" crossorigin="anonymous"></script>

	<link rel="stylesheet" href="{% static 'css/base.css' %}" />
        {% block head %}
        {% endblock %}

    </head>
    <body>
        <div id="content">
        {% block content %}
        {% endblock %}
        </div>



        {% block scripts %}{% endblock %}
        <script src="{% static 'scripts/jquery-3.3.1.slim.min.js' %}"></script>
        <script src="{% static 'scripts/popper.min.js' }"></script>
        <script src="{% static 'scripts/bootstrap.min.js' %}"></script>
    </body>
</html>
