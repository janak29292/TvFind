import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','TvFind.settings')

import django
django.setup()

import requests
from bs4 import BeautifulSoup as bs
from django.db import IntegrityError
from django.shortcuts import get_object_or_404

from showsearch.models import TvShow, Episode, Season

def lookup(text):
    text = text.replace(' ','+')
    url = 'https://www.imdb.com/search/title?title=' + text + '&title_type=tv_series'
    text = requests.get(url).text
    soup = bs(text,'lxml')
    try:
        search=soup.h3.a.get('href')
        base = url.split('.com')[0]+'.com'
        url = base+search
    except Exception as e:
        print('not found')
    else:
        return crawlshow(url,base)

def crawlshow(url,base):
    text = requests.get(url).text
    soup = bs(text,'lxml')
    postr=None
    rte=None
    vte=None
    summ=None
    divep = None
    if soup.find('div',class_='poster'):
        postr = soup.find('div',class_='poster').a.img.get('src')
    if soup.find('span',itemprop='ratingValue'):
        rte=soup.find('span',itemprop='ratingValue').text
    if soup.find('span',itemprop='ratingCount'):
        vte=soup.find('span',itemprop='ratingCount').text
    if soup.find('div',class_='summary_text'):
        summ=soup.find('div',class_='summary_text').text.strip()
    try:
        divep=soup.find('div',class_='seasons-and-year-nav').find_all('div')[2].a
        diveptxt=divep.text
    except Exception:
        diveptxt='0'

    print(soup.title.text)                                                      #name
    print(rte,vte)                                                              #rate, vote
    print(diveptxt)                                                             #number_of_seasons
    print(summ)                                                                 #summary
    print(postr)                                                                #image
    tvshow=TvShow(name=soup.title.text,
                    number_of_seasons=diveptxt,
                    rating=rte,
                    votes=vte,
                    summary=summ,
                    image=postr)
    try:
        tvshow.save()
    except IntegrityError:
        print('Show already exists')
    else:
        if divep:
            return (base+divep.get('href'),tvshow)


def ep_data(seurl,tvshow):
    text = requests.get(seurl).text
    soup = bs(text,'lxml')
    chest = soup.find_all('div',class_='list_item')
    srate=None
    n=0
    ep = 0
    for box in chest:
        strrate=box.find('span',class_='ipl-rating-star__rating').text
        if strrate=='':
            rate=None
        else:
            rate=float(strrate)
        if srate==None:
            srate = rate
        else:
            n+=1
            srate = (srate*(n-1) + rate)/n
        ep+=1
    print('\n'+soup.find('h3',id='episode_top').text.replace('\xa0',' '))   #name
    srate = float("{0:.1f}".format(srate))
    print(srate)                                                            #rating
    print(str(ep))                                                          #number_of_episodes
    seas=Season(show=tvshow,
                    name=soup.find('h3',id='episode_top').text.replace('\xa0',' '),
                    rating=srate,
                    number_of_episodes=str(ep))
    seas.save()
    for box in chest:
        print('\n\n\n\n\n')
        strrate=box.find('span',class_='ipl-rating-star__rating').text
        vote =box.find('span',class_='ipl-rating-star__total-votes')
        desc=None
        if vote:
            vote=vote.text
        if strrate=='':
            rate=None
        else:
            rate=float(strrate)
        if box.find('div',class_='item_description').text.strip()=='Know what this is about?\n Be the first one to add a plot.':
            pass
        else:
            desc=box.find('div',class_='item_description').text.strip()
        print(rate)                                              #rating
        print(box.div.div.div.text)                             #episode position
        print(box.div.a.get('title'))                           #name
        print(box.find('div',class_='airdate').text.strip())    #date
        print(vote)                                            #votes
        print(box.img.get('src'))                               #image
        print(desc)                                             #summary
        episode=Episode(season=seas,
                        rating=rate,
                        position=box.div.div.div.text,
                        name=box.div.a.get('title'),
                        date=box.find('div',class_='airdate').text.strip(),
                        votes=vote,
                        image=box.img.get('src'),
                        summary=desc)
        episode.save()
    base_show = seurl.split('?')[0]
    if soup.find('a',{'id':'load_previous_episodes'}):
        next_ep = base_show + soup.find('a',{'id':'load_previous_episodes'}).get('href')
        ep_data(next_ep,tvshow)

def showlist():
    url='https://www.imdb.com/list/ls051600015/?sort=list_order,asc&st_dt=&mode=detail&page=1'
    list=[]
    while url:
        text=requests.get(url).text
        url=None
        soup=bs(text,'lxml')
        if soup.find('a',class_='next-page'):
            url='https://www.imdb.com'+ soup.find('a',class_='next-page').get('href')
        for box in soup.find_all('div',class_='lister-item mode-detail'):
            list.append(box.find('h3').a.text)
    return list

if __name__ == '__main__':
    list=showlist()
    for text in list:
        try:
            ep,tvs = lookup(text)
        except TypeError:
            pass
        else:
            if ep:
                ep_data(ep,tvs)

# if __name__ == '__main__':
#     text=input()
#     ep,tvs = lookup(text)
#     if ep:
#         ep_data(ep,tvs)
