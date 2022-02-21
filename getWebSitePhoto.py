'''
http://npm.taobao.org/mirrors/chromedriver/  需要下载driver 如果是chrome就下载chrome  先查看自己chrome的版本避免版本不对应无法执行
下载完毕后存在一个chromedriver.exe的程序，我们要使用webdriver模块时需要将其打开
可以设置系统变量
chromedriver 就可以直接执行了
'''
#!/usr/bin/python3
# coding: utf-8

import requests
import time
import threading
import queue
from selenium import webdriver
import optparse


#warnings.filterwarnings(action='ignore')

exitFlag = 0
start = time.time()

#后台运行chrome
option = webdriver.ChromeOptions()
option.add_argument('--headless')
option.add_argument('--no-sandbox')
option.add_argument('--start-maximized')
option.add_argument('--disable-gpu')
option.add_argument('--ignore-certificate-errors')
option.add_argument('--disable-software-rasterizer')
option.add_experimental_option('excludeSwitches', ['enable-logging'])





class myThread(threading.Thread):
    def __init__(self, threadID, name, q):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.q = q

    def run(self):
        print("start sub_thread：" + self.name)
        brower=webdriver.Chrome(chrome_options=option,executable_path=r"C:\Program Files (x86)\Google\chromedriver.exe")
        process_data(self.threadID, self.name, self.q,brower)
        brower.quit()
        print("exit sub_thread：" + self.name)


def process_data(id, threadName, q,brower):
    while not exitFlag:
        if q.empty() == False:
            try:
                req = q.get()
                url = req
                #brower=webdriver.Chrome(chrome_options=option,executable_path=r"C:\Program Files (x86)\Google\chromedriver.exe")
                #brower.set_page_load_timeout(5)
                brower.implicitly_wait(3)
                brower.get(url=url)
                brower.set_window_size(1920,1080)
                name=url.split('//')[1]
                name=name.replace(':','_')
                name=name.replace('/','_')
                name=name.replace('?','_')
                name=name.replace('#','_')
                name=name.replace('=','_')
                name=name.replace('&','_')
                name=name.replace('"','_')
                picName = name + ".png"
                path = "C:\\Users\\Tr2ck\\Desktop\\p\\dd\\"+picName
                brower.save_screenshot(path)
            except:
                pass



if __name__ == "__main__":
    usage="python %prog -f file"
    parser=optparse.OptionParser(usage) ## 写入上面定义的帮助信息
    parser.add_option('-f', '--file',dest='File',type='string',help='import file')
    options, args=parser.parse_args()
    File = options.File
    # TODO：自行修改配置参数
    workQueue = queue.Queue(len(open(File,'r').readlines()))
    threads = []
    threadID = 1

    # TODO：自行修改配置参数
    file = open(File,'r')
    for text in file.readlines():
        domain = text.strip('\n')
        workQueue.put(domain)

    # TODO：自行修改配置参数
    for num in range(1, 5):
        tName = "thread-" + str(num)
        thread = myThread(threadID, tName, workQueue)
        thread.start()
        threads.append(thread)
        threadID += 1

    while not workQueue.empty():
        pass

    exitFlag = 1

    for t in threads:
        t.join()
    print("exit main thread")
    end = time.time()
    print("耗时" + str(end-start))
