@ -1,1092 +0,0 @@
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QAction
from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QLineEdit, QComboBox
from PyQt5.QtWidgets import QStackedWidget
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QLabel, QSizePolicy
from PyQt5.QtWidgets import QDesktopWidget
from PyQt5.QtWidgets import QToolBar
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QBrush, QFont
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize
import sys
import subprocess
import pandas as pd
import socket
import Constants



font = QFont()
font.setFamily("黑体")
font.setPointSize(12)  # 设置字体大小
font.setBold(True)  # 设置字体加粗


toolbarTop_style = """
    QToolBar {
        border: 2px solid gray;
        border-radius: 10px;
        padding: 10px;
        background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                          stop: 0 #f6f7fa, stop: 1 #dadbde);
    }
    QToolBar:hover {
        background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                          stop: 0 #dadbde, stop: 1 #f6f7fa);
    }

    QToolBar:pressed {
        background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                          stop: 0 #f6f7fa, stop: 1 #dadbde);
        border-style: inset;
    }
"""


toolbarBottom_style="""
    QToolBar {
        border: 2px solid gray;
        border-radius: 10px;
        padding: 10px;
        background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                          stop: 0 #f6f7fa, stop: 1 #dadbde);
    }
    QToolBar:hover {
        background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                          stop: 0 #dadbde, stop: 1 #f6f7fa);
    }

    QToolBar:pressed {
        background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                          stop: 0 #f6f7fa, stop: 1 #dadbde);
        border-style: inset;
    }
"""

butt_style = """
    QPushButton {
        border: 2px solid gray;
        border-radius: 10px;
        padding: 10px;
        background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                          stop: 0 #f6f7fa, stop: 1 #dadbde);
    }

    QPushButton:hover {
        background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                          stop: 0 #dadbde, stop: 1 #f6f7fa);
    }

    QPushButton:pressed {
        background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                          stop: 0 #f6f7fa, stop: 1 #dadbde);
        border-style: inset;
    }
"""

label_style = """
    QLineEdit {
        border: 2px solid gray;
        border-radius: 10px;
        padding: 10px;}
"""

combo_style = """
    QComboBox {
        border: 2px solid gray;
        border-radius: 10px;
        padding: 10px;}
"""

ip = Constants.IP
msg = ''

def start_server(ip,msg):
	
	# 创建socket对象
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# 绑定IP地址和端口号
	ip = ""
	server_address = (ip,8266)
	server_socket.bind(server_address)

	# 设置最大连接数
	server_socket.listen(15)

	# 接受客户端连接
	clients = []
	for i in range(9):
		client_socket, client_address = server_socket.accept()
		print("client_socket:",client_socket)
		print("client_address:",client_address)
		clients.append(client_socket)
		print('客户端 {} 已连接'.format(client_address))


	# 关闭客户端连接
	for client in clients:
		message = msg.encode()
		client.sendall(message)
		print(message)
		client.close()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 设置窗口背景颜色
        palette = self.palette()
        palette.setColor(QPalette.Background, QColor(232,232,232))  # 设置为白色背景
        self.setPalette(palette)

        # 获取屏幕的宽高信息
        screen = QDesktopWidget().screenGeometry()
        width, height = screen.width(), screen.height()

        # 设置窗口大小为屏幕的 80%
        self.resize(int(width * 0.3), int(height * 0.8))

        # 设置窗口样式为无边框
        self.setWindowFlags(Qt.FramelessWindowHint)

        # 创建一个工具栏
        toolbar_top = QToolBar()
        self.addToolBar(toolbar_top)

        # 创建工具栏上的按钮
        action1 = QAction(QIcon("icon\\pen.png"),'秘书小姐', self)
        action2 = QAction(QIcon("icon\\home.png"),'管家助手', self)

        # 将按钮添加到工具栏
        toolbar_top.addAction(action1)
        toolbar_top.addAction(action2)
        
        # 设置按钮图标的大小为64x64像素
        toolbar_top.setIconSize(QSize(int(width*0.08), 30))
        # 设置按钮的位置为图标和文本并排
        toolbar_top.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        toolbar_top.setStyleSheet(toolbarTop_style)

        action1.setFont(font)
        action2.setFont(font)
        

        action1.triggered.connect(self.to_Mis)
        action2.triggered.connect(self.to_Assis)
        

        toolbar_bottom = QToolBar()

        # 设置按钮图标的大小为64x64像素
        toolbar_bottom.setIconSize(QSize(int(width*0.05), 30))
        # 设置按钮的位置为图标和文本并排
        toolbar_bottom.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        # 添加按钮
        action_set = QAction(QIcon("icon\\pen.png"),"设置", self)
        action_my = QAction(QIcon("icon\\pen.png"),"我的", self)
        action_exit = QAction(QIcon("icon\\close.svg"),'结束程序', self)
        action_set.setFont(font)
        action_my.setFont(font)
        action_exit.setFont(font)
        toolbar_bottom.addAction(action_set)
        toolbar_bottom.addAction(action_my)
        toolbar_bottom.addAction(action_exit)

        action_set.triggered.connect(self.to_set)
        action_my.triggered.connect(self.to_my)
        action_exit.triggered.connect(self.close)


        toolbar_bottom.setStyleSheet(toolbarBottom_style)

        # 设置工具栏位置为底部
        self.addToolBar(Qt.BottomToolBarArea, toolbar_bottom)


    def to_Mis(self):
        stack.setCurrentIndex(1)		

    def to_Assis(self):
        stack.setCurrentIndex(2)

    def to_set(self):
        stack.setCurrentIndex(3)

    def to_my(self):
        stack.setCurrentIndex(4)

