#### 工具说明

- 本工具是基于adb使用python语言进行开发，目前只支持android手机的截屏和录制屏幕的功能。工具把adb集成在environment文件夹里，并兼容了windows和mac系统。

#### 使用说明

- mac系统用户

  - 使用前请打开手机的usb调试，并用数据线连接到电脑

  - 直接点击文件里的tool_mac软链接即可运行，或点击bin_mac文件夹里的tool_mac二进制文件也可运行
  - 本工具支持自主打包，需要安装pyinstaller，运行source文件夹里的pack.py脚本即可
    - 安装pyinstaller
      - 需要有python 2.7环境
      - 在命令行输入pip install pyinstaller，等待安装完成即可
  - 文件夹切忌不要随意移动，特别是bin_mac文件夹，脚本会依赖与这些文件夹的相对路径，避免产生错误
  - 截图和录制的视频保存在data文件夹里

- windows系统用户

  - 使用前请打开手机的usb调试，并用数据线连接到电脑
  - 直接点击文件里的tool_win.exe链接即可运行，或点击bin_win文件夹里的tool_win.exe文件也可运行
  - 本工具支持自主打包，需要安装pyinstaller，运行source文件夹里的pack.py脚本即可。完成后，在bin_win文件夹里可以看到tool_win.exe文件，点击运行即可。也可以自己创建软链接到其他地方，更方便运行
    - 安装pyinstaller
      - 需要有python 2.7环境
      - 在命令行输入pip install pyinstaller，等待安装完成即可
  - 文件夹切忌不要随意移动，特别是bin_win文件夹，脚本会依赖与这些文件夹的相对路径，避免产生错误
  - 截图和录制的视频保存在data文件夹里