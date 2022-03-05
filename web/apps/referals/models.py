from django.db import models


class Referals(models.Model):
    id = models.AutoField(primary_key=True)
    from_id = models.IntegerField(blank=True, null=True)
    to_id = models.IntegerField(blank=True, null=True)
    type_payment = models.IntegerField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)

    class Meta:
#        managed = False
        db_table = 'referals'