class Miss_secretary(QWidget):
	"""docstring for Misssecrety"""
	def __init__(self):
		super(Miss_secretary, self).__init__()
		self.initUI()

	def initUI(self):
		# 加载背景图片
		img = "icon\\bg0.jpg"
		pixmap = QPixmap(img)

		# 创建标签并设置背景图片
		background = QLabel(self)
		background.setPixmap(pixmap)
		
		# 调整标签大小以适应窗口
		background.setGeometry(0, 0, pixmap.width(), pixmap.height())
		
		# 将标签放置到窗口的底层
		background.lower()

		button1 = QPushButton("收邮件", self)
		button1.setGeometry(200,100,200,50)
		button1.setFont(font)
		button1.setStyleSheet(butt_style)
		button1.clicked.connect(self.rsv_email)

		button2 = QPushButton("发邮件", self)
		button2.setGeometry(200,180,200,50)
		button2.setFont(font)
		button2.setStyleSheet(butt_style)
		button2.clicked.connect(self.sd_email)

		button3 = QPushButton("添加提醒", self)
		button3.setGeometry(200,260,200,50)
		button3.setFont(font)
		button3.setStyleSheet(butt_style)
		button3.clicked.connect(self.add_remind)

		button4 = QPushButton("翻译成英文", self)
		button4.setGeometry(200,340,200,50)
		button4.setFont(font)
		button4.setStyleSheet(butt_style)
		button4.clicked.connect(self.trans)

		button5 = QPushButton("返回主页", self)
		button5.setGeometry(200,450,200,50)
		button5.setFont(font)
		button5.setStyleSheet(butt_style)
		button5.clicked.connect(self.close)

	def add_remind(self):
		stack.setCurrentIndex(5)

	def rsv_email(self):
		subprocess.Popen(["python", "ReceiveEmail.py"])

	def sd_email(self):
		subprocess.Popen(["python", "SendEmail.py"])

	def trans(self):
		subprocess.Popen(["python", "Translators.py"])
		
