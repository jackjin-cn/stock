#coding: UTF-8
import math
import time
import string
import sys,os
import os, io, sys, re, time, json, base64
import webbrowser
import urllib2

import msvcrt
import time
import ctypes



STD_INPUT_HANDLE = -10  
STD_OUTPUT_HANDLE= -11  
STD_ERROR_HANDLE = -12  
  
FOREGROUND_BLACK = 0x0  
FOREGROUND_BLUE = 0x01 # text color contains blue.  
FOREGROUND_GREEN= 0x02 # text color contains green.  
FOREGROUND_RED = 0x04 # text color contains red.  
FOREGROUND_INTENSITY = 0x08 # text color is intensified.  
  
BACKGROUND_BLUE = 0x10 # background color contains blue.  
BACKGROUND_GREEN= 0x20 # background color contains green.  
BACKGROUND_RED = 0x40 # background color contains red.  
BACKGROUND_INTENSITY = 0x80 # background color is intensified.  
  
class Color:  
    ''''' See http://msdn.microsoft.com/library/default.asp?url=/library/en-us/winprog/winprog/windows_api_reference.asp 
    for information on Windows APIs.'''  
    std_out_handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)  
      
    def set_cmd_color(self, color, handle=std_out_handle):  
        """(color) -> bit 
        Example: set_cmd_color(FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE | FOREGROUND_INTENSITY) 
        """  
        bool = ctypes.windll.kernel32.SetConsoleTextAttribute(handle, color)  
        return bool  
      
    def reset_color(self):  
        self.set_cmd_color(FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE)  
      
    def print_red_text(self, print_text):  
        self.set_cmd_color(FOREGROUND_RED | FOREGROUND_INTENSITY)  
        print print_text  
        self.reset_color()  
          
    def print_green_text(self, print_text):  
        self.set_cmd_color(FOREGROUND_GREEN | FOREGROUND_INTENSITY)  
        print print_text  
        self.reset_color()  
      
    def print_blue_text(self, print_text):   
        self.set_cmd_color(FOREGROUND_BLUE | FOREGROUND_INTENSITY)  
        print print_text  
        self.reset_color()  
            
    def print_red_text_with_blue_bg(self, print_text):  
        self.set_cmd_color(FOREGROUND_RED | FOREGROUND_INTENSITY| BACKGROUND_BLUE | BACKGROUND_INTENSITY)  
        print print_text  
        self.reset_color()      
  

      
# http://hq.sinajs.cn/list=sh600000

# http://hq.sinajs.cn/list=sz000913
#var hq_str_sh601006="大秦铁路, 27.55, 27.25, 26.91, 27.55, 26.20, 26.91, 26.92,
#                     22114263, 589824680, 4695, 26.91, 57590, 26.90, 14700, 26.89,
#                     14300,6.88, 15100, 26.87, 3100, 26.92, 8900, 26.93, 14230,
#                     26.94, 25150, 26.95, 15220, 26.96, 2008-01-11, 15:05:32";

 
#
#   0：”大秦铁路”，股票名字；
#   1：”27.55″，今日开盘价；
#   2：”27.25″，昨日收盘价；
#   3：”26.91″，当前价格；//时间结束后也就是收盘价了
#   4：”27.55″，今日最高价；
#   5：”26.20″，今日最低价；
#   6：”26.91″，竞买价，即“买一”报价；
#   7：”26.92″，竞卖价，即“卖一”报价；
#   8：”22114263″，成交的股票数，由于股票交易以一百股为基本单位，所以在使用时，通常把该值除以一百；
#   9：”589824680″，成交金额，单位为“元”，为了一目了然，通常以“万元”为成交金额的单位，所以通常把该值除以一万；
#   10：”4695″，“买一”申请4695股，即47手；
#   11：”26.91″，“买一”报价；
#   12：”57590″，“买二”
#   13：”26.90″，“买二”
#   14：”14700″，“买三”
#   15：”26.89″，“买三”
#   16：”14300″，“买四”
#   17：”26.88″，“买四”
#   18：”15100″，“买五”
#   19：”26.87″，“买五”
#   20：”3100″，“卖一”申报3100股，即31手；
#   21：”26.92″，“卖一”报价 (22, 23), (24, 25), (26,27), (28, 29)分别为“卖二”至“卖四的情况”
#   30：”2008-01-11″，日期；  
#   31：”15:05:32″，时间；

