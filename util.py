import os
import win32com.client
import win32api
import win32con
import webbrowser


class Util():

    # 初始化方法
    def __init__(self):
        super().__init__()

    # 检查某程序是否运行
    @staticmethod
    def check_exsit(process_name):
        WMI = win32com.client.GetObject('winmgmts:')
        processCodeCov = WMI.ExecQuery('select * from Win32_Process where Name="%s"' % process_name)
        if len(processCodeCov) > 0:
            return True
        else:
            return False

    # 设置开机启动
    @staticmethod
    def set_autorun(path):
        name = 'GoProxy'  # 要添加的项值名称
        KeyName = 'Software\\Microsoft\\Windows\\CurrentVersion\\Run'
        try:
            key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER, KeyName, 0, win32con.KEY_ALL_ACCESS)
            win32api.RegSetValueEx(key, name, 0, win32con.REG_SZ, path)
            win32api.RegCloseKey(key)
        except:
            return False
        else:
            return True

    # 删除开机启动项
    @staticmethod
    def del_autorun():
        os.system('reg delete "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v GoProxy /f')
        return True

    # 开机静默启动
    @staticmethod
    def silent_run(conf):
        if Util().check_exsit('proxy-wingui.exe'):
            os.system('taskkill /F /IM proxy-wingui.exe')
        shell = 'start proxy-wingui.exe http -t tcp -p ":' + conf['local_port']+ '" -T tls -P'
        shell = shell + ' "' + conf['server_ip'] + ':' + conf['server_port'] + '"'
        if conf['ssl'] == 'True':
            shell = shell + ' -C .cert/proxy.crt -K .cert/proxy.key'
        if conf['log'] == 'True':
            shell = shell + ' --log proxy.log'
        os.system(shell)
        status = Util().check_exsit('proxy-wingui.exe')
        if status:
            print('静默开机启动代理成功')
        else:
            print('静默开机启动代理失败')

    # 打开github页面
    @staticmethod
    def show_help():
        webbrowser.open_new('https://github.com/CorePlusPlus/goproxy-pyui')