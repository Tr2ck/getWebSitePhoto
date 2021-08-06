'''
http://npm.taobao.org/mirrors/chromedriver/  需要下载driver 如果是chrome就下载chrome  先查看自己chrome的版本避免版本不对应无法执行
下载完毕后存在一个chromedriver.exe的程序，我们要使用webdriver模块时需要将其打开
可以设置系统变量
chromedriver 就可以直接执行了
'''


from selenium import webdriver
import time

#后台运行chrome
option = webdriver.ChromeOptions()
option.add_argument('--headless')
option.add_argument('--no-sandbox')
option.add_argument('--start-maximized')
option.add_argument('--disable-gpu')
option.add_argument('--ignore-certificate-errors')
option.add_argument('--disable-software-rasterizer')


count = 0


def get_png(domain):
    print(domain)
    driver=webdriver.Chrome(chrome_options=option)
    #driver.maximize_window()    #打开全屏幕模式
    driver.set_window_size(1920,1080)
    driver.implicitly_wait(4)   #截屏该网页
    driver.get(domain)
    domain=domain.split('//')[1]
    domain=domain.replace(':','_')
    time.sleep(1)
    path = "D:\\test\\"+str(domain)+".png"
    print(path)
    driver.get_screenshot_as_file(path)
    driver.quit()


def main():
    for line in open('ip.txt'):
         try:
            line = line.strip()
            get_png(line)
            time.sleep(1)
         except:
            pass


def banner():
    xfile = open('ip.txt')
    global count
    for line in xfile:
        count=count+1
    print("文件行数："+str(count)+"行")
    print("预计需要: "+str((count*5)/60.0)+"分钟")

if __name__ == "__main__":
    banner()
    main()
