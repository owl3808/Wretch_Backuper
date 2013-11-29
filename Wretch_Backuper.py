# -*- coding: utf-8 -*-
from HTMLParser import HTMLParser
import codecs
import os
import urllib2

# setting default encoding
'''default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
''''''
# debugger
import pdb
pdb.set_trace()
'''

# create a subclass and override the handler methods
class GetDetailInfo(HTMLParser):
    AlbumInfo=[]
    is_title_found=None
    is_filename_found=None
    name=""
    filename=""
    def handle_data(self, data):
        if self.is_table_found:
            if data == '相簿標題:':
                self.is_title_found=True
                return
        
            if self.is_title_found:
                self.name = data
                #print '相簿標題:'+ self.name
                self.is_title_found=False
             
            if data == '內容連結檔案:':
                self.is_filename_found=True
                return
        
    def handle_starttag(self, tag, attrs):
        if tag=='a' and self.is_filename_found:
            self.filename = attrs[0][1]
            #print "檔案:"+ str(self.filename)
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
            print '下載"%s"失敗'%filename
    except ValueError:
        print 'url為"%s"無法存取'%url
        



    
# read
try:
    CWD= os.path.dirname(os.path.abspath(__file__)).replace('\\','/')
    dest=CWD + '/album'
except NameError:
    dest='./album'
          
# get the file of album detail ( title and descripts )
fileopen = open(dest+'/detail.html','rb')
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
    name=name.replace('/','').replace('"','').replace('?','').replace(':','').replace('*','').replace('|','').replace('<','').replace('>','')
    urlfile=Album['filename']
    albumpath= dest + '/' + name
    print ''
    print '開始備份: %s'%name

    # make dir
    try:
        os.mkdir(albumpath.decode('utf-8'))
    except WindowsError as e:
        print "Error: 建立「%s」資料夾失敗，可能是資料夾已經存在，此相簿將放棄備份"%name
        print e
        continue

    # read url file
    try:
        f= codecs.open(dest+'/'+urlfile,'r','utf-8')
    except IOError:
        print "Error: 無法找到關聯的URL檔案:%s , 此相簿將放棄備份"%urlfile
        continue

    # download each file
    for url in f.readlines():
        downfile(url.decode('utf-8') ,albumpath.decode('utf-8'))

    print '完成'
    
    
    