import msvcrt 
import time

def kbfunc(): 
   x = msvcrt.kbhit()
   if x: 
      ret = ord(msvcrt.getch()) 
   else: 
      ret = 0 
   return ret

def calc_profit(buy,sell,number):
    #==========相关费率
    profit=[0]*4
    yongjin=0.0006 #拥金
    yinhuasui=0.001#印花税率
    
    buy_fee=buy*number*yongjin
    sell_fee=sell*number*(yongjin+yinhuasui)
    souxufei=number*.0006

    #计算 利润-利润率
    profit[0]=(sell-buy)*number-buy_fee-sell_fee-2*souxufei
    profit[1]=profit[0]/(buy*number)#利润率
    profit[2]=sell*number-sell_fee-souxufei#真市值
    return profit
#print "buy_f'e=",buy_fee
#print "sell_fee",sell_fee
#print "souxufei",souxufei*2

def querystock(stock_code,buy,number):
    stock={}
    exchange = "sz" if (int(stock_code) // 100000 == 3) else "sh"
    query="http://hq.sinajs.cn/list="
    qy=query+exchange+stock_code
    stdout = urllib2.urlopen(qy)
    html=stdout.read()
    tempData = re.search('''(")(.+)(")''', html).group(2)
    stockinfo = tempData.split(",")
    sell=string.atof(stockinfo[3])
    pf=calc_profit(buy,sell,number)#利润

    stock['name']=stockinfo[0]
    stock['yestoday']=string.atof(stockinfo[2])
    stock['now']=string.atof(stockinfo[3])
    stock['max']=string.atof(stockinfo[4])
    stock['min']=string.atof(stockinfo[5])
    stock['profit']=pf[0]
    stock['profit_percent']=pf[1]*100
    stock['cost']=buy*number
    stock['time']=stockinfo[31]
    stock['date']=stockinfo[30]
    stock['range']=(stock['now']/stock['yestoday']-1)*100
    stock['buy']=buy
    stock['number']=number
    stock['total']=stock['now']*number
    stock['true_total']=pf[2]
    return stock


#**********  main   **************

#==========设置买入＝＝＝＝＝＝＝

#buy=32
#number=3500
#stock='601688'
format_number=5 #文件数据行数
fb=open('stock.txt','r')
line=fb.readlines()
fb.close()

repeat=len(line)/format_number
times=2
stock_number=10
runing=1
res=['']*12
max=[0]*10
prev=[0]*10
stock=[{}]*stock_number  #最多支持几支股票查询
up=u'↗'
down=u'↘'
no=u' '
flag=u''
clr=Color()
while runing:
    for i in range(repeat):
        up2=u' '
        buy=string.atof(line[1+i*format_number])
        number=string.atoi(line[2+i*format_number])
        stock_code=line[0+i*format_number]
        stock[i]=querystock(stock_code,buy,number)
        max[i]=stock[i]['now']
        if stock[i]['now']==stock[i]['max']:
            flag=u'☆'*times
            clr.set_cmd_color(0x1|BACKGROUND_INTENSITY)

        else:
            if prev[i]<stock[i]['now']:
                flag=up*times
                clr.set_cmd_color(FOREGROUND_BLACK|500)
            else:
                if prev[i]==stock[i]['now']:
                    flag=no*times
                else:
                    flag=down*times
                    clr.set_cmd_color(FOREGROUND_GREEN)
        #print stockname
        if stock[i]['now']>stock[i]['yestoday']:
            updown=u'↗'
        else:
            if stock[i]['now']<stock[i]['yestoday']:
                updown=u'↘'
            else:
                updown=u'→'

        prev[i]=stock[i]['now']
        if stock[i]['profit']>0:
			up2=up
        else:
			up2=down
        print "%s %s %6.2f %5.2f%%"%(stock[i]['name'],stock[i]['time'],stock[i]['now'],stock[i]['range']),updown,"total=%6d profit=%8.2f%s %-4.2f%% "%(stock[i]['true_total'],stock[i]['profit'],up2,stock[i]['profit_percent']),flag
        clr.reset_color()
    r = kbfunc()
    if r != 0:
        break 
    time.sleep(3)
    print '-'*50
    print ' '*50

