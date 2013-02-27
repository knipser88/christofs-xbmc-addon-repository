import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmcaddon

#KinoKiste - by Christof Torres 2011 - 2013.

addon = xbmcaddon.Addon(id='plugin.video.kinokiste')
path = addon.getAddonInfo('path')+'/resources/art/'

user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'

def CATEGORIES():
        addDir('Kinofilme','http://www.kkiste.to/aktuelle-kinofilme/',1,path+'/aktuelle-kinofilme.jpg')
        addDir('Serien','http://www.kkiste.to/serien/',2,path+'/serien.jpg')
        addDir('Neu!','http://www.kkiste.to/neue-filme/',3,path+'/neue-filme.jpg')
        addDir('Filmlisten','http://www.kkiste.to/film-index/',4,path+'/film-index.jpg')
        addDir('Genres','http://www.kkiste.to/genres/',5,path+'/genres.jpg')
        addDir('Suche','http://www.kkiste.to/search/?q=',6,path+'/suche.jpg')
                        
def INDEX(url):
        main_url = url
        req = urllib2.Request(main_url)
        req.add_header('User-Agent', user_agent)
        response = urllib2.urlopen(req)
        link = response.read()
        response.close()
        menu = url[20:len(url)]
        pages = re.compile('<li><a href="\?page=.+?">(.+?)</a></li>').findall(link)
        if (len(pages) != 0):
            pages = int(pages[len(pages)-1])
        else:
            pages = 1
        for i in range(1, (pages+1)):
                page_url = main_url+'?page='+str(i)
                req2 = urllib2.Request(page_url)
                req2.add_header('User-Agent', user_agent)
                response2 = urllib2.urlopen(req2)
                link2 = response2.read()
                response2.close()
                match = re.compile('<a href="(.+?)" title="(.+?)" class="title">.+?</a>').findall(link2)
                for url,name in match:
                        try:
                                url = 'http://www.kkiste.to'+url
                                req3 = urllib2.Request(url)
                                req3.add_header('User-Agent', user_agent)
                                response3 = urllib2.urlopen(req3)
                                link3 = response3.read()
                                response3.close()
                                match2 = re.compile('<img src="(.+?)" width="145" height="215" alt=".+?" />').findall(link3)
                                thumbnail = 'http://www.kkiste.to'+match2[0]
                                name = name[6:len(name)]
                                name = name[0:name.find('Stream ansehen')-1]
                                year = re.compile('Jahr:</span> (.+?)</p>').findall(link3) 
                                name = name+' ('+year[0]+')'
                                if (menu == '/serien/'):
                                       addDir(name,url,8,thumbnail)
                                else:
                                       addDir(name,url,10,thumbnail)
                        except:
                                print 'Unexpected error: '+url

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
        kb = xbmc.Keyboard('', 'www.kinokiste.com durchsuchen', False)
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
                        match2 = re.compile('<img src="(.+?)" width="145" height="215" alt=".+?" />').findall(link2)
                        thumbnail = 'http://www.kkiste.to'+match2[0]
                        name = name[6:len(name)]
                        name = name[0:name.find('Stream ansehen')-1]
                        year = re.compile('Jahr:</span> (.+?)</p>').findall(link2) 
                        name = name+' ('+year[0]+')'
                        if (link2.find('class="seasonselect"') != -1):
                                addDir(name,url,8,thumbnail)
                        else:
                                addDir(name,url,10,thumbnail)
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
                name = 'Staffel '+season_number
                addDir(name,url,9,path+'/staffel.jpg')

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
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        
        submenu=re.compile('<a class="submenu" href="#" onclick="(.+?);">(.+?)</a></li>').findall(link)
        if (len(submenu) > 0):
                for host,part in submenu:
                        host = host[host.find('(')+1:host.find(')')]
                        stream = url[0:24]+'/stream/'+url[25:len(url)]+'?h='+host
                        
                        req2 = urllib2.Request(stream)
                        req2.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                        response2 = urllib2.urlopen(req2)
                        link2=response2.read()
                        response2.close()

                        match2=re.compile('<iframe src="(.+?)"').findall(link2)

                        for eco_url in match2:
                            eco_url = eco_url[0:23]+'/stream/'+eco_url[30:len(eco_url)]
                            
                            formdictionary = { 'ss' : '1' }
                            params = urllib.urlencode(formdictionary)
                            response3 = urllib2.urlopen(eco_url, params)
                            link3 = response3.read()
                            response3.close()
                                
                            match3=re.compile("var t=setTimeout\(\"lc\('([^']+)','([^']+)','.+?','.+?'\)\",(.+?)\);").findall(link3)
                                
                            for s,k,t in match3:
                                next_url = 'http://www.ecostream.tv/object.php?s='+s+'&k='+k+'&t='+t
                                
                                req4 = urllib2.Request(next_url)
                                req4.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                                response4 = urllib2.urlopen(req4)
                                link4=response4.read()
                                response4.close()
                                
                                match4=re.compile('<param name="flashvars" value="file=(.*?)&').findall(link4)
                                if (match4[0].find('%') != -1):
                                    match4[0] = match4[0][0:match4[0].find('%')]
                                addLink(name+' - '+part,match4[0],path+'/ecostream.jpg')
        else:
            match=re.compile('<div class="embedplayer">\n\t\t\t\t\t<a href="(.+?)" target="_blank">').findall(link)
        
            for eco_url in match:

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
                    if (match3[0].find('%') != -1):
                        match3[0] = match3[0][0:match3[0].find('%')]
                    addLink(name,match3[0],path+'/ecostream.jpg')

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
