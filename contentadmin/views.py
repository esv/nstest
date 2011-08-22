from django.http import HttpResponse
from contentadmin.models import VrContract, Content

def index(request):
    c = Content.objects.get()
    #v = VrContract.objects.get(pk=1)
    #c.contracts.remove(v)
    return HttpResponse(str(c.contracts.all()))
    #return HttpResponse(' '.join(c.link))
