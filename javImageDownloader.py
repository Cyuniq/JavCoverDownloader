#version:0.1.2
import  requests
from bs4 import BeautifulSoup
import re   
import os   #用于读写文件操作
import time #用于计算运行时间

def getInfo(frontname):
    headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko"}
    #网站需要挂代理
    proxy = '127.0.0.1:10808'
    proxies = {
        'http': 'socks5://' + proxy,
        'https': 'socks5://' + proxy,
    }
    mainUrl="https://www.javlibrary.com/cn/vl_searchbyid.php?keyword="+frontname
    response = requests.get(mainUrl,proxies=proxies, headers = headers)

    soup = BeautifulSoup(response.text,'lxml')
    global stateCode
    global videoTitle
    videoTitle = soup.find_all(re.compile("a"),limit=28)

    if videoTitle[27].get('title') == "我想要" :
        print('-! ! ! ! ! ! ! ! ! ! ! ! ! ! !')
        print("-查询成功:"+frontname+"存在多个返回结果，请手动处理")
        stateCode = 1
        return
    if videoTitle[27].string == "tt-01sd3" :
        print('-! ! ! ! ! ! ! ! ! ! ! ! ! ! !')
        print("-查询失败:"+frontname+"是错误的番号，请手动处理")
        stateCode = 2
        return
    else:
        global pic
        stateCode = 0
        try:
            print("-查询成功:"+frontname)
            pic = soup.find('img',id="video_jacket_img")
            #print(pic.get('src'))
        except Exception as e:
            print(e)

def downloadImage(name,url):
    headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko"}
    proxy = '127.0.0.1:10808'
    proxies = {
        'http': 'socks5://' + proxy,
        'https': 'socks5://' + proxy,
    }
    if url[0:6] == "https:":
        jpgUrl=str(url)
    else :
        jpgUrl="https:"+str(url)
    jpgName=str(name)+".jpg"
    
    try:
        req = requests.get(jpgUrl, timeout=10)
            #print("正在从"+fileurl+"下载")
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




stateCode = 0 # 0-状态正常 1-多个返回结果 2-不存在搜索结果
path=os.getcwd() #获取当前文件夹路径
fileList=os.listdir(path) #获取当前目录下文件列表

'''
#####测试用代码块#####
fileName="stars-461.mp4"
frontName=os.path.splitext(fileName)[0]
#print(frontName)
backNmae=os.path.splitext(fileName)[1]
#print(backNmae)
ctcStart=time.time()
print('------------------------------')
getInfo(frontName)
if stateCode == 0 :
    downloadImage(videoTitle[27].string,pic.get('src'))
ctcEnd=time.time()
print("-耗    时:{:.2f}秒".format(ctcEnd-ctcStart))
####################
'''



for fileName in fileList:
    frontName=os.path.splitext(fileName)[0]
    #print(frontName)
    backNmae=os.path.splitext(fileName)[1]
    #print(backNmae)
    ctcStart=time.time()
    print('------------------------------')
    getInfo(frontName)
    if stateCode == 0 :
        downloadImage(videoTitle[27].string,pic.get('src'))
    ctcEnd=time.time()
    print("-耗    时:{:.2f}秒".format(ctcEnd-ctcStart))