class home_Assistant(QWidget):
	"""docstring for Misssecrety"""
	def __init__(self):
		super(home_Assistant, self).__init__()
		self.initUI()

	def initUI(self):
		# 加载背景图片
		img = "icon\\bg0.jpg"
		pixmap = QPixmap(img)

		# 创建标签并设置背景图片
		background = QLabel(self)
		background.setPixmap(pixmap)
		
		# 调整标签大小以适应窗口
		background.setGeometry(0, 0, pixmap.width(), pixmap.height())
		
		# 将标签放置到窗口的底层
		background.lower()

		button1 = QPushButton("学习动作", self)
		button1.setGeometry(200,100,200,50)
		button1.setFont(font)
		button1.setStyleSheet(butt_style)
		button1.clicked.connect(self.stdy_actions)

		button2 = QPushButton("移动", self)
		button2.setGeometry(200,180,200,50)
		button2.setFont(font)
		button2.setStyleSheet(butt_style)
		button2.clicked.connect(self.movepage)

		button3 = QPushButton("抓取", self)
		button3.setGeometry(200,260,200,50)
		button3.setFont(font)
		button3.setStyleSheet(butt_style)
		button3.clicked.connect(self.catch_hand)

		button4 = QPushButton("吸取", self)
		button4.setGeometry(200,340,200,50)
		button4.setFont(font)
		button4.setStyleSheet(butt_style)
		button4.clicked.connect(self.pump_hand)

		button6 = QPushButton("家电控制中心", self)
		button6.setGeometry(200,420,200,50)
		button6.setFont(font)
		button6.setStyleSheet(butt_style)
		button6.clicked.connect(self.ctrllorpage)

		button5 = QPushButton("返回主页", self)
		button5.setGeometry(200,550,200,50)
		button5.setFont(font)
		button5.setStyleSheet(butt_style)
		button5.clicked.connect(self.close)


	def stdy_actions(self):
		subprocess.Popen(["python", "MCap2CSV.py"])

	def ctrllorpage(self):
		stack.setCurrentIndex(10)		

	def movepage(self):
		stack.setCurrentIndex(11)

	def catch_hand(self):
		subprocess.Popen(["python", "Yolowupinfenleizhuaqu.py"])

	def pump_hand(self):
		print(["python", "pump_hand.py"])
		

class main_page(QWidget):
	def __init__(self):
		super().__init__()

		self.name_label = QLabel(" 视睿机器人 联系我们：info@cherrymv.com\n 更多功能及教程请关注\n 微信公众号：CHERRY樱桃视频 一个越看越聪明的频道",self)
		self.name_label.setGeometry(100,600,480,50)
		self.name_label.setFont(font)

class settings(QWidget):
	"""docstring for settings"""
	def __init__(self):
		super().__init__()

		# 加载背景图片
		img = "icon\\bg0.jpg"
		pixmap = QPixmap(img)

		# 创建标签并设置背景图片
		background = QLabel(self)
		background.setPixmap(pixmap)
		
		# 调整标签大小以适应窗口
		background.setGeometry(0, 0, pixmap.width(), pixmap.height())
		
		# 将标签放置到窗口的底层
		background.lower()

		self.shuoming_label = QLabel("点击按钮打开配置文件，按照说明填写对应内容并保存",self)
		self.shuoming_label.setStyleSheet("color: white")
		self.shuoming_label.setGeometry(50,150,480,50)
		self.shuoming_label.setFont(font)

		self.open_button = QPushButton("打开配置文件",self)
		self.open_button.setGeometry(50,300,480,50)
		self.open_button.setFont(font)
		self.open_button.setStyleSheet(butt_style)
		self.open_button.clicked.connect(self.setting_file)


		self.button5 = QPushButton("返回主页", self)
		self.button5.setGeometry(200,620,200,50)
		self.button5.setFont(font)
		self.button5.setStyleSheet(butt_style)
		self.button5.clicked.connect(self.close)


	def setting_file(self):
		subprocess.Popen(["notepad", "Constants.py"])
		
class account_info(QWidget):
	"""docstring for account_info"""
	def __init__(self):
		super(account_info, self).__init__()


		self.name_label = QLabel("此版本为单机版，不需要联网及账号登陆\n请放心配置个人信息！", self)
		self.name_label.setGeometry(120,600,480,50)
		self.name_label.setFont(font)

		
		label = QLabel(self)
		pixmap = QPixmap('icon/qrcode.jpg')  
		label.setPixmap(pixmap)
		label.setGeometry(120,50,480,480)
		
