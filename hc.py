from collections import Counter
from konlpy.tag import Hannanum
from urllib.request import urlopen,Request
from urllib.parse import quote
from urllib.error import HTTPError
from re import compile,search,findall
from bs4 import BeautifulSoup
from multiprocessing import Pool
from os import getpid
from pprint import pprint
from key import KEY
def naver_search_summary(keyword,target="blog"):
    key = KEY
    keyword = quote(keyword)
    url = "http://openapi.naver.com/search?key={}&query={}&target={}&start=1&display=50".format(key,keyword,target)
    request = Request(url, headers={"Accept" : "application/xml"})
    html = urlopen(request).read()
    soup = BeautifulSoup(html,"html.parser")
    pprint(url)
    pprint (soup.title.string)
    links = []
    desc = []
    for e in soup.find_all("item"):
        stre = str(e)
        l = search(r'http://(.*?)(?=<)',stre).group()
        links.append(l)
        desc.append(e.description.string)
    return (links,desc)

def get_nouns(text, ntags=50, multiplier=10):
    h = Hannanum()
    nouns = h.nouns(text)
    count = Counter(nouns).most_common(50)
    return (nouns,count)

def parse_map(url):
    s = urlopen(url).read().decode()
    s = s.replace("\\",'')
    #pprint(s)
    x = search(r'(?<="mapX":)(\d*\.?\d*)(?=,"\w)',s).group()
    y = search(r'(?<="mapY":)(\d*\.?\d*)(?=,"\w)',s).group()
    title,addr = search(r'(?<="title":").*(?=","mapMode")',s).group().split('","address":"')
    return (x,y,title,addr.encode('utf-8').decode())

def parse_blog(url):
    map_link = None
    #pprint(url, getpid())

    html = urlopen(url).read()
    print(html)
    soup = BeautifulSoup(html,"html.parser")
    try:
        url = soup.find('frame')['src']
    except TypeError:
        print("This blog is not in naver")
        return None
    # get iframe link

    #If blog is not in naver

    if url[:9] != "/PostView":
        return map_link,url
    try:
        html = urlopen("http://blog.naver.com"+url).read()
    except HTTPError:
        return map_link,url

    
    soup = BeautifulSoup(html,"html.parser")
    article = soup.find('div',{'class':'post-view'})
    images = article.find_all('img')
    strings = article.stripped_strings
    #pprint(list(strings))
    iframe = article.find_all('iframe')
    try:
        for i in iframe:
            if "포스트에 첨부된 지도" == i['title']:
                map_link = i['src']
    except:
        pass

    return map_link,url

def is_hangul(text):
    """
    hangul = compile('[^ \u3131-\u3163\uac00-\ud7a3]+')
    hangul.findall(text)
    """
    hangul = compile('[ ㄱ-ㅣ가-힣]+')
    return bool(hangul.findall(text))

map_links = []

links, desc = naver_search_summary("홍대 혼자 밥")
with Pool(processes=4) as pool:
    map_links = pool.map(parse_blog,links)

#for i in links:
#    map_links.append(parse_blog(i))

