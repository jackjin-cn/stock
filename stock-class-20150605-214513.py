#coding: UTF-8
import math
import time
import string
import sys,os
import io, re, json, base64
import webbrowser
import urllib2
import datetime
import csv
import win32con
import wxversion
wxversion.select('3.0')
import wx
import msvcrt
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
class stock:
    yongjin=0.0006 #拥金
    yinhuasui=0.001#印花税率
    max_total_profit=0
    yestoday_total_profit=0

    def __init__(self,stock_code,buy,number,date):
        self.prev=0
        self.stock={}
        self.exchange = "sz" if (int(stock_code) // 100000 == 3) else "sh"
        self.query="http://hq.sinajs.cn/list="
        self.query=self.query+self.exchange+stock_code
        self.stock['code']=stock_code
        self.stock['buy']=string.atof(buy)
        self.stock['number']=string.atoi(number)
        self.stock['buy_date']=date.strip()
        self.stock['max_profit']=0

    def querystock(self):
        self.stdout = urllib2.urlopen(self.query)
        self.html=self.stdout.read()
        self.tempData = re.search('''(")(.+)(")''',self.html).group(2)
        self.stockinfo = self.tempData.split(",")
        self.sell=string.atof(self.stockinfo[3])

        self.stock['name']=self.stockinfo[0]
        self.stock['yestoday']=string.atof(self.stockinfo[2])
        self.stock['now']=string.atof(self.stockinfo[3])
        self.stock['max']=string.atof(self.stockinfo[4])
        self.stock['min']=string.atof(self.stockinfo[5])
        self.stock['time']=self.stockinfo[31]
        self.stock['date']=self.stockinfo[30]
        self.calc_days()
        self.stock['range_percent']=(self.stock['now']/self.stock['yestoday']-1)*100
        #print (self.stock['now']/self.stock['yestoday']-1)*100
        self.calc_profit()#利润
        self.stock['range']=self.stock['now']-self.stock['yestoday']
        return

    def calc_profit(self):
        #==========相关费率
        self.buy_fee=self.stock['buy']*self.stock['number']*self.yongjin
        self.sell_fee=self.stock['now']*self.stock['number']*(self.yongjin+self.yinhuasui)
        self.souxufei=self.stock['number']*.0006

        #计算 利润-利润率
        self.stock['cost']=self.stock['buy']*self.stock['number']+self.buy_fee+self.souxufei
        self.stock['profit']=(self.stock['now']-self.stock['buy'])*self.stock['number']-self.buy_fee-self.sell_fee-2*self.souxufei
        self.stock['max_profit']=self.stock['number']*(self.stock['max']*.9984-self.stock['buy']*1.0006-2*stock.yongjin)
        self.stock['yestoday_profit']=self.stock['number']*(self.stock['yestoday']*.9984-self.stock['buy']*1.0006-2*stock.yongjin)

        self.stock['profit_percent']=self.stock['profit']/(self.stock['cost'])*100#利润率
        self.stock['year_profit_percent']=self.stock['profit_percent']/self.stock['hold_days']*365/12
        self.stock['true_total']=self.stock['now']*self.stock['number']-self.sell_fee-self.souxufei#真市值

        return

    def display(self):
        self.times=2
        self.result_string=''
        self.max=self.stock['now']
        self.up='↗'
        self.down='↘'
        self.no=' '
        self.flag=''

        self.up=self.up.decode('utf-8').encode('gbk')
        self.no=self.no.decode('utf-8').encode('gbk')
        self.flag=self.flag.decode('utf-8').encode('gbk')
        self.down=self.down.decode('utf-8').encode('gbk')
        if self.stock['now']==self.stock['max']:
            self.flag='☆'.decode('utf-8').encode('gbk')*self.times
            self.fc="Yellow"
            self.bk="Black"

        else:
            if self.prev<self.stock['now']:    #上升
                self.flag=self.up*times
                self.fc='Yellow'
                self.bk='red'
                #clr.set_cmd_color(FOREGROUND_BLACK|500)
            else:
                if self.prev==self.stock['now']:
                    self.flag=self.no*self.times
                    self.fc='White'
                    self.bk='Black'
                else:
                    self.flag=self.down*self.times #下降
                    self.fc='Green'
                    self.bk='Blue'

        if self.stock['now']>self.stock['yestoday']:
            self.updown=self.up
        else:
            if self.stock['now']<self.stock['yestoday']:
                self.updown=self.down
            else:
                self.updown=self.no

        self.prev=self.stock['now']
        if self.stock['profit']>0:
            self.up2=self.up
        else:
            self.up2=self.down
        self.result_string="%s %s "%(self.stock['name'],self.stock['time'])
        self.result_string=self.result_string+"{:>6.2f}({:<6.2f}{:<6.2f}) {:5.2f} {:5.2f}%".format(self.stock['now'],self.stock['max'],self.stock['yestoday'],self.stock['range'],self.stock['range_percent'])
        self.result_string=self.result_string+self.updown
        self.result_string=self.result_string+' 市值'.decode('utf-8').encode('gbk')+'={:>6.0f} {}={:>8.2f}'.format(self.stock['true_total'],' 利润'.decode('utf-8').encode('gbk'),self.stock['profit']) 
        self.result_string=self.result_string+"{} {:>5.2f}%{} {:7.2f}% {:3d}d\n".format(self.up2,self.stock['profit_percent'],self.flag,self.stock['year_profit_percent'],self.stock['hold_days'])
        return self.result_string




    def calc_days(self):
        #nowday,olday is string 'xxxx-xx-xx"
        self.d2=time.strptime(self.stock['buy_date'],'%Y-%m-%d') 
        self.dd1= datetime.datetime.now()
        self.dd2= datetime.datetime(self.d2.tm_year,self.d2.tm_mon,self.d2.tm_mday)
        self.stock['hold_days']= (self.dd1-self.dd2).days
        return

# http://hq.sinajs.cn/list=sh600000

# http://hq.sinajs.cn/list=sz000913
#var hq_str_sh601006="大秦铁路, 27.55, 27.25, 26.91, 27.55, 26.20, 26.91, 26.92,
#                     22114263, 589824680, 4695, 26.91, 57590, 26.90, 14700, 26.89,
#                     14300,6.88, 15100, 26.87, 3100, 26.92, 8900, 26.93, 14230,
#                     26.94, 25150, 26.95, 15220, 26.96, 2008-01-11, 15:05:32";
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



#**********  main   **************
#**********gui

class static(wx.Frame):
    def _init_(self):#,parent):
    #app = wx.App(False)
        frame = wx.Frame(self,title=u"mystock",size=(600,100))
        #text01=wx.StaticText(frame,-1,'bb',style=wx.TE_MULTILINE,size=(600,30))#邮件标题
        frame.Show()
        app.MainLoop()

def draw_static(a,txt,fc,bc):
    
    a.SetForegroundColour(fc)
    a.SetBackgroundColour(bc)
    a.Label=txt
    return

def OnStock(event):
    
    repeat=len(line)/format_number
    times=2
    stock_number=10
    ss=['']*stock_number
    stock.max_total_profit=0
    stock.yestoday_total_profit=0
    #stock=[{}]*stock_number  #最多支持几支股票查询
   
    pp=''
    total_profit=0
    total_cost=0
    total_hold=0
    
    for i in range(repeat):
        stock_inst[i].querystock()
        ss[i]=stock_inst[i].display()
        total_profit=total_profit+stock_inst[i].stock['profit']
        total_cost=total_cost+stock_inst[i].stock['cost']
        total_hold=total_hold+stock_inst[i].stock['true_total']
        pp=ss[i]
        stock.max_total_profit=stock.max_total_profit+stock_inst[i].stock['max_profit']
        stock.yestoday_total_profit=stock.yestoday_total_profit+stock_inst[i].stock['yestoday_profit']
        draw_static(text[i],pp,stock_inst[i].fc,stock_inst[i].bk)
    souyilv=total_profit/total_cost*100
    pp="%s=%7.0f max=(%-7.0f) yes=%.1f %6.2f%% %s=%10.2f"%('收益'.decode('utf-8').encode('gbk'),total_profit,stock.max_total_profit,stock.yestoday_total_profit,souyilv,'总市值'.decode('utf-8').encode('gbk'),total_hold)
    draw_static(text[repeat],pp,'white','Black')
    #.Label=pp+"%s=%7.0f %6.2f%% %s=%10.2f"%('收益'.decode('utf-8').encode('gbk'),total_profit,souyilv,'总市值'.decode('utf-8').encode('gbk'),total_hold)


def OnClose(event):
    print "close"
    repeat=len(line)/format_number
    times=2
    stock_number=10
    ss=['']*stock_number
    stock.max_total_profit=0
    stock.yestoday_total_profit=0
    #stock=[{}]*stock_number  #最多支持几支股票查询
    csvfile=open('sr.csv','wb+')
    fw=csv.writer(csvfile,dialect='excel')#,quoting=csv.QUOTE_MINIMAL)
    fw.writerow(['股票名称'.decode('utf-8').encode('gbk'),'时间'.decode('utf-8').encode('gbk'),'现价'.decode('utf-8').encode('gbk'),'最高价'.decode('utf-8').encode('gbk'),'昨收'.decode('utf-8').encode('gbk')])
    csvfile.close()
    return
    pp=''
    total_profit=0
    total_cost=0
    
    total_hold=0

    for i in range(repeat):
        stock_inst[i].querystock()
        ss[i]=stock_inst[i].display()
        total_profit=total_profit+stock_inst[i].stock['profit']
        total_cost=total_cost+stock_inst[i].stock['cost']
        total_hold=total_hold+stock_inst[i].stock['true_total']
        pp=ss[i]
        stock.max_total_profit=stock.max_total_profit+stock_inst[i].stock['max_profit']
        stock.yestoday_total_profit=stock.yestoday_total_profit+stock_inst[i].stock['yestoday_profit']
        fb.writelines(pp)
        #draw_static(text[i],pp,stock_inst[i].fc,stock_inst[i].bk)
    souyilv=total_profit/total_cost*100
    pp="%s=%7.0f max=(%-7.0f) yes=%.1f %6.2f%% %s=%10.2f"%('收益'.decode('utf-8').encode('gbk'),total_profit,stock.max_total_profit,stock.yestoday_total_profit,souyilv,'总市值'.decode('utf-8').encode('gbk'),total_hold)
    fb.writelines(pp)
    fb.close()
    #draw_static(text[repeat],pp,'white','Black')
    

#==========设置买入＝＝＝＝＝＝＝
format_number=5
times=2
#global max_total_profit=0
fb=open('stock.txt','r')
line=fb.readlines()
fb.close()
stock_inst=['']*10
repeat=len(line)/format_number
for i in range(repeat):
    b=(line[1+i*format_number])
    n=(line[2+i*format_number])
    c=line[0+i*format_number]
    d=line[3+i*format_number]
    stock_inst[i]=stock(c,b,n,d)

app=wx.App()
mytitle=u"'JJB' stock analisy system V1.05 "+u'(2015-06-05)'
w_weight=950
w_height=150
s_height=20
frame = wx.Frame(parent=None,title=mytitle,size=(w_weight,w_height),style=wx.DEFAULT_FRAME_STYLE|wx.STAY_ON_TOP)
other=2
text=['']*(repeat+2)
for i in range(repeat+other):
    #print 0,s_height*(i-1)
    text[i]=wx.StaticText(frame,-1,mytitle,style=wx.TE_MULTILINE,pos=(0,s_height*(i)),size=(w_weight,s_height))#邮件标题
    text[i].SetForegroundColour("yellow")
    text[i].SetBackgroundColour("Black")
    font=wx.Font(13,wx.ROMAN,wx.NORMAL,wx.NORMAL,False,'Consolas')
    text[i].SetFont(font)
timer=wx.Timer()
timer.Start(1000)
timer.Bind(wx.EVT_TIMER,OnStock)
frame.Bind(wx.EVT_WINDOW_DESTROY,OnClose)
frame.Show()
app.MainLoop()