class add_reminder(QWidget):
	"""docstring for settings"""
	def __init__(self):
		super().__init__()

		# 加载背景图片
		img = "icon\\bg0.jpg"
		pixmap = QPixmap(img)

		# 创建标签并设置背景图片
		background = QLabel(self)
		background.setPixmap(pixmap)
		
		# 调整标签大小以适应窗口
		background.setGeometry(0, 0, pixmap.width(), pixmap.height())
		
		# 将标签放置到窗口的底层
		background.lower()

		self.thstime_label = QLabel("发生频率",self)
		self.thstime_label.setStyleSheet("color: white")
		self.thstime_label.setGeometry(50,150,480,50)
		self.thstime_label.setFont(font)
		self.comboBox = QComboBox(self)
		self.comboBox.setStyleSheet(combo_style)
		self.comboBox.setFont(font)
		self.comboBox.addItem("--请选择--")
		self.comboBox.addItem("每天")
		self.comboBox.addItem("每周")
		self.comboBox.addItem("每月")
		self.comboBox.addItem("每年")
		self.comboBox.setGeometry(50, 200, 480, 50)


		self.content_label = QLabel("设置提醒内容",self)
		self.content_label.setStyleSheet("color: white")
		self.content_label.setGeometry(50,50,480,50)
		self.content_label.setFont(font)
		self.content_line_edit = QLineEdit(self)
		self.content_line_edit.setStyleSheet(label_style)
		self.content_line_edit.setGeometry(50,100,480,50)

		self.rtimey_label = QLabel("设置提醒日期:",self)
		self.rtimey_label.setStyleSheet("color: white")
		self.rtimey_label.setGeometry(50,300,480,50)
		self.rtimey_label.setFont(font)
		self.rtimey_line_edit = QLineEdit("日期格式：0000-00-00",self)
		self.rtimey_line_edit.setGeometry(50,350,480,50)
		self.rtimey_line_edit.setStyleSheet(label_style)

		self.rtimeh_label = QLabel("设置提醒时间:",self)
		self.rtimeh_label.setStyleSheet("color: white")
		self.rtimeh_label.setGeometry(50,400,480,50)
		self.rtimeh_label.setFont(font)
		self.rtimeh_line_edit = QLineEdit("时间格式：00:00",self)
		self.rtimeh_line_edit.setGeometry(50,450,480,50)
		self.rtimeh_line_edit.setStyleSheet(label_style)

		self.save_button = QPushButton("保存",self)
		self.save_button.setGeometry(200,540,200,50)
		self.save_button.setFont(font)
		self.save_button.setStyleSheet(butt_style)
		self.save_button.clicked.connect(self.save_information)

		self.button5 = QPushButton("返回主页", self)
		self.button5.setGeometry(200,620,200,50)
		self.button5.setFont(font)
		self.button5.setStyleSheet(butt_style)
		self.button5.clicked.connect(self.close)
		
		layout = QVBoxLayout()	

		self.setLayout(layout)

	def save_information(self):

		# 添加记录至文本
		content = self.content_line_edit.text()
		#thstime = self.thstime_line_edit.text()
		thstime = self.comboBox.currentText()
		reminder_date = self.rtimey_line_edit.text()         
		reminder_time = self.rtimeh_line_edit.text()   
		makelist = {'事件':[content], '频率':[thstime], '提醒日期':[reminder_date], '提醒时间':[reminder_time]}
		df = pd.DataFrame(makelist)
		df.to_csv('../reminders.csv', mode='a',encoding='utf-8', index=False, header=False)

		self.content_line_edit.clear()
		self.comboBox.setCurrentIndex(0)
		self.rtimey_line_edit.clear()
		self.rtimeh_line_edit.clear()

