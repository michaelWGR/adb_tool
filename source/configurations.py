# -*- coding: utf-8 -*-
import os
import sys
import platform

__author__ = 'Michael'

# 录制展示状态
record_status_map = {
    0: '未开始录制',
    1: '正在录制',
    2: '录制失败',
    3: '停止录制失败',
    4: '命名错误',
    5: '未选择手机'
}

# 截图的状态
cap_status_map = {
    0: '未开始截图',
    1: '正在截图',
    2: '命名错误',
    3: '截图失败',
    4: '未选择手机'
}

# 截图的图片类型
photo_type = ['.png', '.jpg']

# 录制的视频类型
video_type = ['.mp4']

# 系统类型
system = platform.system()

# 当前脚本的路径
def app_path():
    if hasattr(sys, 'frozen'):
        return os.path.realpath(sys.executable)
    else:
        return os.path.realpath(__file__)
scriptPath = app_path()

# 根目录的路径
rootPath = os.path.dirname(os.path.dirname(scriptPath))

# data路径
dataPath = os.path.join(rootPath, 'data')

# resources路径
resourcesPath = os.path.join(rootPath, 'resources')

# source路径
sourcePath = os.path.join(rootPath, 'source')

# environment路径
environmentPath = os.path.join(rootPath, 'environment')

# mac的bin路径
binMacPath = os.path.join(rootPath, 'bin_mac')

# window的bin路径
binWinPath = os.path.join(rootPath, 'bin_win')

if __name__ == '__main__':
    print scriptPath
    print rootPath
    print dataPath
    print resourcesPath
    print sourcePath
    print environmentPath
    print binMacPath
    print binWinPath
    print system