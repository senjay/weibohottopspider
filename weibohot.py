import requests
import datetime
import time
import pymysql
from bs4 import BeautifulSoup
import random
hottime=''#时间
sql = "insert into hottop(time,top)values(%s,%s)"
db = pymysql.connect("ip","user","passwd","weibohot")#weibohot为数据库名
cursor = db.cursor()

def Gethot():
    url = 'https://s.weibo.com/top/summary?cate=realtimehot'
    #这里为了稳定,可以添加一个user-Agent的池,然后每次用的时候随机一个,也可以添加ip池
    header={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0'
    }
    try:
        # global 声明接下来用的hottime是全局变量,
        # 如果不加这个,它会变成局部变量,即使你在函数外声明了一个hottime
        global hottime
        hottime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        hotweb = requests.get(url, headers=header, timeout=10)
    except:
        print(hottime+':http Error')
    else:
        soup = BeautifulSoup(hotweb.text, "html.parser")
        ans = soup.find_all('td')
        top = ''
        for i in ans:
            a = i.find('a')  # a标签内容，即热搜内容
            span = i.find('span')  # span标签内的的热度
            if (a != None and span != None):
                top += a.get_text() + '__' + span.get_text() + '\n'
        return top

errorcount=0#5次错误跳出循环
while True:
    try:
        top = Gethot()
        cursor.execute(sql,(hottime,top))
    except Exception as e:
        errorcount+=1
        db.rollback()
        print(hottime+":执行MySQL: %s 时出错：%s" % (sql, e))
        if(errorcount==5):
            break
        else:
            time.sleep(10)
            continue
    else:
        db.commit()
        time.sleep(random.randint(450,550))#每次sleep随机450-550秒