class electric_ctrl(QWidget):
	"""docstring for electric_ctrl"""
	def __init__(self):
		super(electric_ctrl, self).__init__()

		self.initUI()


	def initUI(self):
		# 加载背景图片
		img = "icon\\bg0.jpg"
		pixmap = QPixmap(img)

		# 创建标签并设置背景图片
		background = QLabel(self)
		background.setPixmap(pixmap)
		
		# 调整标签大小以适应窗口
		background.setGeometry(0, 0, pixmap.width(), pixmap.height())
		
		# 将标签放置到窗口的底层
		background.lower()

		button1 = QPushButton("灯光", self)
		button1.setGeometry(200,100,200,50)
		button1.setFont(font)
		button1.setStyleSheet(butt_style)
		button1.clicked.connect(self.lightpage)
		
		button2 = QPushButton("空调", self)
		button2.setGeometry(200,180,200,50)
		button2.setFont(font)
		button2.setStyleSheet(butt_style)
		button2.clicked.connect(self.airpage)

		button3 = QPushButton("影音", self)
		button3.setGeometry(200,260,200,50)
		button3.setFont(font)
		button3.setStyleSheet(butt_style)
		button3.clicked.connect(self.vpage)

		button4 = QPushButton("烹饪", self)
		button4.setGeometry(200,340,200,50)
		button4.setFont(font)
		button4.setStyleSheet(butt_style)
		button4.clicked.connect(self.kichpage)

		button5 = QPushButton("返回主页", self)
		button5.setGeometry(200,450,200,50)
		button5.setFont(font)
		button5.setStyleSheet(butt_style)
		button5.clicked.connect(self.close)

	def lightpage(self):
		stack.setCurrentIndex(6)

	def airpage(self):
		stack.setCurrentIndex(7)

	def vpage(self):
		stack.setCurrentIndex(8)

	def kichpage(self):
		stack.setCurrentIndex(9)

class light_ctrl(QWidget):
	"""docstring for light_ctrl"""
	def __init__(self):
		super(light_ctrl, self).__init__()

		self.initUI()

	def initUI(self):
		# 加载背景图片
		img = "icon\\bg0.jpg"
		pixmap = QPixmap(img)

		# 创建标签并设置背景图片
		background = QLabel(self)
		background.setPixmap(pixmap)
		
		# 调整标签大小以适应窗口
		background.setGeometry(0, 0, pixmap.width(), pixmap.height())
		
		# 将标签放置到窗口的底层
		background.lower()

		button1 = QPushButton("进门", self)
		button1.setGeometry(50,100,200,50)
		button1.setFont(font)
		button1.setStyleSheet(butt_style)
		button1.clicked.connect(self.light_door)

		button2 = QPushButton("客厅", self)
		button2.setGeometry(50,180,200,50)
		button2.setFont(font)
		button2.setStyleSheet(butt_style)
		button2.clicked.connect(self.light_livingroom)

		button3 = QPushButton("主卧", self)
		button3.setGeometry(50,260,200,50)
		button3.setFont(font)
		button3.setStyleSheet(butt_style)
		button3.clicked.connect(self.light_bdroom0)

		button4 = QPushButton("客卧", self)
		button4.setGeometry(50,340,200,50)
		button4.setFont(font)
		button4.setStyleSheet(butt_style)
		button4.clicked.connect(self.light_bdroom1)

		button11 = QPushButton("书房", self)
		button11.setGeometry(50,420,200,50)
		button11.setFont(font)
		button11.setStyleSheet(butt_style)
		button11.clicked.connect(self.light_bkroom)

		button5 = QPushButton("返回主页", self)
		button5.setGeometry(200,600,200,50)
		button5.setFont(font)
		button5.setStyleSheet(butt_style)
		button5.clicked.connect(self.close)

		button6 = QPushButton("厨房", self)
		button6.setGeometry(320,100,200,50)
		button6.setFont(font)
		button6.setStyleSheet(butt_style)
		button6.clicked.connect(self.light_kitchen)
		
		button7 = QPushButton("主卫", self)
		button7.setGeometry(320,180,200,50)
		button7.setFont(font)
		button7.setStyleSheet(butt_style)
		button7.clicked.connect(self.light_bthroom0)

		button8 = QPushButton("次卫", self)
		button8.setGeometry(320,260,200,50)
		button8.setFont(font)
		button8.setStyleSheet(butt_style)
		button8.clicked.connect(self.light_bthroom1)

		button9 = QPushButton("餐厅", self)
		button9.setGeometry(320,340,200,50)
		button9.setFont(font)
		button9.setStyleSheet(butt_style)
		button9.clicked.connect(self.light_dinning)

		button10 = QPushButton("阳台", self)
		button10.setGeometry(320,420,200,50)
		button10.setFont(font)
		button10.setStyleSheet(butt_style)
		button10.clicked.connect(self.light_balcony)

		button11 = QPushButton("返回控制中心", self)
		button11.setGeometry(200,500,200,50)
		button11.setFont(font)
		button11.setStyleSheet(butt_style)
		button11.clicked.connect(self.bk2ctrlpage)

	def bk2ctrlpage(slef):
		stack.setCurrentIndex(10)

	def light_door(self):
		self.msg = "l0"
		start_server(ip,msg=self.msg)

	def light_livingroom(self):
		self.msg = "l1"
		start_server(ip,msg=self.msg)

	def light_bdroom0(self):
		self.msg = "l2"
		start_server(ip,msg=self.msg)

	def light_bdroom1(self):
		self.msg = "l3"
		start_server(ip,msg=self.msg)

	def light_kitchen(self):
		self.msg = "l4"
		start_server(ip,msg=self.msg)

	def light_bthroom0(self):
		self.msg = "l5"
		start_server(ip,msg=self.msg)

	def light_bthroom1(self):
		self.msg = "l6"
		start_server(ip,msg=self.msg)

	def light_dinning(self):
		self.msg = "l7"
		start_server(ip,msg=self.msg)

	def light_balcony(self):
		self.msg = "l8"
		start_server(ip,msg=self.msg)

	def light_bkroom(self):
		self.msg = "l9"
		start_server(ip,msg=self.msg)
		


