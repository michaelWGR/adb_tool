# -*- coding: utf-8 -*-
import subprocess
import time
from source.configurations import *
import os
import platform

__author__ = 'Michael'

PLATFORM = platform.system()

dataPath = os.path.join(rootPath, 'data')  # data文件夹的路径
if not os.path.isdir(dataPath):
    if os.path.isfile(dataPath):
        os.remove(dataPath)
    os.makedirs(dataPath)


def getAdbPath():
    androidPath = os.path.join(environmentPath, 'android')
    result = os.system('adb devices')
    if 0 == result:
        return 'adb'
    elif platform.system() == 'Darwin':
        ptMacPath = os.path.join(androidPath, 'platform-tools-mac')
        adbMacPath = os.path.join(ptMacPath, 'adb')
        return adbMacPath
    elif platform.system() == 'Windows':
        ptWinPath = os.path.join(androidPath, 'platform-tools-windows')
        adbWinPath = os.path.join(ptWinPath, 'adb')
        return adbWinPath
    else:
        return ''


# 定义adb路径
ADBPATH = getAdbPath()


def connectDevice():  # 判断是否可连接上设备
    cmd_device = '{} devices'.format(ADBPATH).split()
    p_device = subprocess.Popen(cmd_device, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p_device.wait()
    deviceInfo = p_device.stdout.readlines()
    if deviceInfo[1].decode() == '\n':
        print('设备未连接，请重新连接android设备')
        sys.exit()
    else:
        return True


def pull_rm(phone_id, save_phone_path):  # 把文件从手机拉出来，然后删除手机的文件
    try:
        if not os.path.isdir(dataPath):
            if os.path.isfile(dataPath):
                os.remove(dataPath)
            os.makedirs(dataPath)
        print('Pulling and removing...')
        # cmd_pull = '{} -s {} pull {} "{}"'.format(ADBPATH, phone_id, save_phone_path, dataPath).split()
        cmd_pull = [ADBPATH, '-s', phone_id, 'pull', save_phone_path, dataPath]  # 预防windows有空格的文件名
        print(cmd_pull)
        res_pull = subprocess.Popen(cmd_pull, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        print(res_pull[0].decode())
        print(res_pull[1].decode())
        if res_pull[1].decode() != '':
            return
        time.sleep(1)

        cmd_rm = '{} -s {} shell rm {}'.format(ADBPATH, phone_id, save_phone_path).split()
        print(cmd_rm)
        res_rm = subprocess.Popen(cmd_rm, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        print(res_rm[0].decode())
        print(res_rm[1].decode())
        if res_rm[1].decode() != '':
            return

    except:
        print('Please try again')


# 打开data文件夹
def openDir():
    if not os.path.isdir(dataPath):
        os.makedirs(dataPath)
    print(dataPath)
    pf = platform.system()
    if pf == 'Darwin':
        cmd = 'open {}'.format(dataPath).split()
        subprocess.Popen(cmd).communicate()
    elif pf == 'Windows':
        os.startfile(dataPath)


# 获取当前时间
def get_current_time():
    localtime = time.localtime(time.time())
    format_time = time.strftime('%Y%m%d%H%M%S', localtime)
    return format_time


def screencap(phone_id, filename):  # 截取图片
    if phone_id == '':
        return cap_status_map[4]

    if filename in photo_type:
        # 判断是否使用默认命名方式,photo_type配置文件的图片后缀
        current_time = get_current_time()
        filename = current_time + filename

    if os.path.splitext(filename)[1] not in photo_type:  # 判断图片类型
        return cap_status_map[2]

    try:
        print(filename)
        save_phone_path = '/sdcard/' + filename  # 为了适配windos和macos系统
        cmd_cap = '{} -s {} shell screencap -p {}'.format(ADBPATH, phone_id, save_phone_path).split()
        res_cap = subprocess.Popen(cmd_cap, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        print(res_cap[0].decode())
        print(res_cap[1].decode())

        if res_cap[1].decode() != '':
            return cap_status_map[3]

        pull_rm(phone_id, save_phone_path)

        return ''
    except Exception as e:
        return cap_status_map[3]


class PhoneType(object):
    phone_dict = {'': ''}

    @classmethod
    def get_phone_id_list(cls):
        """获取设备id"""
        phone_id_list = []
        cmd = '{} devices'.format(ADBPATH).split()
        sub_id = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out = sub_id.communicate()
        # byte需要转为string
        if out[1].decode() == '':
            id_list = out[0].decode().split('\n')
            for i in range(1, len(id_list)):
                if id_list[i] not in ['', '\r']:
                    phone_id = id_list[i].split('\t')[0]
                    phone_id_list.append(phone_id)
        return phone_id_list

    @classmethod
    def get_phone_dict(cls):
        """集成手机名和设备id的字典"""
        phone_id_list = cls.get_phone_id_list()
        cls.phone_dict = {'': ''}
        if phone_id_list != []:
            cls.phone_dict.clear()
            for id in phone_id_list:
                cmd = '{} -s {} shell getprop | grep ro.product.model]'.format(ADBPATH, id).split()
                sub = subprocess.Popen(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
                out = sub.communicate()
                # byte需要转为string
                if out[1].decode() == '':
                    phone_name = out[0].decode().split(':')[1].strip()
                    phone_name = phone_name[1:len(phone_name) - 1]
                    cls.phone_dict[phone_name] = id
        return cls.phone_dict

    @classmethod
    def get_phone_name_list(cls):
        """获取手机名称，用于显示"""
        phone_name_list = []
        if cls.get_phone_dict():
            phone_name_list = list(cls.get_phone_dict().keys())
        print(phone_name_list)
        return phone_name_list

    @classmethod
    def get_phone_id(cls, phone_name):
        """获取设备id用户操作请求"""
        phone_id = cls.phone_dict.get(phone_name, '')
        print(phone_id)
        return phone_id


class Record(object):
    ''' 录制展示状态
    record_status_map = {
        0: '未开始录制',
        1: '正在录制',
        2: '录制失败',
        3: '命名错误'
    }
    '''

    record_status = 0
    sub_process = None
    save_phone_path = ''
    do_quit = True
    return_text = ''
    phone_id = ''

    @classmethod
    def begin_record(cls, phone_id, videoname, RATE='16000000', TIME='180'):  # 视频录制
        # print videoname
        cls.phone_id = phone_id
        if phone_id == '':
            cls.record_status = 5
            cls.return_text = record_status_map[cls.record_status]
            return

        if videoname in video_type:  # 判断是否使用默认命名方式,video_type配置文件的视频后缀
            current_time = get_current_time()
            videoname = current_time + videoname

        if os.path.splitext(videoname)[1] not in video_type:  # 判断视频文件名的格式
            cls.record_status = 4
            cls.return_text = record_status_map[cls.record_status]
            return

        try:
            print(videoname)
            if cls.record_status == 0:
                cls.save_phone_path = '/sdcard/' + videoname  # 为了适配windos和macos系统

                cmd_record = '{} -s {} shell screenrecord --bit-rate {} --time-limit {} {}'.format(ADBPATH,
                                                                                                   cls.phone_id, RATE,
                                                                                                   TIME,
                                                                                                   cls.save_phone_path).split()
                cls.sub_process = subprocess.Popen(cmd_record, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

                cls.record_status = 1
                print('Recording...')

                cls.time_to_quit()
                cls.return_text = ''

                erro = cls.sub_process.stderr.read().decode()
                if erro != '':
                    print(erro.strip())
                    cls.record_status = 2
                    cls.return_text = record_status_map[cls.record_status]

        except Exception as e:
            cls.record_status = 2
            cls.return_text = record_status_map[cls.record_status]

    @classmethod
    def time_to_quit(cls):  # 时间到后自动结束录制
        while cls.do_quit:
            if cls.sub_process.poll() != None:
                time.sleep(1)  # 为了完全关闭进程
                pull_rm(cls.phone_id, cls.save_phone_path)
                cls.record_status = 0
                break

    @classmethod
    def quit_record(cls):  # 手动结束录制
        try:

            if cls.record_status == 1 and cls.sub_process.poll() == None:
                cls.do_quit = False  # 为了结束time_to_quit里的循环
                cls.sub_process.terminate()

                time.sleep(1)  # 为了完全关闭进程
                pull_rm(cls.phone_id, cls.save_phone_path)
                cls.record_status = 0

                cls.return_text = ''
        except:
            cls.record_status = 3
            cls.return_text = record_status_map[cls.record_status]

    @classmethod
    def set_status(cls, status):
        if status in record_status_map.keys():
            cls.record_status = status


# class quit_record():  # 使用线程结束视频录制的进程
#
#     def __init__(self, process):
#         self.process = process
#
#     def input_to_quit(self):
#         while True and self.process.poll() == None:
#             quit_signal = raw_input("Enter 'q' to quit recording:")
#             if quit_signal == 'q':
#                 self.process.terminate()
#                 break
#
#     def time_to_quit(self):
#         while True:
#             if self.process.poll() != None:
#                 break
#
#     def run(self):
#         threads = []
#         threads.append(threading.Thread(target=self.input_to_quit))
#         threads.append(threading.Thread(target=self.time_to_quit))
#         for t in threads:
#             t.setDaemon(True)
#             t.start()
#
#         while True:
#             if not (threads[0].isAlive() and threads[1].isAlive()):
#                 break
#
# def screenrecord(videoname, RATE='16000000', TIME='180'):       #视频录制
#     if os.path.splitext(videoname)[1] not in ['.mp4']:      #判断视频文件名的格式
#         return 'Please input correct videoname.'
#
#     try:
#         save_phone_path = '/sdcard/'+videoname      #为了适配windos和macos系统
#
#         cmd_record = 'adb shell screenrecord --bit-rate {} --time-limit {} {}'.format(RATE, TIME, save_phone_path).split()
#         sub_process = subprocess.Popen(cmd_record)
#         print 'Recording...'
#
#         q = quit_record(sub_process)
#         q.run()
#         time.sleep(1)       #为了完全关闭进程
#
#         pull_rm(save_phone_path)
#     except:
#         return 'Please try again.'

# def main():
#     parser = argparse.ArgumentParser(description='record video and cap photo for android phone')
#     parser.add_argument('-p', '--photo', dest='photo', type=str, help='the name of printscreen')
#     parser.add_argument('-v', '--video', dest='video', type=str, help='the name of recording video')
#     parser.add_argument('--rate', dest='rate', type=str, default='16000000', help='the bit rate of video')
#     parser.add_argument('--time', dest='time', type=str, default='180', help='the time of recording')
#     args = parser.parse_args()
#     param_photo = args.photo
#     param_video = args.video
#     param_rate = args.rate
#     param_time = args.time
#
#     if connectDevice():
#         if param_photo is not None:
#             print screencap(param_photo)
#         elif param_video is not None:
#             print screenrecord(param_video, param_rate, param_time)

if __name__ == '__main__':
    # main()
    # Record.begin_record('RTJ0217727000288', 'test.mp4')
    # get_current_time()
    # print getAdbPath()
    # screencap('a3c2ca1d', '12.jpg')
    PhoneType().get_phone_name_list()
    PhoneType().get_phone_id('Redmi Note 5')

