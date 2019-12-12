import re

import requests
from bs4 import BeautifulSoup
from hrs.models import Film,Img
from concurrent.futures import ThreadPoolExecutor
F=[]
I=[]
star=True
class Films:
    name=''
    Type=''
    msg=[]
    Torrent=[]
    TorrentURL=[]
    FilmURL=''

    def getList(self):
        list=[]
        I=0
        for m in self.msg:
            one=Film(self.FilmURL+str(I),self.name,self.Type,self.Torrent[I],self.FilmURL,m['big'])
            list.append(one)
            I+=1
        return list
        pass
    def getImgList(self):
        list=[]
        I=0
        for m in self.msg:
            imglist=m['img']
            for imgurl in imglist:
                one=Img(None,self.FilmURL + str(I),imgurl)
            I+=1
        return list
        pass

    def setMsg(self,text):
        pp = re.split('【', text)
        name = ''
        big = 0
        for p in pp:
            o = re.split('】：', p)
            if o[0] in ['影片名称']:
                name = o[1]
            if o[0] in['影片大小','档案大小'] :

                if re.search('MB', o[1], flags=re.I):
                    big = float(re.split('MB', o[1], flags=re.I)[0])
                if re.search('G', o[1], flags=re.I):
                    big = float(re.split('G', o[1], flags=re.I)[0]) * 1024
        thisMsg={'doc':text,'name':name,'big':big,'img':[]}
        self.msg.append(thisMsg)
        pass

    def __init__(self,name,Type,URL):
        self.name=name
        self.Type+=Type
        self.FilmURL='https://cc.6hrz.icu/'+URL
        self.Torrent=[]
        self.TorrentURL=[]
        self.msg=[]
        html = requests.get(self.FilmURL)
        html.encoding = 'GBK'
        bf = BeautifulSoup(html.text, features="lxml")
        a_ls = bf.find_all('a')
        Ix=0
        for a in a_ls:
            a_text = a.text
            a_href = a.get('href')
            r_h=None
            if a_href!=None:
                r_h = re.search('hash', a_href)
            r = re.search('hash', a_text)
            if r != None:
                self.Torrent.append('http://www.rmdown.com/download.php?ref=' + a_text[r.span()[0]:])
                self.TorrentURL.append(a_text)
                a_p=a.find_parent()
                self.setMsg(a_p.text)
                img_ls=a_p.find_all('img')
                for img in img_ls:
                    p=img.get('data-src')
                    if re.search('jpg',p)!=None:
                        self.msg[Ix]['img'].append(str(p))
            elif r_h!=None:
                self.Torrent.append('http://www.rmdown.com/download.php?ref='+a_href[r.span()[0]:])
                self.TorrentURL.append('http://www.rmdown.com/link.php?' + a_href[r.span()[0]:])
                a_p = a.find_parent()
                self.setMsg(a_p.text)
                img_ls = a_p.find_all('img')
                for img in img_ls:
                    p=img.get('data-src')
                    if re.search('jpg',p)!=None:
                        self.msg[Ix]['img'].append(str(p))
            else:
                pass
            pass
        pass
    def __str__(self):
        show=self.name+'\t'+self.Type+'\t'+self.FilmURL+'\n'+'\t'
        for i in self.msg:
            show +=i['name']
            show +=str(i['big'])
        return show

def getFilm(i,Index,type):
    html = requests.get(f"https://cc.6hrz.icu/thread0806.php?fid={i}&page={Index}")
    html.encoding = 'GBK'
    bf = BeautifulSoup(html.text, features="lxml")
    itme_ls = bf.find_all('h3')
    for itme in itme_ls:
        href=itme.a.get('href')
        if len(str(href))==28:
            newFo(itme,type,href)
    pass
def newFo(itme,type,href):
    film = Films(itme.a.text, type, href)
    if len(film.msg) > 0:
        fs=film.getList()
        for f in  fs:
            print(f)
            f.save()
        ils=film.getImgList()
        for i in ils:
            print(i)
            i.save()
    pass


P=[[2,100,'亚洲无码'],[5,100,'里番动漫']]
#pool=ThreadPoolExecutor(max_workers=30)
def down(i):
    p=P[0]
    i=1
    while i<p[1]:
        getFilm(p[0], i, p[2])


