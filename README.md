# JavCoverDownloader

## 简介

根据文件名识别番号搜索标题 <br>
根据标题重命名原文件 <br>
下载专辑封面到本地并按照标题重命名 <br>
输出文件名修改日志 <br>

数据源：https://www.javbus.com/ <br>

## 使用方法
安装依赖

自行下载对应浏览器的驱动，示例使用chrome，需搭配下载chromedriver使用。


数据源网站因大家都懂的原因不能直接访问，默认在方法getWebpage中配置了代理为'socks5://127.0.0.1:7897'，自行修改即可 <br>


修改需要搜索信息的媒体文件目录，运行脚本即可

`python javImageDownloader.py`