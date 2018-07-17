from django.shortcuts import render, get_object_or_404
from showsearch.models import TvShow
# Create your views here.
def index(request):
    return render(request,'home.html',{'page':'home'})

def shows(request):
    tvshows = TvShow.objects.all().order_by('name')
    abets= ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    return render(request,'shows.html',{'page':'shows','tvshows':tvshows,'abets':abets})

def showdetails(request,key):
    det = get_object_or_404(TvShow,pk=key)
    return render(request,'showdetails.html',{'det':det})

def search(request):
    list = []
    title=''
    if request.method=='POST':
        title = request.POST.get('search')
        shows = TvShow.objects.all()
        for show in shows:
            if title=='':
                pass
            elif title.lower().replace(' ','') in show.name.lower().replace(' ',''):
                list.append(show)
    return render(request,'results.html',{'title':title,'list':list})
