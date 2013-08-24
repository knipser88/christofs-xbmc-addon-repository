import urllib,urllib2,re

#KinoKiste - by Christof Torres 2011 - 2013.


user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
                        
url = 'http://kkiste.to/harry-potter-und-die-kammer-des-schreckens-stream.html'

req = urllib2.Request(url)
req.add_header('User-Agent', user_agent)
response = urllib2.urlopen(req)
link = response.read()
response.close()
parts = re.compile('<li class=".+?"><a href="(.+?)" target="_blank">Ecostream <small>(.+?)</small></a></li>').findall(link)
for part, part_number in parts:
        print part
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
                print link3
                stream_url = re.compile('<param name="flashvars" value="file=(.*?)&').findall(link3)[0]
                stream_url = 'http://www.ecostream.tv'+stream_url
                print stream_url
                print 'Ecostream '+part_number
