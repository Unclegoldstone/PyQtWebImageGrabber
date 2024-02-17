from PyQt6 import uic
from PyQt6.QtGui import QIcon, QPixmap
import sys
from PyQt6.QtWidgets import *
import os
import requests
from bs4 import BeautifulSoup
from PyQt6.QtCore import QCoreApplication

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36 Edg/87.0.664.47'
}


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        #默认属性
        self.path = "./Images/"
        self.picTypeUrl = "https://pic.netbian.com/4kdongman/" #图片类型的网址
        self.maxNum = 0 #抓取的图片数量
        self.keyword = ""
        self.loaded = 0 #已抓取的图片数量
        self.rand = False
        self.saveLocation = "" #保存文件的地址


        # 使用ui.loadUi加载ui文件
        ui = uic.loadUi("myWidget.ui",self)
        #设置窗口图标
        icon = QIcon(QPixmap("./icon/icon.png"))
        self.setWindowIcon(icon)  # 设置图标
        #固定ui大小
        self.setFixedSize(self.size())
        #绑定按钮
        self.BtnCartoon.clicked.connect(self.Btn_Cartoon)
        self.BtnBackGround.clicked.connect(self.Btn_BackGround)
        self.BtnGame.clicked.connect(self.Btn_Game)
        self.BtnGet.clicked.connect(self.Btn_GetPic)
        self.BtnScenery.clicked.connect(self.Btn_BtnScenery)

    def Btn_BtnScenery(self):
        self.picTypeUrl = "https://pic.netbian.com/4kfengjing/"
        print("已选图片类型为风景")
        self.LabelType.setText("风景")
        self.textEdit.append("已选择图片类型为: 风景")

    def Btn_Game(self):
        self.picTypeUrl = "https://pic.netbian.com/4kyouxi/"
        print("已选图片类型为游戏")
        self.LabelType.setText("游戏")
        self.textEdit.append("已选择图片类型为: 游戏")

    def Btn_BackGround(self):
        self.picTypeUrl = "https://pic.netbian.com/4kbeijing/"
        print("已选图片类型为背景")
        self.LabelType.setText("背景")
        self.textEdit.append("已选择图片类型为: 背景")

    def Btn_Cartoon(self): #动漫按钮
        self.picTypeUrl = "https://pic.netbian.com/4kdongman/"
        print("已选图片类型为动漫")
        self.LabelType.setText("动漫")
        self.textEdit.append("已选择图片类型为: 动漫")


    def GetPicLine(self):
        '''
        点击抓取后的一行的输出
        :return:  str : 要显示给用户的内容
        '''
        if self.keyword == "":  #关键词为空
            return "设置的关键词为空, 默认全部抓取全部类型的图片; 需要爬取的图片数量为 : " + str(self.maxNum)
        else:
            return "设置的关键词为: " + self.keyword +"; 需要爬取的图片数量为: " + str(self.maxNum)

    def Btn_GetPic(self):   #爬取图片按钮
        self.loaded = 0
        self.maxNum = self.spinBox.value()
        self.keyword = self.lineEdit.text()
        self.rand = False
        self.textEdit.append("随机抓取 : " + str(self.rand))
        self.textEdit.append(self.GetPicLine())
        self.textEdit.append("三秒后开始抓取...")
        if self.keyword == "": #关键词为空
            self.textEdit.append("图片将存放于./Images/Default/目录下")
            self.saveLocation = "./Images/Default/"
            self.Download_Default()

        else:
            self.textEdit.append("图片将存放于./Images/"+self.keyword+"目录下")
            try:
                os.makedirs("./Images/"+self.keyword)
            except:
                print("目标文件夹已存在")
            self.saveLocation = "./Images/"+self.keyword + "/"
            self.Download_Key()


    def contain_Key(self, tags : str):
        '''
        用来判断关键词是否存在
        :param tags: str 关键词
        :return: bool
        '''


    def craw_html(selfself, url):
        '''
        解析网页
        :param url:   请求地址
        :return:  解析后的网页源码
        '''
        # 请求网页
        responce = requests.get(url=url, headers=headers)
        responce.encoding = "gbk"
        return responce.text

    def getPage(self,html):
        '''
        获取网页页码数
        :param html:
        :return:
        '''
        # 实例化soup
        soup = BeautifulSoup(html, 'lxml')
        r = soup.select("div.page a")
        pages = r[-2].text
        print(pages)
        return int(pages)

    def download_img(self, src):  # 下载一页的图片内容
        '''
        下载图片
        :param src: 图片的相对路径(网址)
        :return:
        '''
        # 获取图片名称
        filename = os.path.basename(src)  # 文件名称
        print(filename)
        # 拼接地址
        location = self.saveLocation
        try:
            with open(self.saveLocation + f"{filename}", 'wb') as file:
                lineWord =  "("+ str(self.loaded + 1) + ")" +  " 图片: " + filename + " 下载成功"
                self.textEdit.append(lineWord)
                file.write(requests.get("https://pic.netbian.com" + src).content)
                QCoreApplication.processEvents() # 强制刷新界面

        except:
            print(src, "下载异常")

    def parse_html(self, html):
        # 实例化soup
        soup = BeautifulSoup(html, 'lxml')
        # 获取所有图片
        img_list = soup.select("ul.clearfix li a img")
        print(img_list)
        for img in img_list:
            img_link = img['src']  # 图片地址
            # print(img['src'])
            if self.loaded >= self.maxNum: #抓取数量超过了
                print("规定数额已抓取完成")
                break
            self.download_img(img_link)
            self.loaded = self.loaded + 1
            print("已抓取: ", self.loaded, "张图片")

    def parse_html_key(self, html):
        # 实例化soup
        soup = BeautifulSoup(html, 'lxml')
        # 获取所有图片
        img_list = soup.select("ul.clearfix li a img")
        print(img_list)
        for img in img_list:
            img_link = img['src']  # 图片地址
            tags = img.get('alt') # 关键词
            if self.keyword not in tags:
                continue
            if self.loaded >= self.maxNum: #抓取数量超过了
                print("规定数额已抓取完成")
                break
            self.download_img(img_link)
            self.loaded = self.loaded + 1
            print("已抓取: ", self.loaded, "张图片")

    def Download_Default(self):
        '''
        :param n: 需要爬取的图片数量
        :return:
        '''
        url = self.picTypeUrl
        html = self.craw_html(url)
        pageNum = self.getPage(html)
        print("抓取的网页为:", url)
        print("需要抓取的数量为:", self.maxNum)
        if self.rand == False: #顺序抓取
            print("正在抓取第1页")
            self.parse_html(html)
            for i in range(2, self.getPage(html)):
                print("正在抓取第",i,"页")
                if self.loaded >= self.maxNum:
                    break
                self.parse_html(self.craw_html(f"https://pic.netbian.com/4kdongman/index_{i}.html"))

            if self.loaded < self.maxNum:
                self.textEdit.append("资源获取处没有更多的图啦")
        else:
            pass

    def Download_Key(self):
        url = self.picTypeUrl
        html = self.craw_html(url)
        pageNum = self.getPage(html)
        print("抓取的网页为:", url)
        print("需要抓取的数量为:", self.maxNum)
        if self.rand == False: #顺序抓取
            print("正在抓取第1页")
            self.parse_html_key(html)
            for i in range(2, self.getPage(html)):
                print("正在抓取第",i,"页")
                if self.loaded >= self.maxNum:
                    break
                self.parse_html_key(self.craw_html(f"https://pic.netbian.com/4kdongman/index_{i}.html"))

            if self.loaded < self.maxNum:
                self.textEdit.append("资源获取处没有更多的图啦")
        else:
            pass

if __name__ == "__main__":
    app = QApplication([])
    # 创建主窗口实例
    main_window = MyWidget()
    #显示主窗口
    main_window.show()
    sys.exit(app.exec())