#map_links =[(None, '/PostView.nhn?blogId=ji9511&logNo=220416530676&beginTime=0&jumpingVid=&from=search&redirect=Log&widgetTypeCall=true'), (None, '/PostView.nhn?blogId=mnani24&logNo=220473326932&beginTime=0&jumpingVid=&from=search&redirect=Log&widgetTypeCall=true'), (None, '/PostView.nhn?blogId=rhkrtjsdud56&logNo=220409593902&beginTime=0&jumpingVid=&from=search&redirect=Log&widgetTypeCall=true'), ('http://mashup.map.naver.com/view.nhn?mid=bl0117755227&type=total', '/PostView.nhn?blogId=aram0327&logNo=220455461112&beginTime=0&jumpingVid=&from=search&redirect=Log&widgetTypeCall=true'), (None, '/PostView.nhn?blogId=hyein5347&logNo=220461974128&beginTime=0&jumpingVid=&from=search&redirect=Log&widgetTypeCall=true'), ('http://mashup.map.naver.com/view.nhn?mid=bl0117932376@13575201&type=total', '/PostView.nhn?blogId=charmshongg&logNo=220463525469&beginTime=0&jumpingVid=&from=search&redirect=Log&widgetTypeCall=true'), ('http://mashup.map.naver.com/view.nhn?mid=bl0117950964@s30847318&type=total', '/PostView.nhn?blogId=yohandb&logNo=220460112611&beginTime=0&jumpingVid=&from=search&redirect=Log&widgetTypeCall=true'), ('http://mashup.map.naver.com/view.nhn?mid=bl0116197390&type=total', '/PostView.nhn?blogId=pos02013&logNo=220383113837&beginTime=0&jumpingVid=&from=search&redirect=Log&widgetTypeCall=true'), ('http://mashup.map.naver.com/view.nhn?mid=bl0117049062@s35958012&type=total', '/PostView.nhn?blogId=angelhot1&logNo=220422402514&beginTime=0&jumpingVid=&from=search&redirect=Log&widgetTypeCall=true'), ('http://mashup.map.naver.com/view.nhn?mid=bl0115929109@s30847318&type=total', '/PostView.nhn?blogId=yohandb&logNo=220370335429&beginTime=0&jumpingVid=&from=search&redirect=Log&widgetTypeCall=true'), ('http://mashup.map.naver.com/view.nhn?mid=bl0115374246@s36154695&type=total', '/PostView.nhn?blogId=ji9511&logNo=220344551202&beginTime=0&jumpingVid=&from=search&redirect=Log&widgetTypeCall=true'), (None, '/PostView.nhn?blogId=hynn2j&logNo=220487590799&beginTime=0&jumpingVid=&from=search&redirect=Log&widgetTypeCall=true'), ('http://mashup.map.naver.com/view.nhn?mid=bl0118398068@s21692522&type=total', '/PostView.nhn?blogId=japtevidajoa&logNo=220485294543&beginTime=0&jumpingVid=&from=search&redirect=Log&widgetTypeCall=true'), (None, '/PostView.nhn?blogId=lkh9007&logNo=220492298682&beginTime=0&jumpingVid=&from=search&redirect=Log&widgetTypeCall=true'), ('http://mashup.map.naver.com/view.nhn?mid=bl0118360939@s31044433&type=total', '/PostView.nhn?blogId=effortpeople&logNo=220467867536&beginTime=0&jumpingVid=&from=search&redirect=Log&widgetTypeCall=true'), (None, '/PostView.nhn?blogId=joymind100&logNo=220335546294&beginTime=0&jumpingVid=&from=search&redirect=Log&widgetTypeCall=true'), (None, '/PostView.nhn?blogId=clee20000&logNo=220293899286&beginTime=0&jumpingVid=&from=search&redirect=Log&widgetTypeCall=true'), (None, '/PostView.nhn?blogId=dlrmsgn137&logNo=220341638287&beginTime=0&jumpingVid=&from=search&redirect=Log&widgetTypeCall=true'), ('http://mashup.map.naver.com/view.nhn?mid=bl0118271728&type=total', '/PostView.nhn?blogId=dltptkddlek&logNo=220479557072&beginTime=0&jumpingVid=&from=search&redirect=Log&widgetTypeCall=true'), (None, '/PostView.nhn?blogId=bebamouso&logNo=220483307453&beginTime=0&jumpingVid=&from=search&redirect=Log&widgetTypeCall=true'), ('http://mashup.map.naver.com/view.nhn?mid=bl0113199436@s13575194&type=total', '/PostView.nhn?blogId=riflemp5&logNo=220238309696&beginTime=0&jumpingVid=&from=search&redirect=Log&widgetTypeCall=true'), ('http://mashup.map.naver.com/view.nhn?mid=bl0116668775@s13483839&type=total', '/PostView.nhn?blogId=hoyhoyo2&logNo=220405358513&beginTime=0&jumpingVid=&from=search&redirect=Log&widgetTypeCall=true'), (None, '/PostView.nhn?blogId=hyein5347&logNo=220482974003&beginTime=0&jumpingVid=&from=search&redirect=Log&widgetTypeCall=true'), ('http://mashup.map.naver.com/view.nhn?mid=bl0112593355@s12977962&type=total', '/PostView.nhn?blogId=dntwk87o_o&logNo=220207393747&beginTime=0&jumpingVid=&from=search&redirect=Log&widgetTypeCall=true'), ('http://mashup.map.naver.com/view.nhn?mid=bl0115961047@18717467&type=total', '/PostView.nhn?blogId=jyusco0929&logNo=220371673687&beginTime=0&jumpingVid=&from=search&redirect=Log&widgetTypeCall=true'), ('http://mashup.map.naver.com/view.nhn?mid=bl0115398863@s13011505&type=total', '/PostView.nhn?blogId=tnalskdlxm&logNo=220345697173&beginTime=0&jumpingVid=&from=search&redirect=Log&widgetTypeCall=true'), ('http://mashup.map.naver.com/view.nhn?mid=bl0114754610&type=total', '/PostView.nhn?blogId=makise2011&logNo=220315908795&beginTime=0&jumpingVid=&from=search&redirect=Log&widgetTypeCall=true'), ('http://mashup.map.naver.com/view.nhn?mid=bl0117130519@s19882431&type=total', '/PostView.nhn?blogId=co_ola&logNo=220427823361&beginTime=0&jumpingVid=&from=search&redirect=Log&widgetTypeCall=true'), ('http://mashup.map.naver.com/view.nhn?mid=bl0117880388@s13011505&type=total', '/PostView.nhn?blogId=dmlcjf5915&logNo=220461213667&beginTime=0&jumpingVid=&from=search&redirect=Log&widgetTypeCall=true'), ('http://mashup.map.naver.com/view.nhn?mid=bl0114457280@p18717733&type=total', '/PostView.nhn?blogId=lbabeel&logNo=220301870573&beginTime=0&jumpingVid=&from=search&redirect=Log&widgetTypeCall=true'), ('http://mashup.map.naver.com/view.nhn?mid=bl0118406459@p18717848&type=total', '/PostView.nhn?blogId=yeji0383&logNo=220485714507&beginTime=0&jumpingVid=&from=search&redirect=Log&widgetTypeCall=true'), ('http://mashup.map.naver.com/view.nhn?mid=bl0111873193@s11620952&type=total', '/PostView.nhn?blogId=yohandb&logNo=220172416580&beginTime=0&jumpingVid=&from=search&redirect=Log&widgetTypeCall=true'), ('http://mashup.map.naver.com/view.nhn?mid=bl0110075320@s13483839&type=total', '/PostView.nhn?blogId=youds0413&logNo=220084071856&beginTime=0&jumpingVid=&from=search&redirect=Log&widgetTypeCall=true'), ('http://mashup.map.naver.com/view.nhn?mid=bl0114677605@s20510788&type=total', '/PostView.nhn?blogId=won2gonzo&logNo=220312163438&beginTime=0&jumpingVid=&from=search&redirect=Log&widgetTypeCall=true'), (None, '/PostView.nhn?blogId=psjals&logNo=220465397110&beginTime=0&jumpingVid=&from=search&redirect=Log&widgetTypeCall=true'), ('http://mashup.map.naver.com/view.nhn?mid=bl019293510&type=total', '/PostView.nhn?blogId=yohandb&logNo=220045447867&beginTime=0&jumpingVid=&from=search&redirect=Log&widgetTypeCall=true'), (None, '/PostView.nhn?blogId=hodolry&logNo=220445267852&beginTime=0&jumpingVid=&from=search&redirect=Log&widgetTypeCall=true'), (None, '/PostView.nhn?blogId=gky5511&logNo=220394785337&beginTime=0&jumpingVid=&from=search&redirect=Log&widgetTypeCall=true'), (None, '/PostView.nhn?blogId=shk9402&logNo=220476831702&beginTime=0&jumpingVid=&from=search&redirect=Log&widgetTypeCall=true'), (None, '/PostView.nhn?blogId=lov375mile&logNo=220333748635&beginTime=0&jumpingVid=&from=search&redirect=Log&widgetTypeCall=true'), (None, '/PostView.nhn?blogId=qldgusgh0907&logNo=150128482359&beginTime=0&jumpingVid=&from=search&redirect=Log&widgetTypeCall=true'), (None, '/PostView.nhn?blogId=yjv619&logNo=220434900774&beginTime=0&jumpingVid=&from=search&redirect=Log&widgetTypeCall=true'), ('http://mashup.map.naver.com/view.nhn?mid=bl014948448@p18718411&type=total', '/PostView.nhn?blogId=fhjik6&logNo=100196242847&beginTime=0&jumpingVid=&from=search&redirect=Log&widgetTypeCall=true'), (None, '/PostView.nhn?blogId=paiele&logNo=30058324615&beginTime=0&jumpingVid=&from=search&redirect=Log&widgetTypeCall=true'), ('http://mashup.map.naver.com/view.nhn?mid=bl0116107832&type=total', '/PostView.nhn?blogId=seondud&logNo=220378522916&beginTime=0&jumpingVid=&from=search&redirect=Log&widgetTypeCall=true'), (None, '/PostView.nhn?blogId=unbalauloin&logNo=130170275264&beginTime=0&jumpingVid=&from=search&redirect=Log&widgetTypeCall=true'), ('http://mashup.map.naver.com/view.nhn?mid=bl0117303527@s13586350&type=total', '/PostView.nhn?blogId=deepp&logNo=220434396424&beginTime=0&jumpingVid=&from=search&redirect=Log&widgetTypeCall=true'), ('http://mashup.map.naver.com/view.nhn?mid=bl019057155@s21592216&type=total', '/PostView.nhn?blogId=nothinghall&logNo=220032261497&beginTime=0&jumpingVid=&from=search&redirect=Log&widgetTypeCall=true'), (None, '/PostView.nhn?blogId=fiona01&logNo=50160975708&beginTime=0&jumpingVid=&from=search&redirect=Log&widgetTypeCall=true')]

m = [(_map) for _map,link in map_links if _map is not None]
pprint(m)
with Pool(processes=4) as pool:
    pprint(pool.map(parse_map,m))
    
