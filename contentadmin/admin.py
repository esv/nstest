from django.contrib import admin
from nstest.contentadmin.models import Country, VrContract, Content, Status

class CountryAdmin(admin.ModelAdmin):
    #exclude = ('id',)
    pass

class VrContractAdmin(admin.ModelAdmin):
    #exclude = ('id',)
    pass

class ContentAdmin(admin.ModelAdmin):
    #exclude = ('id',)
    pass

class StatusAdmin(admin.ModelAdmin):
    #exclude = ('id',)
    pass

admin.site.register(Country, CountryAdmin)
admin.site.register(VrContract, VrContractAdmin)
admin.site.register(Content, ContentAdmin)
admin.site.register(Status, StatusAdmin)
