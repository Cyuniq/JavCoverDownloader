#version:0.1.2
import  requests
from bs4 import BeautifulSoup
import re   
import os   #用于读写文件操作
import time #用于计算运行时间

#从网页抓取指定信息
def getInfo(frontname):
    global headers
    #网站需要挂代理
    global proxies
    mainUrl="https://www.javlibrary.com/cn/vl_searchbyid.php?keyword="+frontname
    response = requests.get(mainUrl,proxies = proxies, headers = headers)

    soup = BeautifulSoup(response.text,'lxml')
    global stateCode
    global videoTitle
    videoTitle = soup.find_all(re.compile("a"),limit=28)

    if videoTitle[27].get('title') == "我想要" :
        print('-! ! ! ! ! ! ! ! ! ! ! ! ! ! !')
        print("-查询成功:"+frontname+"存在多个返回结果，请手动处理")
        #print(soup.prettify())
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
    global headers
    global proxies
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




#全局变量部分

#状态码
# 0-状态正常 1-多个返回结果 2-不存在搜索结果
stateCode = 0 

#代理配置
proxyProtocol = 'socks5'
proxyHost     = '127.0.0.1'
proxyPort     = '10808'
proxies = {
    'http':  proxyProtocol+'://'+proxyHost+':'+proxyPort,
    'https': proxyProtocol+'://'+proxyHost+':'+proxyPort,
}

headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko"}



#获取当前文件夹路径
path=os.getcwd()
#获取当前目录下文件列表
fileList=os.listdir(path) 

'''
#####测试用代码块#####
fileName="tek-077-C.mp4"
print(strName(fileName))
frontName=os.path.splitext(fileName)[0]
strfrontName=strName(frontName)
#print(frontName)
backNmae=os.path.splitext(fileName)[1]
#print(backNmae)
ctcStart=time.time()
print('------------------------------')
getInfo(strfrontName)
if stateCode == 0 :
    downloadImage(videoTitle[27].string,pic.get('src'))
ctcEnd=time.time()
print("-耗    时:{:.2f}秒".format(ctcEnd-ctcStart))
####################
'''


'''
for fileName in fileList:
    frontName=os.path.splitext(fileName)[0]
    #print(frontName)
    backNmae=os.path.splitext(fileName)[1]
    #print(backNmae)
    ctcStart=time.time()
    print('------------------------------')
    strfrontName=strName(frontName)
    print('-识别番号:'+strfrontName)
    getInfo(strfrontName)
    if stateCode == 0 :
        downloadImage(videoTitle[27].string,pic.get('src'))
    ctcEnd=time.time()
    print("-耗    时:{:.2f}秒".format(ctcEnd-ctcStart))
'''