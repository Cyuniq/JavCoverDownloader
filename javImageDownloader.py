#version:0.1.2
import  requests
from bs4 import BeautifulSoup
import re   
import os   #用于读写文件操作
import time #用于计算运行时间


def getWebpage(url):
    headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko"}
    proxyProtocol = 'socks5'
    proxyHost     = '127.0.0.1'
    proxyPort     = '10808'
    proxies = {
    'http':  proxyProtocol+'://'+proxyHost+':'+proxyPort,
    'https': proxyProtocol+'://'+proxyHost+':'+proxyPort,
}
    response = requests.get(url, proxies=proxies, headers=headers,timeout=10)
    return response


def searchInfo(url,frontname):
    #soup = getWebpage(url)
    soup = BeautifulSoup(getWebpage(url).text,'lxml')
    global videoTitle
    frontname=frontname.upper()
    if soup.find_all('a')[14].string == "缩图模式" :
        if len(soup.find_all('span')) == 0:
            print("-查询成功:"+frontname+"存在多个返回结果，已选择第一个匹配项")
            for a in soup.select('a[href][title]'):
                if a.text[:a.text.index(' ')] == strName(frontname):
                    videoTitle = a.text
                    print(videoTitle)
                    #print(a['href'][1:])
                    firstMatchUrl='https://www.javlibrary.com/cn'+a['href'][1:]
                    print(firstMatchUrl)
                    break #找到第一个匹配项后停止
            soup = searchInfo(firstMatchUrl,frontname)
            return soup
        if len(soup.find_all('span') )!= 0 :
            videoTitle = "无查询结果"
            print("-查询失败:'"+frontname+"'搜寻没有结果。")
            return soup            
            #return getWebpage(firstMatchUrl)

    if frontname == soup.find_all('td')[8].string:
        videoTitle = soup.find_all("a")[14].string
        try:
            print("-查询成功:"+frontname+"查询到匹配结果")
            #print(pic.get('src'))
        except Exception as e:
            print(e)
        return soup

def downloadImage(name,url):
    if url[0:6] == "https:":
        jpgUrl=str(url)
    else :
        jpgUrl="https:"+str(url)
    jpgName=str(name)+".jpg"
    try:
        req = getWebpage(jpgUrl)
        if req.status_code != 200:
            print('-下载异常')
            return
        try:
            if (os.path.exists(jpgName)==True):
                print('-封面存在，跳过下载')
            if (os.path.exists(jpgName)==False):    
                with open(jpgName, 'wb') as f:
                    #req.content为获取html的内容
                    f.write(req.content)
                    print('-下载成功:'+jpgName[:48]+(jpgName[48:] and  '...'))
                    #print('-下载成功:'+jpgName)
        except Exception as e:
            print(e)

    except requests.exceptions.RequestException as e:
        print(e)

def strName(name):
    name=name.replace('-A','')
    name=name.replace('-B','')
    name=name.replace('-C','')
    name=name.replace('-D','')
    name=name.replace('-2k','')
    name=name.replace('-4k','')
    name=name.replace('ch','')
    name=name.replace('jav20s8.com@','')
    name=name.replace('hhd800.com@','')
    name=name.upper()
    return name

def renameFile(path,srcname,dstname):
    srcpathNname=path+'\\'+srcname
    print(srcpathNname)
    dstpathNname=path+'\\'+dstname+os.path.splitext(srcname)[1]
    print(dstpathNname)
    writeLog(srcname+'--->'+dstname+os.path.splitext(srcname)[1])
    os.rename(srcpathNname,dstpathNname)

def writeLog(log):
    path=os.getcwd()
    with open(path+'\\log.txt','a',encoding='utf-8') as f:
        f.write(log+'\n')



'''
#####测试用代码块#####
fileName="tek-077-C.mp4"
fileName="rki-111-C.mp4"
fileName="测试.mp4"
frontName=os.path.splitext(fileName)[0]
#print(frontName)
backNmae=os.path.splitext(fileName)[1]
#print(backNmae)
ctcStart=time.time()
mainSearchUrl="https://www.javlibrary.com/cn/vl_searchbyid.php?list&keyword="+strName(frontName)
print('------------------------------')
print("-识别番号:"+strName(frontName))
searchResult=searchInfo(mainSearchUrl,strName(frontName))
coverSoup=searchResult.find('img',id="video_jacket_img")
if coverSoup != None:
    downloadImage(videoTitle,coverSoup.get('src'))
ctcEnd=time.time()
print("-耗    时:{:.2f}秒".format(ctcEnd-ctcStart))
####################
'''


#状态码
# 0-状态正常 1-多个返回结果 2-不存在搜索结果
stateCode = 0 

#获取当前文件夹路径
path=os.getcwd()
#获取当前目录下文件列表
fileList=os.listdir(path) 

for fileName in fileList:
    frontName=os.path.splitext(fileName)[0]
    #print(frontName)
    backNmae=os.path.splitext(fileName)[1]
    #print(backNmae)
    ctcStart=time.time()
    mainSearchUrl="https://www.javlibrary.com/cn/vl_searchbyid.php?list&keyword="+strName(frontName)
    print('------------------------------')
    print("-识别番号:"+strName(frontName))
    searchResult=searchInfo(mainSearchUrl,strName(frontName))
    coverSoup=searchResult.find('img',id="video_jacket_img")
    if coverSoup != None:
        print(videoTitle)
        downloadImage(videoTitle,coverSoup.get('src'))
        renameFile(path,fileName,videoTitle)
    ctcEnd=time.time()
    print("-耗    时:{:.2f}秒".format(ctcEnd-ctcStart))

