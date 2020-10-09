# -*- coding: utf-8 -*-

import subprocess
from source.configurations import *
import os
import shutil

__author__ = 'Michael'

def pack():

    # 新建data目录
    dataPath = os.path.join(rootPath, 'data')
    if not os.path.isdir(dataPath):
        os.makedirs(dataPath)

    # 打包成命令
    iconPath = os.path.join(resourcesPath, 'Taget.ico')         # icon路径
    viewScriptPath = os.path.join(sourcePath, 'record_and_cap_view.py')
    cmd = 'pyinstaller -D -y -i {} {}'.format(iconPath, viewScriptPath).split()
    sub = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, erro = sub.communicate()
    # print out
    print(erro.decode())

    if 'completed successfully' in erro.decode():
        print('y')
        try:
            # 打包产生的文件夹和文件路径
            distPath = os.path.join(sourcePath, 'dist')
            viewPath = os.path.join(distPath, 'record_and_cap_view')
            buildPath = os.path.join(sourcePath, 'build')
            specPath = os.path.join(sourcePath, 'record_and_cap_view.spec')

            # 分系统进行操作
            if 'Darwin' in system:

                # 复制mac的bin文件夹到根目录
                if os.path.isdir(binMacPath):
                    shutil.rmtree(binMacPath)
                shutil.copytree(viewPath, binMacPath, True)

                # 重命名mac可执行的bin文件
                oldScriptNameMac = os.path.join(binMacPath, 'record_and_cap_view')
                newScriptNameMac = os.path.join(binMacPath, 'tool_mac')
                os.rename(oldScriptNameMac, newScriptNameMac)

                # 创建软连接到根文件夹
                softlinkMac = os.path.join(rootPath, 'tool_mac')
                if os.path.isfile(softlinkMac):
                    os.remove(softlinkMac)
                os.symlink(newScriptNameMac, softlinkMac)
                
            elif 'Windows' in system:
                print('b')

                # 复制windows的bin文件夹到根目录
                if os.path.isdir(binWinPath):
                    shutil.rmtree(binWinPath)
                shutil.copytree(viewPath, binWinPath, True)

                print('c')
                # 重命名windows可执行的bin文件
                oldScriptNameWin = os.path.join(binWinPath, 'record_and_cap_view.exe')
                newScriptNameWin = os.path.join(binWinPath, 'tool_win.exe')
                os.rename(oldScriptNameWin, newScriptNameWin)

                print('d')
                # 创建软连接到根文件夹
                # softlinkWin = os.path.join(rootPath, 'tool_win.exe')
                # if os.path.isfile(softlinkWin):
                #     os.remove(softlinkWin)
                # os.symlink(newScriptNameWin, softlinkWin)         # 暂时只能手动创建链接

            

        except:
            print('Package failure')
    else:
        print('Package failure in cmd')

    # 删除打包产生的文件夹和文件路径
    if os.path.isdir(distPath):
        shutil.rmtree(distPath)
    if os.path.isdir(buildPath):
        shutil.rmtree(buildPath)
    if os.path.isfile(specPath):
        os.remove(specPath)




if __name__ == '__main__':

    pack()