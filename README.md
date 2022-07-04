# JavCoverDownloader

## 简介

根据文件名识别番号搜索标题 <br>
根据标题重命名原文件 <br>
下载专辑封面到本地并按照标题重命名 <br>
输出文件名修改日志 <br>

开发环境：Python 3.10.5 <br>
依赖：requests、BeautifulSoup4 <br>
数据源：https://www.javlibrary.com/cn/ <br>

## 使用方法
安装依赖

`pip install -r requirements.txt`

数据源网站因大家都懂的原因不能直接访问，默认在方法getWebpage中配置了代理为'socks5://127.0.0.1:10808'，自行修改即可 <br>


在需要搜索信息的媒体文件目录下使用python运行脚本即可

`python javImageDownloader.py`