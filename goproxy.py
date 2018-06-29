import sys
import os
import json
import win32com.client
from PyQt5.QtWidgets import (QPushButton, QGridLayout, QLabel, QLineEdit, QApplication,
                             QMessageBox, QGroupBox, QFormLayout, QCheckBox, QDialog)
from PyQt5.QtGui import QIcon


class Util():
    # 初始化方法
    def __init__(self):
        super().__init__()
        self.config = self.getConfig()

    # 获取配置文件
    def getConfig(self):
        if self.hasConfig():
            return self.readConfig()
        else:
            return {}

    # 判断配置文件是否存在
    @staticmethod
    def hasConfig():
        return os.path.exists('config.json')

    # 读取配置文件
    @staticmethod
    def readConfig():
        with open('config.json', 'r') as f:
            return json.load(f)

    # 写配置文件
    @staticmethod
    def saveConfig(data):
        with open('config.json', 'w') as f:
            json.dump(data, f)

    # 检查某程序是否运行
    def check_exsit(process_name):
        WMI = win32com.client.GetObject('winmgmts:')
        processCodeCov = WMI.ExecQuery('select * from Win32_Process where Name="%s"' % process_name)
        if len(processCodeCov) > 0:
            return 1
        else:
            return 0


class Window(QDialog):

    def __init__(self):
        super(QDialog, self).__init__()
        self.init_ui()

    # 窗口初始化
    def init_ui(self):
        # 创建布局
        self.formGroupBox = QGroupBox("参数配置")
        layout = QFormLayout()

        # 创建文本框
        self.edit_server_ip = QLineEdit()
        self.edit_server_port = QLineEdit()
        self.edit_local_port = QLineEdit()

        # 创建复选框
        self.cb_ssl = QCheckBox('SSL通信')
        self.cb_log = QCheckBox('记录日志')

        # 创建按钮
        btn_stop = QPushButton("关闭代理")
        btn_start = QPushButton("启动代理")
        btn_save = QPushButton("保存配置")
        btn_autorun = QPushButton("开机启动")

        # 按钮点击事件
        btn_start.clicked.connect(self.start_proxy)
        btn_stop.clicked.connect(self.stop_proxy)
        btn_save.clicked.connect(self.save_config)
        btn_autorun.clicked.connect(self.autorun)

        # 添加到容器
        layout.addRow(QLabel("服务器IP:"), self.edit_server_ip)
        layout.addRow(QLabel("服务器端口:"), self.edit_server_port)
        layout.addRow(QLabel("本地代理端口:"), self.edit_local_port)
        layout.addRow(self.cb_ssl, self.cb_log)
        layout.addRow(btn_save, btn_autorun)
        layout.addRow(btn_stop, btn_start)

        # 获取配置信息
        conf = Util().config

        # 如果有配置文件则赋值
        if conf != {}:
            self.edit_server_ip.setText(str(conf['server_ip']))
            self.edit_server_port.setText(str(conf['server_port']))
            self.edit_local_port.setText(str(conf['local_port']))
            if conf['ssl'] == 'True':
                self.cb_ssl.setChecked(True)
            if conf['log'] == 'True':
                self.cb_log.setChecked(True)

        # 显示UI
        self.formGroupBox.setLayout(layout)
        mainLayout = QGridLayout()
        mainLayout.addWidget(self.formGroupBox)
        self.setLayout(mainLayout)

        # 设置窗口标题
        self.setWindowTitle('GoProxy')
        # 设置窗口图标
        self.setWindowIcon(QIcon('icon.png'))
        # 显示窗口
        self.show()

    # 启动代理
    def start_proxy(self):
        shell = 'start proxy-wingui.exe http -t tcp -p ":' + self.edit_local_port.text() + '" -T tls -P'
        shell = shell + ' "' + self.edit_server_ip.text() + ':' + self.edit_server_port.text() + '"'
        if self.cb_ssl.isChecked():
            shell = shell + ' -C .cert/proxy.crt -K .cert/proxy.key'
        if self.cb_log.isChecked():
            shell = shell + ' --log proxy.log'
        print(shell)
        os.system(shell)
        QMessageBox.information(self, "报告老大", self.tr("代理已开启"))

    # 停止代理
    def stop_proxy(self):
        os.system('taskkill /F /IM proxy-wingui.exe')
        QMessageBox.information(self, "报告老大", self.tr("我已经把它干掉了..."))

    # 保存配置
    def save_config(self):
        config = {
            "server_ip": self.edit_server_ip.text(),
            "server_port": self.edit_server_port.text(),
            "local_port": self.edit_local_port.text(),
            "ssl": str(self.cb_ssl.isChecked()),
            "log": str(self.cb_log.isChecked())
        }
        conf = Util()
        conf.saveConfig(config)
        QMessageBox.information(self, "提示", self.tr("保存成功"))

    # 开机启动
    def autorun(self):
        QMessageBox.information(self, "提示", self.tr("暂不支持"))


# 程序运行入口
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Window()
    sys.exit(app.exec_())
