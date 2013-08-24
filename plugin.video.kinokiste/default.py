import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmcaddon

#KinoKiste - by Christof Torres 2011 - 2013.

addon = xbmcaddon.Addon(id='plugin.video.kinokiste')
path = addon.getAddonInfo('path')+'/resources/art/'

user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'

def CATEGORIES():
        addDir('Kinofilme','http://www.kkiste.to/aktuelle-kinofilme/?page=1',1,path+'/aktuelle-kinofilme.jpg')
        addDir('Serien','http://www.kkiste.to/serien/',2,path+'/serien.jpg')
        addDir('Neu!','http://www.kkiste.to/neue-filme/',3,path+'/neue-filme.jpg')
        addDir('Filmlisten','http://www.kkiste.to/film-index/',4,path+'/film-index.jpg')
        addDir('Genres','http://www.kkiste.to/genres/',5,path+'/genres.jpg')
        addDir('Suche','http://www.kkiste.to/search/?q=',6,path+'/suche.jpg')
                        
def INDEX(url):
        main_url = url
        req = urllib2.Request(url)
        req.add_header('User-Agent', user_agent)
        response = urllib2.urlopen(req)
        link = response.read()
        response.close()
        pages = re.compile('<li><a href="\?page=.+?">(.+?)</a></li>').findall(link)
        match = re.compile('<a href="(.+?)" title="(.+?)" class="title">.+?</a>').findall(link)
        for url,name in match:
                try:
                        url = 'http://www.kkiste.to'+url
                        req2 = urllib2.Request(url)
                        req2.add_header('User-Agent', user_agent)
                        response2 = urllib2.urlopen(req2)
                        link2 = response2.read()
                        response2.close()
                        name = name[6:len(name)]
                        name = name[0:name.find('Stream ansehen')-1]
                        thumbnail = re.compile('<img src="(.+?)" width="145" height="215" alt=".+?" />').findall(link2)[0]
                        director = re.compile('<p><span>von:</span> <a href=".+?">(.+?)</a>').findall(link2)[0]
                        rating = re.compile('IMDB Rating:</span> <a href=".+?" target="_blank" title=".+?">(.+?)</a>').findall(link2)[0]
                        year = re.compile('Jahr:</span> (.+?)</p>').findall(link2)[0] 
                        plot = re.compile('<p id="kk-plot">(.+?)<span class="kk-ds">').findall(link2)[0].replace("<br>","\n").replace("<br />","\n").replace("&nbsp;"," ")
                        actors = re.compile('<li><a href="/darsteller/.+?/" title=".+?">(.+?)</a></li>').findall(link2)
                        cast = ''
                        for actor in actors:
                                cast = cast+actor+'\n'
                        if (link2.find('class="seasonselect"') != -1):
                                addSerie(name,url,thumbnail,director,rating,year,plot,cast)
                        else:
                                addMovie(name,url,thumbnail,director,rating,year,plot,cast)
                except:
                        print 'Unexpected error: '+url
        last_page = pages[len(pages)-1]
        current_page = main_url[46:len(main_url)]
        if (current_page < last_page):
                addDir('Folgende Seite >','http://www.kkiste.to/aktuelle-kinofilme/?page='+str(int(current_page)+1),1,'')

def ALPHABETICINDEX(url):
        for filter_index in '0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z':
                index_url = url+filter_index.lower()+'/'
                addDir(filter_index,index_url,1,path+'/'+filter_index+'.jpg')

