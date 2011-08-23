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
from datetime import datetime

class Country(models.Model):
    #id = models.IntegerField(primary_key=True)
    name = models.TextField(unique=True)
    title = models.TextField(unique=True)
    
    class Meta:
        db_table = u'country'

    def __unicode__(self):
        return self.title

class VrContract(models.Model):
    #id = models.IntegerField(primary_key=True)
    uniq_key = models.TextField()
    vr_id = models.IntegerField()
    date_start = models.DateField()
    date_end = models.DateField()
    title = models.TextField()
    fee = models.DecimalField(max_digits=10, decimal_places=4)

    class Meta:
        db_table = u'vr_contract'

    def __unicode__(self):
        return self.title

class Status(models.Model):
    #id = models.IntegerField(primary_key=True)
    status = models.TextField(unique=True)
    title = models.TextField(unique=True)
    description = models.TextField(blank=True)

    class Meta:
        db_table = u'status'

    def __unicode__(self):
        return self.title

class Content(models.Model):
    #id = models.IntegerField(primary_key=True, blank=True, null=True)
    status = models.ForeignKey(Status, db_column='status', default=1, on_delete=models.PROTECT)
    title = models.TextField()
    compilation = models.TextField(blank=True)
    origin_country = models.ForeignKey(Country, db_column='origin_country', on_delete=models.PROTECT)
    duration = models.IntegerField(blank=True)
    vr_contract = models.ForeignKey(VrContract, blank=True, on_delete=models.PROTECT, null=True)
    release_date = models.DateField(blank=True)
    date_insert = models.DateField(default=datetime.now())
    link = arrayfields.StringArrayField(blank=True)
    list_vr_contract_id = arrayfields.ArrayManyToManyField(VrContract, related_name='noname', manager_name='contracts')
    view_price = models.DecimalField(max_digits=24, decimal_places=4, blank=True)
    fee = models.DecimalField(max_digits=10, decimal_places=4, blank=True)
    min_payment = models.DecimalField(max_digits=24, decimal_places=4, blank=True)

    class Meta:
        db_table = u'content'

    def __unicode__(self):
        return self.title
