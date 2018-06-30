# goproxy-pyui 科学上网利器
这是基于Python Pyqt5开发[goproxy](https://github.com/snail007/goproxy)的GUI版本
# 预览图
![Preview.png](https://raw.githubusercontent.com/CorePlusPlus/goproxy-pyui/master/Preview.png)
# 使用方法
### 服务端
* 安装goproxy
* `curl -L https://raw.githubusercontent.com/snail007/goproxy/master/install_auto.sh | bash `
* 生成证书(执行后会在当前目录生成proxy.crt和proxy.key下载这两个文件到本地)
* `proxy keygen -C proxy`
* 启动科学上网服务(38080为服务器端口可自定义需要开放此端口防火墙)
* `proxy http -t tls -p ":38080" -C proxy.crt -K proxy.key --daemon --forever`
### 客户端
* 下载[客户端](https://github.com/CorePlusPlus/goproxy-pyui/releases)
* 填写配置信息(参考预览图)
* 将上面下载好的proxy.crt和proxy.key放到.cert文件夹里面(替换掉原来的文件)
* 点启动代理
* 浏览器需要将代理改为127.0.0.1:1080(和SS/SSR类似)
* 然后可以愉快的搞py交易了

# 其他说明
* 后期会把开机启动和设置系统代理给加上，先凑合用着吧
* 有问题请提issues