class air_ctrl(QWidget):
	"""docstring for air_ctrl"""
	def __init__(self):
		super(air_ctrl, self).__init__()

		self.initUI()


	def initUI(self):
		# 加载背景图片
		img = "icon\\bg0.jpg"
		pixmap = QPixmap(img)

		# 创建标签并设置背景图片
		background = QLabel(self)
		background.setPixmap(pixmap)
		
		# 调整标签大小以适应窗口
		background.setGeometry(0, 0, pixmap.width(), pixmap.height())
		
		# 将标签放置到窗口的底层
		background.lower()

		self.button1 = QPushButton("书房", self)
		self.button1.setGeometry(200,100,200,50)
		self.button1.setFont(font)
		self.button1.setStyleSheet(butt_style)
		self.button1.clicked.connect(self.air_bkroom)

		self.button2 = QPushButton("客厅", self)
		self.button2.setGeometry(200,180,200,50)
		self.button2.setFont(font)
		self.button2.setStyleSheet(butt_style)
		self.button2.clicked.connect(self.air_livingroom)

		self.button3 = QPushButton("主卧", self)
		self.button3.setGeometry(200,260,200,50)
		self.button3.setFont(font)
		self.button3.setStyleSheet(butt_style)
		self.button3.clicked.connect(self.air_bdroom0)

		self.button4 = QPushButton("客卧", self)
		self.button4.setGeometry(200,340,200,50)
		self.button4.setFont(font)
		self.button4.setStyleSheet(butt_style)
		self.button4.clicked.connect(self.air_bdroom1)

		button5 = QPushButton("返回主页", self)
		button5.setGeometry(200,600,200,50)
		button5.setFont(font)
		button5.setStyleSheet(butt_style)
		button5.clicked.connect(self.close)

		button6 = QPushButton("返回控制中心", self)
		button6.setGeometry(200,450,200,50)
		button6.setFont(font)
		button6.setStyleSheet(butt_style)
		button6.clicked.connect(self.bk2ctrlpage)

	def bk2ctrlpage(slef):
		stack.setCurrentIndex(10)


	def air_livingroom(self):
		self.button = self.button2
		self.msg = "a1"
		start_server(ip,msg=self.msg)


	def air_bdroom0(self):
		self.button = self.button3
		self.msg = "a2"
		start_server(ip,msg=self.msg)


	def air_bdroom1(self):
		self.button = self.button4
		self.msg = "a3"
		start_server(ip,msg=self.msg)


	def air_bkroom(self):
		self.button = self.button2
		self.msg = "a4"
		start_server(ip,msg=self.msg)



		    

