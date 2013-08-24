import urllib,urllib2,re

#KinoKiste - by Christof Torres 2011 - 2013.


user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
                        
url = 'http://kkiste.to/how-i-met-your-mother-stream.html'

main_url = url
url = url+'?season=1'
req = urllib2.Request(url)
req.add_header('User-Agent', user_agent)
response = urllib2.urlopen(req)
link = response.read()
response.close()
print link
match = re.compile('value="(.+?)">Episode .+?</option>').findall(link)
print match

serie = main_url[25:main_url.find("-stream")]
serie = serie.lower()
serie = serie.replace("-", "+")

url2='http://www.fernsehserien.de/index.php?suche='+serie

req2 = urllib2.Request(url2)
req2.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
response2 = urllib2.urlopen(req2)
link2=response2.read()
response2.close()

#link2 = link2[link2.find('staffel='+name[8:len(name)]+'">'+name+'</a>'):len(link2)]
#link2 = link2[0:link2.find("<a href=")]
#link2 = link2.replace("<br>", "<br><br>")

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
        except:
                print 'EPISODE '+str(index+1)+' IS MISSING...!'
