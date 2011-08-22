# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models
import arrayfields

class Country(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField(unique=True)
    title = models.TextField(unique=True)
    class Meta:
        db_table = u'country'

class VrContract(models.Model):
    id = models.IntegerField(primary_key=True)
    uniq_key = models.TextField()
    vr_id = models.IntegerField()
    date_start = models.DateField()
    date_end = models.DateField()
    title = models.TextField()
    fee = models.DecimalField(max_digits=10, decimal_places=4)
    class Meta:
        db_table = u'vr_contract'

class Status(models.Model):
    id = models.IntegerField(primary_key=True)
    status = models.TextField(unique=True)
    title = models.TextField(unique=True)
    description = models.TextField()
    class Meta:
        db_table = u'status'

class Content(models.Model):
    id = models.IntegerField(primary_key=True)
    status = models.ForeignKey(Status, db_column='status')
    title = models.TextField()
    compilation = models.TextField()
    origin_country = models.ForeignKey(Country, db_column='origin_country')
    duration = models.IntegerField()
    vr_contract = models.ForeignKey(VrContract)
    release_date = models.DateField(blank=True)
    date_insert = models.DateField()
    link = arrayfields.StringArrayField() # This field type is a guess.
    #list_vr_contract_id = models.TextField() # This field type is a guess.
    list_vr_contract_id = arrayfields.ArrayManyToManyField(VrContract, related_name='placeholder', manager_name='contracts', ) # This field type is a guess.
    view_price = models.DecimalField(max_digits=24, decimal_places=4)
    fee = models.DecimalField(max_digits=10, decimal_places=4)
    min_payment = models.DecimalField(max_digits=24, decimal_places=4)
    class Meta:
        db_table = u'content'

