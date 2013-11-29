# -*- coding: utf-8 -*-
from HTMLParser import HTMLParser
import codecs
import os
import urllib2
#import pdb
#pdb.set_trace()

# create a subclass and override the handler methods
class GetDetailInfo(HTMLParser):
    AlbumInfo=[]
    is_title_found=None
    is_filename_found=None
    name=""
    filename=""
    def handle_data(self, data):
        if self.is_table_found:
            if data == u'相簿標題:':
                self.is_title_found=True
                return
        
            if self.is_title_found:
                self.name = data
                #print u'相簿標題:'+ self.name
                self.is_title_found=False
             
            if data == u'內容連結檔案:':
                self.is_filename_found=True
                return
        
    def handle_starttag(self, tag, attrs):
        if tag=='a' and self.is_filename_found:
            self.filename = attrs[0][1]
            #print u"檔案:"+ str(self.filename)
            self.is_filename_found=False
        if tag == 'table':
            self.is_table_found=True
            
    def handle_endtag(self, tag):
        if tag=='table':
            self.AlbumInfo.append({'name':self.name,'filename':self.filename})    
            self.is_table_found=False

def downfile(url, destdir):
    filename=url.split('/')[-1].split('?')[0]
    try:
        f = urllib2.urlopen(url)
        with open(destdir+'/'+filename, "wb") as code:
            code.write(f.read())
    except urllib2.HTTPError, err:
        if err.code == 404:
            print u'下載"%s"失敗'%filename
    except ValueError:
        print u'url為"%s"無法存取'%url
        


    
# read
#dest=input('請輸入目地位置,(default:"./")')
dest=u'./album'
          
# get the file of album detail ( title and descripts )
fileopen = codecs.open(dest+'/detail.html','r','utf-8')
details = fileopen.read()
fileopen.close()

# Parser Detail.html to get album name and url file name
parser = GetDetailInfo()
parser.is_table_found=False
parser.is_title_found=False
parser.is_filename_found=False
parser.feed(details)
Albums=parser.AlbumInfo


# Start Backup
for Album in Albums:
    # setting paramaters
    name=Album['name']
    # remove char illegal for dirname
    name=name.replace('/','').replace(u'"','').replace(u'?','').replace(u':','').replace(u'*','').replace(u'|','').replace(u'<','').replace(u'>','')
    urlfile=Album['filename']
    albumpath= dest + u'/' + name
    print u''
    print u'開始備份: %s'%name

    # make dir
    try:
        os.mkdir(albumpath)
    except WindowsError:
        print u"Error: 建立「%s」資料夾失敗，可能是資料夾已經存在，此相簿將放棄備份"%name
        continue

    # read url file
    try:
        f= codecs.open(dest+'/'+urlfile,'r','utf-8')
    except IOError:
        print u"Error: 無法找到關聯的URL檔案:%s , 此相簿將放棄備份"
        continue
        
    print urlfile
    for url in f.readlines():
        downfile(url,albumpath)

    print u'完成'
    
    
    


