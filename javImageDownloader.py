#version:0.1.1
import  requests
from bs4 import BeautifulSoup
import re   
import os   #用于读写文件操作
import time #用于计算运行时间

def getInfo(id):
    headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko"}
    #网站需要挂代理
    proxy = '127.0.0.1:10808'
    proxies = {
        'http': 'socks5://' + proxy,
        'https': 'socks5://' + proxy,
    }
    mainUrl="https://www.javlibrary.com/cn/vl_searchbyid.php?keyword="+id
    response = requests.get(mainUrl,proxies=proxies, headers = headers)
    # 查看响应内容,response.text返回的是Unicode格式的数据
    #print(response.text)

    soup = BeautifulSoup(response.text,'lxml')
    global stateCode
    #获取标题
    global title
    title = soup.find_all(re.compile("a"),limit=28)
    #name=title[27].string
    #print(title[27].string)
    #print(title[27].text)
    if title[27].get('title') == "我想要" :
        print("?-查询成功:"+id+"存在多个返回结果，请手动处理")
        stateCode = 1
        return
    if title[27].string == "tt-01sd3" :
        print("×-查询失败:"+id+"是错误的番号，请手动处理")
        stateCode = 2
        return
    else:
        #获取封面地址
        global pic
        stateCode = 0
        try:
            print("√-查询成功:"+id)
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
        fileurl=str(url)
    else :
        fileurl="https:"+str(url)
    filename=str(name)+".jpg"
    
    try:
        req = requests.get(fileurl, timeout=10)
            #print("正在从"+fileurl+"下载")
        if req.status_code != 200:
            print('×--下载异常')
            return
        try:
            with open(filename, 'wb') as f:
                #req.content为获取html的内容
                f.write(req.content)
                print('√--下载成功:'+filename)
        except Exception as e:
            print(e)

    except requests.exceptions.RequestException as e:
        print(e)




stateCode = 0 # 0-状态正常 1-多个返回结果 2-不存在搜索结果

path=os.getcwd() #获取当前文件夹路径
fileList=os.listdir(path) #获取当前目录下文件列表
#fileNumber=len(fileList)


#####测试用代码块#####
id="stars-451"
ctcStart=time.time()
getInfo(id)
if stateCode == 0 :
    downloadImage(title[27].string,pic.get('src'))
ctcEnd=time.time()
print("耗时{:.2f}秒".format(ctcEnd-ctcStart))
id="rki-111"
ctcStart=time.time()
getInfo(id)
if stateCode == 0 :
    downloadImage(title[27].string,pic.get('src'))
ctcEnd=time.time()
print("耗时{:.2f}秒".format(ctcEnd-ctcStart))
####################



'''
for file in fileList:
    id=os.path.splitext(file)[0]
    #print(id)
    ctcStart=time.time()
    getInfo(id)
    if stateCode == 0 :
        downloadImage(title[27].string,pic.get('src'))
    ctcEnd=time.time()
    print("!---耗时:{:.2f}秒".format(ctcEnd-ctcStart))
'''