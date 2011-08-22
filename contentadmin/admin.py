from django.contrib import admin
from nstest.contentadmin.models import Country, VrContract, Content, Status

class CountryAdmin(admin.ModelAdmin):
    pass

class VrContractAdmin(admin.ModelAdmin):
	pass
	
class ContentAdmin(admin.ModelAdmin):
	pass
	
class StatusAdmin(admin.ModelAdmin):
	pass

admin.site.register(Country, CountryAdmin)
admin.site.register(VrContract, VrContractAdmin)
admin.site.register(Content, ContentAdmin)
admin.site.register(Status, StatusAdmin)
