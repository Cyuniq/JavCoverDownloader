from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException

import keyboard #检测按键退出
import sys #运行结束后关闭
import os #判断文件是否存在、获取当前路径
import time #用于计算运行时间
import random #随即秒数，模拟真实用户操作
import re #正则表达式

work_directory = "X:\\20240715\Downloads"

#从网页查询信息
def get_jav_url(url):
    try:
        driver.get(url)
        driver.set_page_load_timeout(10)
        if driver.find_element(By.CSS_SELECTOR,'h4') != "404 Page Not Found!":
            #print("页面内容:", driver.page_source[:2000])
            try:
                search_results = driver.find_element(By.CSS_SELECTOR, "h3")
                title_name = search_results.text
                print(search_results.text)
            except NoSuchElementException:
                print("搜索结果元素未找到")
            try:
                bigImage_url = driver.find_element(By.CLASS_NAME, "bigImage").get_attribute('href')
                download_and_rename_image(bigImage_url, search_results.text)
                #print(bigImage)
            except NoSuchElementException:
                print("搜索结果元素未找到")
            return title_name
        else:
            return "404 Page Not Found!"

    except TimeoutException:
        print("页面加载超时！")
        return "Page load timeout"
    except WebDriverException as e:
        print(f"WebDriver 错误: {e}")
        return "WebDriver error"
    except Exception as e:
        print(f"发生错误: {e}")
        return "Unexpected error"


def ifMedia(name):
    extensions = [".mp4", ".mkv"]
    return name in extensions

def strName(name):
    replace_patterns = ['-A', '-B', '-C', '-D', '-2k', '-4k', 'ch', 'hhd800.com@','-uncensored-nyap2p.com']
    for pattern in replace_patterns:
        name = name.replace(pattern, '')
    name = name.replace(' ', '-')
    name = name.split(' ')[0].upper()
    pattern = r'([A-Z]+[-\s]?\d+)'
    match = re.search(pattern, name)

    # 检查是否符合番号命名规则
    if match:
        print('处理后名字:'+match.group(0))
        return match.group(0)
    else:
        return None


def download_and_rename_image(image_url, new_file_name):

    # 获取图片扩展名
    file_extension = os.path.splitext(image_url)[1]

    # 构建新的文件名
    new_file_name_with_extension = new_file_name + file_extension

    if is_valid_filename(new_file_name_with_extension):
        print("文件名合法:"+new_file_name_with_extension)
    else:
        new_file_name_with_extension = sanitize_filename(new_file_name_with_extension)
        print(f"文件名不合法，修改后: {new_file_name_with_extension}")
    if os.path.exists(work_directory+"\\"+new_file_name_with_extension):
        print('文件已存在，跳过下载:'+new_file_name_with_extension)
    else:
        driver.get(image_url)
        script = """
        var img = document.querySelector('img');
        if (img) {
            var a = document.createElement('a');
            var image_name = arguments[0];
            a.href = img.src;
            a.download = image_name;  // 设置下载文件名
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
        }
        """
        driver.execute_script(script,new_file_name_with_extension)
        append_log_to_file('封面文件下载:'+new_file_name_with_extension+'\n')
        # 等待图像下载
        time.sleep(5)  # 根据实际下载时间调整等待时间




def sanitize_filename(filename):
    # 定义 Windows 和 Linux 不允许的字符
    windows_invalid_chars = r'[<>:"/\\|?*]'
    linux_invalid_chars = '/'

    # 替换 Windows 和 Linux 不允许的字符
    sanitized = re.sub(windows_invalid_chars, '_', filename)
    sanitized = sanitized.replace(linux_invalid_chars, '_')

    # 移除文件名末尾的空格或点
    sanitized = sanitized.rstrip(' .')

    return sanitized

def is_valid_filename(filename):
    # Windows 文件名规则
    windows_invalid_chars = r'[<>:"/\\|?*]'
    if re.search(windows_invalid_chars, filename) or filename.endswith((' ', '.')):
        return False

    # Linux 文件名规则
    if '/' in filename:
        return False

    return True

def append_log_to_file(content):
    try:
        with open('./log.txt', 'a', encoding='utf-8') as file:
            file.write(content)
    except Exception as e:
        print(f"日志追加到文件时发生错误: {e}")


def process_files(file_list):
    for file_name in file_list:
        # 提取文件的前缀和后缀
        base_name, extention = os.path.splitext(file_name)
        
        # 构造搜索 URL
        search_url = f"https://www.javbus.com/{strName(base_name)}"
        
        # 记录开始时间
        start_time = time.time()
        
        # 打印文件处理信息
        print('------------------------------')
        print(f"文件名: {base_name}")
        print(f"-识别番号: {strName(base_name)}")

        title_name=get_jav_url(search_url)
        print('标题名:'+title_name)
        if title_name not in ['404 Page Not Found!', 'Page load timeout', 'WebDriver error', 'Unexpected error']:
            new_file_name = title_name+extention
            if os.path.exists(new_file_name):
                print('文件存在，不处理')
            else:
                os.rename(work_directory+"\\"+file_name, work_directory+"\\"+new_file_name)
                append_log_to_file('原文件:'+file_name+'\n'+'命名后:'+new_file_name+'\n')
        else:
            print('未找到结果，请手动处理')
            append_log_to_file('文件:'+file_name+'\n'+'未搜索到'+'\n')
        # 随机等待时间
        wait_time = random.uniform(1, 10)
        print(f"等待 {wait_time:.2f} 秒")
        time.sleep(wait_time)
        print("暂停结束，继续执行")
        
        # 记录结束时间并计算耗时
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"-耗    时: {elapsed_time:.2f}秒")


proxy = "http://127.0.0.1:7897"

chrome_options = Options()
chrome_options.add_argument(f'--proxy-server={proxy}')
chrome_options.add_experimental_option('prefs', {
    "download.default_directory": work_directory,  # 设置下载路径为当前目录
})

chrome_options.binary_location = './chrome-win64/chrome.exe'
chrome_driver_path = "./chromedriver.exe"
chrome_service = Service(chrome_driver_path)
chrome_service.start()
driver = webdriver.Chrome(options=chrome_options,service=chrome_service)

chrome_version = driver.capabilities['browserVersion']
print("Chrome浏览器版本:", chrome_version)

#获取当前文件夹路径
#path=os.getcwd()
path=work_directory
print("path:"+path)
#获取当前目录下文件列表
file_list=[]
for file in os.listdir(path):
    if ifMedia(os.path.splitext(file)[1]) == 1:
        file_list.append(file)
print(file_list)

process_files(file_list)


driver.quit()
keyboard.read_key()
sys.exit()
