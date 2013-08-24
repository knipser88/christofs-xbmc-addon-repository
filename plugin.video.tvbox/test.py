# -*- coding: utf-8 -*-

#TV Box - by Christof Torres 2012 - 2013.

import urllib,urllib2,re,datetime,os.path

from xml.dom import minidom

user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'

xml = 'resources/data/channels_de.xml'

number = 0
xmldoc = minidom.parse(xml)
channel_list = xmldoc.getElementsByTagName('channel')
for channel in channel_list:
        number += 1
        name = channel.attributes['name'].value.encode("utf-8")
        url = channel.attributes['url'].value.encode("utf-8")
        try:
                if (addon.getSetting("epgsupport") == "true"):
                        epg = get_epg(channel.attributes['epg'].value.encode("utf-8"))
                else:
                        epg = ''
        except:
                epg = ''
        try:
                if (url.find('www.tv-kino.net') != -1):
                        req = urllib2.Request(url)
                        req.add_header('User-Agent', user_agent)
                        response = urllib2.urlopen(req)
                        link = response.read()
                        response.close()
                        flashvars = re.compile('file=(.+?)&amp;.+?streamer=(.+?)&amp;').findall(link)
                        for playpath, rtmp in flashvars:
                                rtmp = rtmp+' swfUrl=http://stream.tv-kino.net/player.swf playpath='+playpath+' pageurl='+url+' live=true swfvfy=true'
                elif (url.find('megatv.to') != -1):
                        req = urllib2.Request(url)
                        req.add_header('User-Agent', user_agent)
                        response = urllib2.urlopen(req)
                        link = response.read()
                        response.close()
                        #rtmp = re.compile('<video width="80%" src="(.+?)" controls="controls"></video>').findall(link)[0].replace("&amp;", "&")
                        #rtmp = re.compile('\'file\': \'(.+?)\'').findall(link)[0].replace("&amp;", "&")
                        rtmp = 'http://sv1.megatv.to/index.m3u8?c=pro7&auth=5e13d234495fef040feed7a17358c97a'
                else:
                        rtmp = url
                        thumbnail = '/resources/media/'+name.lower()+'.jpg'
                print number
                print name
                print epg
                print rtmp
                print thumbnail
                print len(channel_list)
        except:
                print "Unexpected Error: "+url