def GENRESINDEX(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', user_agent)
        response = urllib2.urlopen(req)
        link = response.read()
        response.close()
        match = re.compile('<a href="(.+?)" title=".+?">(.+?) <span>.+?</span></a>').findall(link)
        for link,genre in match:
            genre_url = 'http://www.kkiste.to'+link
            addDir(genre,genre_url,1,path+'/genre.jpg')

def SEARCH(url):
        kb = xbmc.Keyboard('', 'KinoKiste durchsuchen', False)
        kb.doModal()
        if (kb.isConfirmed()) and (kb.getText() != ''):
                search = kb.getText()
                print 'Search for matches with: '+search
                search = search.replace(" ", "+")
                req = urllib2.Request(url+search)
                req.add_header('User-Agent', user_agent)
                response = urllib2.urlopen(req)
                link = response.read()
                response.close()
                match = re.compile('<a href="(.+?)" title="(.+?)" class="title">.+?</a>').findall(link)
                for url,name in match:
                    try:
                        url = 'http://www.kkiste.to'+url
                        req2 = urllib2.Request(url)
                        req2.add_header('User-Agent', user_agent)
                        response2 = urllib2.urlopen(req2)
                        link2 = response2.read()
                        response2.close()
                        name = name[6:len(name)]
                        name = name[0:name.find('Stream ansehen')-1]
                        thumbnail = re.compile('<img src="(.+?)" width="145" height="215" alt=".+?" />').findall(link2)[0]
                        director = re.compile('<p><span>von:</span> <a href=".+?">(.+?)</a>').findall(link2)[0]
                        rating = re.compile('IMDB Rating:</span> <a href=".+?" target="_blank" title=".+?">(.+?)</a>').findall(link2)[0]
                        year = re.compile('Jahr:</span> (.+?)</p>').findall(link2)[0]
                        plot = re.compile('<p id="kk-plot">(.+?)<span class="kk-ds">').findall(link2)[0].replace("<br>","\n").replace("<br />","\n")
                        actors = re.compile('<li><a href="/darsteller/.+?/" title=".+?">(.+?)</a></li>').findall(link2)
                        cast = ''
                        for actor in actors:
                                cast = cast+actor+'\n'
                        if (link2.find('class="seasonselect"') != -1):
                                addSerie(name,url,thumbnail,director,rating,year,plot,cast)
                        else:
                                addMovie(name,url,thumbnail,director,rating,year,plot,cast)
                    except:
                        continue
        
def SEASON(url,name):
        req = urllib2.Request(url)
        req.add_header('User-Agent', user_agent)
        response = urllib2.urlopen(req)
        link = response.read()
        response.close() 
        match = re.compile('<option value="(.+?)">Staffel .+?</option>').findall(link)
        for season_number in match:
                addDir(name+' - Staffel '+season_number,url,9,path+'/staffel.jpg')

def EPISODE(url,name):
        main_url = url
        url = url+'?season='+name[8:len(name)]
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('value="(.+?)">Episode .+?</option>').findall(link)

        serie = main_url[25:main_url.find("-stream")]
        serie = serie.lower()
        serie = serie.replace("-", "+")

        url2='http://www.fernsehserien.de/index.php?suche='+serie

        req2 = urllib2.Request(url2)
        req2.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response2 = urllib2.urlopen(req2)
        link2=response2.read()
        response2.close()

        link2 = link2[link2.find('staffel='+name[8:len(name)]+'">'+name+'</a>'):len(link2)]
        link2 = link2[0:link2.find("<a href=")]
        link2 = link2.replace("<br>", "<br><br>")

        match2=re.compile('<br>(.+?)<br>').findall(link2)

        tab_episode = [["" for col in range(2)] for row in range(int(match[0]))]

        for number in match:
            index = int(number)-1
            if (len(match2) > 1):
                title = match2[index]
                title = title[title.find(" ")+1:len(title)]
                name = 'Episode '+number+' - '+title
            else:
                name = 'Episode '+number

            tab_episode[index][0] = name
            tab_episode[index][1] = url+'&episode='+number

        for index in range(int(match[0])):
            try:
                print tab_episode[index][1]
                print tab_episode[index][0]
                SERIELINKS(tab_episode[index][1], tab_episode[index][0])
            except:
                print 'EPISODE '+str(index+1)+' IS MISSING...!'
                
def VIDEOLINKS(url,name):
        req = urllib2.Request(url)
        req.add_header('User-Agent', user_agent)
        response = urllib2.urlopen(req)
        link = response.read()
        response.close()
        parts = re.compile('<li class=".+?"><a href="(.+?)" target="_blank">Ecostream <small>(.+?)</small></a></li>').findall(link)
        for part, part_number in parts:
                formdictionary = { 'ss' : '1', 'sss' : '1' }
                params = urllib.urlencode(formdictionary)
                req2 = urllib2.Request(part, params)
                req2.add_header('User-Agent', user_agent)
                response2 = urllib2.urlopen(req2)
                link2 = response2.read()
                response2.close()
                match2 = re.compile("var t=setTimeout\(\"lc\('([^']+)','([^']+)','([^']+)','([^']+)'\)\",.+?\);").findall(link2)
                for a,b,t,key in match2:
                        url = 'http://www.ecostream.tv/lo/mq.php?s='+a+'&k='+b+'&t='+t+'&key='+key
                        formdictionary2 = { 's': a, 'k' : b, 't' : t, 'key' : key }
                        params2 = urllib.urlencode(formdictionary2)
                        req3 = urllib2.Request(url, params2)
                        req3.add_header('Referer', 'http://www.ecostream.tv')
                        req3.add_header('X-Requested-With', 'XMLHttpRequest')
                        response3 = urllib2.urlopen(req3)
                        link3 = response3.read()
                        response3.close()
                        stream_url = re.compile('<param name="flashvars" value="file=(.*?)&').findall(link3)[0]
                        stream_url = 'http://www.ecostream.tv'+stream_url
                        if (len(parts) == 1):
                                addLink(name+' - Ecostream',stream_url,path+'/ecostream.jpg')
                        else:
                                addLink(name+' - Ecostream '+part_number,stream_url,path+'/ecostream.jpg')

def SERIELINKS(url,name):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()

        match=re.compile('<iframe src="(.+?)"').findall(link)
        
        for eco_url in match:
                eco_url = 'http://www.ecostream.tv/stream/'+eco_url[30:len(eco_url)]

                formdictionary = { 'ss' : '1' }
                params = urllib.urlencode(formdictionary)
                response2 = urllib2.urlopen(eco_url, params)
                link2 = response2.read()
                response2.close()

                match2=re.compile("var t=setTimeout\(\"lc\('([^']+)','([^']+)','.+?','.+?'\)\",(.+?)\);").findall(link2)

                for s,k,t in match2:
                        next_url = 'http://www.ecostream.tv/object.php?s='+s+'&k='+k+'&t='+t
                        
                        req3 = urllib2.Request(next_url)
                        req3.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                        response3 = urllib2.urlopen(req3)
                        link3=response3.read()
                        response3.close()

                        match3=re.compile('<param name="flashvars" value="file=(.*?)&').findall(link3)
                        if (len(match3) > 0):        
                                for stream in match3:
                                        addLink(name,stream,path+'/ecostream.jpg')
                        else:
                                print 'EPISODE '+name[name.find(' ')+1:name.find('-')-1]+' IS STILL IN TRANSCODING...!'
                
def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param

def addLink(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok

def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def addSerie(name,url,iconimage,director,rating,year,plot,cast):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode=8&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Director": director, "Rating": rating, "Year": year, "Plot": plot, "Cast": "test" } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def addMovie(name,url,iconimage,director,rating,year,plot,cast):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode=10&name="+urllib.quote_plus(name)
        ok=True
        name = name+' ('+year+')'
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Director": director, "Rating": rating, "Year": year, "Plot": plot, "Cast": "test" } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
              
params=get_params()
url=None
name=None
mode=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass

print "Mode: "+str(mode)
print "URL : "+str(url)
print "Name: "+str(name)

if mode==None or url==None or len(url)<1:
        print "CATEGORIES()"
        CATEGORIES()
#-----------------------------------------------#       
#                Menu items                     #        
elif mode==1:
        print "INDEX("+url+")"
        INDEX(url)

elif mode==2:
        print "INDEX("+url+")"
        INDEX(url)

elif mode==3:
        print "INDEX("+url+")"
        INDEX(url)
        
elif mode==4:
        print "ALPHABETICINDEX("+url+")"
        ALPHABETICINDEX(url)

elif mode==5:
        print "GENRESINDEX("+url+")"
        GENRESINDEX(url)

elif mode==6:
        print "SEARCH("+url+")"
        SEARCH(url)
#-----------------------------------------------#
elif mode==8:
        print "SEASON("+url+","+name+")"
        SEASON(url,name)

elif mode==9:
        print "EPISODE("+url+","+name+")"
        EPISODE(url,name)

elif mode==10:
        print "VIDEOLINKS("+url+","+name+")"
        VIDEOLINKS(url,name)

elif mode==11:
        print "SERIENLINKS("+url+","+name+")"
        SERIELINKS(url,name)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
