from conf import Conf
from util import Util
import sys
import os
from PyQt5.QtWidgets import (QPushButton, QGridLayout, QLabel, QLineEdit, QApplication,
                             QMessageBox, QGroupBox, QFormLayout, QCheckBox, QDialog)
from PyQt5.QtGui import QIcon


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
        self.cb_ssl = QCheckBox('SSL加密')
        self.cb_log = QCheckBox('记录日志')
        self.cb_autorun = QCheckBox('开机启动')
        self.cb_proxy = QCheckBox('系统代理')
        self.cb_autorun.stateChanged.connect(self.autorun)
        self.cb_proxy.stateChanged.connect(self.sys_proxy)

        # 创建按钮
        self.btn_action = QPushButton("启动代理")
        btn_help = QPushButton("使用说明")

        # 按钮点击事件
        self.btn_action.clicked.connect(self.start_proxy)
        btn_help.clicked.connect(self.show_help)

        # 添加到容器
        layout.addRow(QLabel("服务器IP:"), self.edit_server_ip)
        layout.addRow(QLabel("服务器端口:"), self.edit_server_port)
        layout.addRow(QLabel("本地代理端口:"), self.edit_local_port)
        layout.addRow(self.cb_ssl, self.cb_log)
        layout.addRow(self.cb_autorun, self.cb_proxy)
        layout.addRow(btn_help, self.btn_action)

        # 获取配置信息
        conf = Conf().conf

        # 如果有配置文件则赋值
        if conf != {}:
            self.edit_server_ip.setText(str(conf['server_ip']))
            self.edit_server_port.setText(str(conf['server_port']))
            self.edit_local_port.setText(str(conf['local_port']))
            if conf['ssl'] == 'True':
                self.cb_ssl.setChecked(True)
            if conf['log'] == 'True':
                self.cb_log.setChecked(True)
            if conf['autorun'] == 'True':
                self.cb_autorun.setChecked(True)
            if conf['proxy'] == 'True':
                self.cb_proxy.setChecked(True)

        # 显示UI
        self.formGroupBox.setLayout(layout)
        mainLayout = QGridLayout()
        mainLayout.addWidget(self.formGroupBox)
        self.setLayout(mainLayout)

        # 判断状态
        self.is_run()

        # 设置窗口标题
        self.setWindowTitle('GoProxy')
        # 设置窗口图标
        self.setWindowIcon(QIcon('icon.png'))
        # 显示窗口
        self.show()

    # 启动代理
    def start_proxy(self):
        status = Util().check_exsit('proxy-wingui.exe')
        if status:
            os.system('taskkill /F /IM proxy-wingui.exe')
            status = Util().check_exsit('proxy-wingui.exe')
            if status:
                QMessageBox.information(self, "提示", self.tr("关闭代理失败"))
            else:
                self.btn_action.setText('启动代理')
                QMessageBox.information(self, "提示", self.tr("关闭代理成功"))
        else:
            shell = 'start proxy-wingui.exe http -t tcp -p ":' + self.edit_local_port.text() + '" -T tls -P'
            shell = shell + ' "' + self.edit_server_ip.text() + ':' + self.edit_server_port.text() + '"'
            if self.cb_ssl.isChecked():
                shell = shell + ' -C .cert/proxy.crt -K .cert/proxy.key'
            if self.cb_log.isChecked():
                shell = shell + ' --log proxy.log'
            os.system(shell)
            status = Util().check_exsit(process_name='proxy-wingui.exe')
            if status:
                self.btn_action.setText('关闭代理')
                QMessageBox.information(self, "报告老大", self.tr("代理已开启"))
            else:
                QMessageBox.information(self, "提示", self.tr("启动代理失败"))

    # 使用说明
    def show_help(self):
        Util.show_help()

    # 保存配置
    def save_config(self):
        config = {
            "server_ip": self.edit_server_ip.text(),
            "server_port": self.edit_server_port.text(),
            "local_port": self.edit_local_port.text(),
            "ssl": str(self.cb_ssl.isChecked()),
            "log": str(self.cb_log.isChecked()),
            "autorun": str(self.cb_autorun.isChecked()),
            "proxy": str(self.cb_proxy.isChecked())
        }
        Conf().save_config(config)

    # 开机启动
    def autorun(self):
        if self.cb_autorun.isChecked():
            path = os.getcwd() + '\goproxy.exe Silent'
            result = Util.set_autorun(path)
            if result == True:
                QMessageBox.information(self, "提示", self.tr("添加到开机启动成功"))
            else:
                QMessageBox.information(self, "提示", self.tr("添加到开机启动失败"))
        else:
            Util.del_autorun()

    # 判断goproxy是否已经后台运行
    def is_run(self):
        status = Util().check_exsit('proxy-wingui.exe')
        if status:
            self.btn_action.setText('关闭代理')
        else:
            self.btn_action.setText('启动代理')
        self.save_config()

    # 设置系统代理
    def sys_proxy(self):
        if self.cb_proxy.isChecked():
            port = self.edit_local_port.text()
            os.system(
                'reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyEnable /t REG_DWORD /d 1 /f')
            os.system(
                'reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyServer /d "http=127.0.0.1:' + port + ';https=127.0.0.1:' + port + '" /f')
            os.system(
                'reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyOverride /t REG_SZ /d "<-loopback>" /f')
            QMessageBox.information(self, "提示", self.tr("已启用系统代理"))
        else:
            os.system(
                'reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyEnable /t REG_DWORD /d 0 /f')
            os.system(
                'reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyServer /d "" /f')
            os.system(
                'reg delete "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyOverride /f')
            QMessageBox.information(self, "提示", self.tr("已关闭系统代理"))
        self.save_config()


# 程序运行入口
if __name__ == '__main__':
    app = QApplication(sys.argv)
    if len(sys.argv) >= 2:
        Util().silent_run(Conf().conf)
    else:
        ex = Window()
        sys.exit(app.exec_())
