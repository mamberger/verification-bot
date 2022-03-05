{% extends 'common/base.tpl' %}
{% block title %}
    Установить баланс
{% endblock %}

{% block content %}
    {% include 'common/header.tpl' %}
    <div class="container">
        <div class="row">
            <div class="col-md-6">
                <form action="#" method="POST">
                    <div class="form-group">
                        <label>
                            <h3>Новый баланс</h3>
                        </label>
                        <input name="balance" type="number" class="form-control" value="{{ balance_account }}">
                    </div>
                    <input type="submit" class="btn btn-success" value="Установить" />
                </form>
            </div>
        </div>
    </div>
{% endblock %}