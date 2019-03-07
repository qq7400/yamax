from tkinter import *
from tkinter import ttk
import random
import time

from export import JsonCsv
from request import AmazonRequests
from dispose import AmazonDispose


class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.window_init()
        self.createWidgets()
        self.data = []
        self.requests = ''
        self.csv = JsonCsv()

    def window_init(self):
        self.master.title('Amazon评论获取工具   by 素笺 and 凌寒初见')
        # width, height = self.master.maxsize()
        # print(width, height)
        # self.master.geometry("{}x{}".format(960, 540))
        self.master.resizable(width=FALSE,height=FALSE)

    def createWidgets(self):
        # fm2
        self.fm2 = Frame(self)
        self.fm2_left = Frame(self.fm2)
        self.fm2_right = Frame(self.fm2)
        self.fm2_left_top = Frame(self.fm2_left)
        self.fm2_left_bottom = Frame(self.fm2_left)

        self.siteLabel = Label(self.fm2_left_top, text='站点')
        self.siteLabel.pack(side=LEFT, padx=10)

        self.siteBox = ttk.Combobox(self.fm2_left_top, state='readonly',width=17)
        self.siteBox.pack(side=LEFT)
        self.siteBox['value'] = ('US', 'JP', 'FR', 'ES', 'IT', 'MX', 'GB', 'UK', 'CA', 'DE', 'IN')
        self.siteBox.current(0)
        self.fm2_left_top.pack(side=TOP, pady=5)

        self.asinLabel = Label(self.fm2_left_bottom, text='asin')
        self.asinLabel.pack(side=LEFT, padx=10)

        self.asinEntry = Entry(self.fm2_left_bottom)
        self.asinEntry.pack(side=LEFT)
        self.fm2_left_bottom.pack(side=TOP, pady=5)
        self.fm2_left.pack(side=LEFT)

        self.startButton = Button(self.fm2_right, text='开始获取', command=self.start)
        self.startButton.pack()
        self.fm2_right.pack(side=LEFT, padx=10)

        self.fm2.pack(side=TOP, pady=10)

        # fm3
        self.fm3 = Frame(self)
        self.msg = Text(self.fm3)
        self.msg.pack()
        self.msg.config(state=DISABLED)
        self.fm3.pack(side=TOP, fill=X)

    def write_msg(self, msg):
        self.msg.config(state=NORMAL)
        self.msg.insert(END, '\n' + msg)
        self.msg.config(state=DISABLED)
        self.msg.see(END)

    def delete_msg(self):
        self.msg.config(state=NORMAL)
        self.msg.delete(0.0, END)
        self.msg.config(state=DISABLED)

    def start(self):
        self.delete_msg()
        self.startButton.config(state=DISABLED)
        site = self.siteBox.get()
        asin = self.asinEntry.get()
        if not asin:
            self.write_msg('asin 为空，请先输入asin')
            self.startButton.config(state=NORMAL)
            return
        self.write_msg('开始任务...，站点--{}，Asin--{}'.format(site, asin))
        #初始化请求类
        self.requests = AmazonRequests(site, asin)
        # 判断asin是否存在
        if asin:
            self.start_download()
        else:
            self.write_msg('asin不存在，请查看是否输入有误')
            self.startButton.config(state=NORMAL)

    def start_download(self):
        # 解析数据 并存储数据
        dispose = AmazonDispose(self.requests.getAmaoznData(), self.siteBox.get(), self.asinEntry.get())
        dicData = dispose.dispose()
        if dicData:
            self.csv.writerCsv(dicData)
        if dispose.isNextPage():
            time.sleep(random.randint(5, 10))
            self.start_download()
        else:
            self.csv.closeCsv()
            self.write_msg('评论获取完毕')
            self.startButton.config(state=NORMAL)


if __name__ == '__main__':
    app = Application()
    app.mainloop()