class v_ctrl(QWidget):
	"""docstring for v_ctrl"""
	def __init__(self):
		super(v_ctrl, self).__init__()

		self.initUI()


	def initUI(self):
		# 加载背景图片
		img = "icon\\bg0.jpg"
		pixmap = QPixmap(img)

		# 创建标签并设置背景图片
		background = QLabel(self)
		background.setPixmap(pixmap)
		
		# 调整标签大小以适应窗口
		background.setGeometry(0, 0, pixmap.width(), pixmap.height())
		
		# 将标签放置到窗口的底层
		background.lower()

		button1 = QPushButton("音响", self)
		button1.setGeometry(200,100,200,50)
		button1.setFont(font)
		button1.setStyleSheet(butt_style)
		button1.clicked.connect(self.voice_ctrl)

		button2 = QPushButton("投影", self)
		button2.setGeometry(200,180,200,50)
		button2.setFont(font)
		button2.setStyleSheet(butt_style)
		button2.clicked.connect(self.video_ctrl)

		button5 = QPushButton("返回主页", self)
		button5.setGeometry(200,600,200,50)
		button5.setFont(font)
		button5.setStyleSheet(butt_style)
		button5.clicked.connect(self.close)

		button6 = QPushButton("返回控制中心", self)
		button6.setGeometry(200,450,200,50)
		button6.setFont(font)
		button6.setStyleSheet(butt_style)
		button6.clicked.connect(self.bk2ctrlpage)

	def bk2ctrlpage(slef):
		stack.setCurrentIndex(10)


	def voice_ctrl(self):
		self.msg = "v1"
		start_server(ip,msg=self.msg)


	def video_ctrl(self):
		self.msg = "v2"
		start_server(ip,msg=self.msg)


	

class kich_ctrl(QWidget):
	"""docstring for kich_ctrl"""
	def __init__(self):
		super(kich_ctrl, self).__init__()

		self.initUI()


	def initUI(self):
		# 加载背景图片
		img = "icon\\bg0.jpg"
		pixmap = QPixmap(img)

		# 创建标签并设置背景图片
		background = QLabel(self)
		background.setPixmap(pixmap)
		
		# 调整标签大小以适应窗口
		background.setGeometry(0, 0, pixmap.width(), pixmap.height())
		
		# 将标签放置到窗口的底层
		background.lower()

		button1 = QPushButton("电饭锅", self)
		button1.setGeometry(200,100,200,50)
		button1.setFont(font)
		button1.setStyleSheet(butt_style)
		button1.clicked.connect(self.prcker_ctrl)

		button2 = QPushButton("早餐机", self)
		button2.setGeometry(200,180,200,50)
		button2.setFont(font)
		button2.setStyleSheet(butt_style)
		button2.clicked.connect(self.brfst_ctrl)

		button3 = QPushButton("烤箱", self)
		button3.setGeometry(200,260,200,50)
		button3.setFont(font)
		button3.setStyleSheet(butt_style)
		button3.clicked.connect(self.oven_ctrl)

		button4 = QPushButton("蒸箱", self)
		button4.setGeometry(200,340,200,50)
		button4.setFont(font)
		button4.setStyleSheet(butt_style)
		button4.clicked.connect(self.steamer_ctrl)

		button5 = QPushButton("返回主页", self)
		button5.setGeometry(200,600,200,50)
		button5.setFont(font)
		button5.setStyleSheet(butt_style)
		button5.clicked.connect(self.close)

		button6 = QPushButton("返回控制中心", self)
		button6.setGeometry(200,450,200,50)
		button6.setFont(font)
		button6.setStyleSheet(butt_style)
		button6.clicked.connect(self.bk2ctrlpage)

	def bk2ctrlpage(slef):
		stack.setCurrentIndex(10)


	def prcker_ctrl(self):
		self.msg = "k1"
		start_server(ip,msg=self.msg)
		

	def brfst_ctrl(self):
		self.msg = "k2"
		start_server(ip,msg=self.msg)
		

	def oven_ctrl(self):
		self.msg = "k3"
		start_server(ip,msg=self.msg)
		

	def steamer_ctrl(self):
		self.msg = "k4"
		start_server(ip,msg=self.msg)
		


		


