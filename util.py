import os
import webbrowser


class Util():

    # 初始化方法
    def __init__(self):
        super().__init__()

    # 检查某程序是否运行
    @staticmethod
    def check_exsit(process_name):
        run = os.popen('tasklist|find /i "'+process_name+'"')
        if run.read() == '':
            return False
        else:
            return True

    # 干掉某程序
    @staticmethod
    def kill_process(name):
        run = os.popen('taskkill /F /IM "'+name+'"')
        if '成功' in run.read():
            return True
        else:
            return False

    # 设置开机启动
    @staticmethod
    def set_autorun(path):
        run = os.popen(
            'reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v GoProxy /t REG_SZ /d "'+path+'" /f')
        if '成功' in run.read():
            return True
        else:
            return False

    # 删除开机启动项
    @staticmethod
    def del_autorun():
        run = os.popen('reg delete "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v GoProxy /f')
        if '成功' in run.read():
            return True
        else:
            return False

    # 设置系统代理
    @staticmethod
    def set_proxy(port):
        run1 = os.popen(
            'reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyEnable /t REG_DWORD /d 1 /f')
        run2 = os.popen(
            'reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyServer /d "http=127.0.0.1:' + port + ';https=127.0.0.1:' + port + '" /f')
        run3 = os.popen(
            'reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyOverride /t REG_SZ /d "<-loopback>" /f')
        if '成功' in run1.read() and '成功' in run2.read() and '成功' in run3.read():
            return True
        else:
            return False

    # 取消设置系统代理
    @staticmethod
    def del_proxy():
        run1 = os.popen(
            'reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyEnable /t REG_DWORD /d 0 /f')
        run2 = os.popen(
            'reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyServer /d "" /f')
        run3 = os.popen(
            'reg delete "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyOverride /f')
        if '成功' in run1.read() and '成功' in run2.read() and '成功' in run3.read():
            return True
        else:
            return False

    # 开机静默启动
    @staticmethod
    def silent_run(conf):
        if Util().check_exsit('proxy-wingui.exe'):
            os.popen('taskkill /F /IM proxy-wingui.exe')
        shell = 'start proxy-wingui.exe http -t tcp -p ":' + conf['local_port']+ '" -T tls -P'
        shell = shell + ' "' + conf['server_ip'] + ':' + conf['server_port'] + '"'
        if conf['ssl'] == 'True':
            shell = shell + ' -C .cert/proxy.crt -K .cert/proxy.key'
        if conf['log'] == 'True':
            shell = shell + ' --log proxy.log'
        os.popen(shell)
        status = Util().check_exsit('proxy-wingui.exe')
        if status:
            print('静默开机启动代理成功')
        else:
            print('静默开机启动代理失败')

    # 打开github页面
    @staticmethod
    def show_help():
        webbrowser.open_new('https://github.com/CorePlusPlus/goproxy-pyui')