class Amu_move(QWidget):
	"""docstring for Amu_move"""
	def __init__(self):
		super(Amu_move, self).__init__()

		self.initUI()


	def initUI(self):
		# 加载背景图片
		img = "icon\\bg0.jpg"
		pixmap = QPixmap(img)

		# 创建标签并设置背景图片
		background = QLabel(self)
		background.setPixmap(pixmap)
		
		# 调整标签大小以适应窗口
		background.setGeometry(0, 0, pixmap.width(), pixmap.height())
		
		# 将标签放置到窗口的底层
		background.lower()

		button1 = QPushButton("前", self)
		button1.setGeometry(200,100,200,50)
		button1.setFont(font)
		button1.setStyleSheet(butt_style)
		button1.clicked.connect(self.fward)

		button2 = QPushButton("后", self)
		button2.setGeometry(200,180,200,50)
		button2.setFont(font)
		button2.setStyleSheet(butt_style)
		button2.clicked.connect(self.bward)

		button3 = QPushButton("停", self)
		button3.setGeometry(200,260,200,50)
		button3.setFont(font)
		button3.setStyleSheet(butt_style)
		button3.clicked.connect(self.stp)

		button4 = QPushButton("左", self)
		button4.setGeometry(200,340,200,50)
		button4.setFont(font)
		button4.setStyleSheet(butt_style)
		button4.clicked.connect(self.tleft)

		button5 = QPushButton("返回主页", self)
		button5.setGeometry(200,600,200,50)
		button5.setFont(font)
		button5.setStyleSheet(butt_style)
		button5.clicked.connect(self.close)

		button6 = QPushButton("返回控制中心", self)
		button6.setGeometry(200,450,200,50)
		button6.setFont(font)
		button6.setStyleSheet(butt_style)
		button6.clicked.connect(self.bk2ctrlpage)

		button7 = QPushButton("右", self)
		button7.setGeometry(200,340,200,50)
		button7.setFont(font)
		button7.setStyleSheet(butt_style)
		button7.clicked.connect(self.tright)

	def bk2ctrlpage(slef):
		stack.setCurrentIndex(10)


	def fward(self):
		self.msg = "f"
		start_server(ip,msg=self.msg)
		

	def bward(self):
		self.msg = "b"
		start_server(ip,msg=self.msg)
		

	def tleft(self):
		self.msg = "l"
		start_server(ip,msg=self.msg)
		

	def tright(self):
		self.msg = "r"
		start_server(ip,msg=self.msg)

	def stp(self):
		self.msg = "s"
		start_server(ip,msg=self.msg)
		

	

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    stack = QStackedWidget()
    mainWindow.setCentralWidget(stack)

    window0 = main_page() 
    window1 = Miss_secretary()
    window2 = home_Assistant()
    window3 = settings()
    window4 = account_info()
    window5 = add_reminder()
    window6 = light_ctrl()
    window7 = air_ctrl()
    window8 = v_ctrl()
    window9 = kich_ctrl()
    window10 = electric_ctrl()
    window11 = Amu_move()



    stack.addWidget(window0)
    stack.addWidget(window1)
    stack.addWidget(window2)
    stack.addWidget(window3)
    stack.addWidget(window4)
    stack.addWidget(window5)
    stack.addWidget(window6)
    stack.addWidget(window7)
    stack.addWidget(window8)
    stack.addWidget(window9)
    stack.addWidget(window10)
    stack.addWidget(window11)
    stack.setCurrentIndex(0)

    mainWindow.show()
    sys.exit(app.exec_())   