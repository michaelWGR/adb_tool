# -*- coding: utf-8 -*-
from tkinter import *
from source.record_and_cap_for_android import *
from source.configurations import *
from tkinter import ttk
import threading
import time

__author__ = 'Michael'


def mainWindow():
    root = Tk()
    root.title('截屏录制工具')
    # root.geometry('400x600')
    root.resizable(width=True, height=True)
    iconPath = os.path.join(resourcesPath, 'Taget.ico')
    root.iconbitmap(iconPath)
    frame = Frame(root)
    frame.grid()

    # 顶部框架
    topFrame = Frame(frame)
    topFrame.grid(row=0, column=0, sticky='W')

    TopView.topArea(topFrame)

    # 设置切换tab
    tabControl = ttk.Notebook(frame)
    tab1 = ttk.Frame(tabControl)
    tabControl.add(tab1, text='截屏')
    tab2 = ttk.Frame(tabControl)
    tabControl.add(tab2, text='录屏')
    tabControl.grid(row=1, column=0, padx=5)

    capframe = LabelFrame(tab1, text='截屏', fg='blue')
    capframe.grid(row=0, column=0, padx=5, pady=5)

    recordframe = LabelFrame(tab2, text='录屏', fg='blue')
    recordframe.grid(row=0, column=0, padx=5, pady=5)

    CapView(capframe).capArea()
    RecordView(recordframe).recordArea()

    root.mainloop()


class TopView(Frame):
    # phone_name = ''

    @classmethod
    def topArea(cls, frame):
        # 手机选项文本
        phone_text = Label(frame, text='请选择手机类型: ')
        phone_text.grid(row=0, column=0, sticky='W', padx=5)

        # 手机类型的下拉选项
        cls.phonelist = ttk.Combobox(frame, width=10, state='readonly')
        phone_name_list = PhoneType.get_phone_name_list()         # 执行获取手机类型
        cls.phonelist['values'] = phone_name_list
        cls.phonelist.current(0)
        cls.phonelist.bind('<Button-1>', cls.set_combox_value)
        cls.phonelist.grid(row=0, column=1)

        # 打开文件夹按钮
        boldStyle = ttk.Style()
        boldStyle.configure('Bold.TButton', font=('微软雅黑', 10, 'bold'))
        openDirButton = ttk.Button(frame, text='打开存储文件夹', style='Bold.TButton',
                                   command=openDir)
        openDirButton.grid(row=0, column=2, sticky='W', padx=40)

    @classmethod
    def set_combox_value(cls, event):
        phone_name_list = PhoneType.get_phone_name_list()
        cls.phonelist['values'] = phone_name_list
        cls.phonelist.current(0)

    @classmethod
    def get_current_id(cls):
        current_phone_name = cls.phonelist.get()
        phone_id = PhoneType.get_phone_id(current_phone_name)
        return phone_id


class CapView(Frame):
    def __init__(self,frame):
        Frame.__init__(self, frame)
        self.frame = frame
        self.var_text = StringVar()

    def capArea(self):
        # 截图名称文本
        p_name_text = Label(self.frame, text='输入截图名称(.png/.jpg):  ')
        p_name_text.grid(row=0, column=0, sticky='W')

        # 截图名称输入框
        name_frame = Frame(self.frame)          # 创建一个框架，容纳名称输入框和名称后缀选择框
        name_frame.grid(row=1, column=0, sticky='W')

        self.p_name = StringVar()
        self.p_name.set('默认以时间命名')
        self.p_name_enter = Entry(name_frame, width=12, textvariable=self.p_name)       # 图片名称输入框

        self.p_name_enter.configure(fg='#A9A9A9', font=('微软雅黑', 10, 'bold'))
        self.p_name_enter.bind('<Button-1>', self.__click_entry)
        self.p_name_enter.grid(row=0, column=0, sticky='W')
        self.p_name_enter.focus()

        self.suffix_box = ttk.Combobox(name_frame, values=photo_type, width=4, state='readonly')      # 图片后缀选择框
        self.suffix_box.current(0)
        self.suffix_box.grid(row=0, column=1, sticky='W')

        # 运行截图操作
        boldStyle = ttk.Style()
        boldStyle.configure('Bold.TButton', font=('微软雅黑', 10, 'bold'))
        self.begin = ttk.Button(self.frame, text='开始截屏', style='Bold.TButton',
                                command=lambda : self.__btFun(name=self.p_name_enter.get()))
        self.begin.grid(row=1, column=1, padx=10)

        # 返回函数发生错误的文本信息
        error_text = Label(self.frame, textvariable=self.var_text, fg='red', font = 'Helvetica -9 bold')
        error_text.grid(row=2, column=0, sticky='W')

    def __btFun(self, name):
        if str(self.begin['state']) == 'normal':            # 判断是否可执行
            self.begin.configure(state='disable')           # 设置按钮不可用

            # 格式化截图名称
            if name == '':
                full_name = ''+self.suffix_box.get()
                self.p_name.set('默认以时间命名')
                self.p_name_enter.configure(fg='#A9A9A9')
            elif name == '默认以时间命名':
                full_name = ''+self.suffix_box.get()
            else:
                full_name = name+self.suffix_box.get()      # 完整的截图名称

            phone_id = TopView.get_current_id()             # 获取选择手机的id
            errorText = screencap(phone_id, full_name)
            self.var_text.set(errorText)
            self.begin.configure(state='normal')
        
    def __click_entry(self,event):
        if self.p_name.get() == u'默认以时间命名':
            self.p_name.set('')
            self.p_name_enter.configure(fg='#000000')
        elif self.p_name.get() == '':
            self.p_name_enter.configure(fg='#000000')


class RecordView(object):
    def __init__(self, frame):
        self.frame = frame
        self.error_text = StringVar()

    def recordArea(self):
        # 视频名称文本
        v_name_text = Label(self.frame, text='输入视频名称(.mp4):  ')
        v_name_text.grid(row=0, column=0, sticky='W')

        # 视频录制时间文本
        v_time_text = Label(self.frame, text='输入录制时间(s):')
        v_time_text.grid(row=0, column=1, sticky='W', padx=5)

        # 视频名称输入框
        v_name_frame = Frame(self.frame)          # 创建一个框架，容纳名称输入框和名称后缀选择框
        v_name_frame.grid(row=1, column=0, sticky='W')

        self.v_name = StringVar()
        self.v_name.set(u'默认以时间命名')
        self.v_name_enter = Entry(v_name_frame, width=12, textvariable=self.v_name)     # 视频名称输入框

        self.v_name_enter.configure(fg='#A9A9A9', font=('微软雅黑', 10, 'bold'))
        self.v_name_enter.bind('<Button-1>', self.__click_entry)
        self.v_name_enter.grid(row=0, column=0, sticky='W')
        self.v_name_enter.focus()

        self.v_suffix_box = ttk.Combobox(v_name_frame, values=video_type, width=4, state='readonly')      # 视频后缀选择框
        self.v_suffix_box.current(0)
        self.v_suffix_box.grid(row=0, column=1, sticky='W')

        # 视频录制时间
        v_time = StringVar()
        v_time_enter = Entry(self.frame, width=4, textvariable=v_time, state='readonly')    # 先设置不可修改
        v_time_enter.grid(row=1, column=1, sticky='W', padx=5)
        v_time.set('180')

        # 运行录屏操作
        boldStyle = ttk.Style()
        boldStyle.configure('Bold.TButton', font=('微软雅黑', 10, 'bold'))
        self.button = ttk.Button(self.frame, style='Bold.TButton')
        self.button.configure(text='开始录制', command=lambda : self.__begin_quit(self.v_name_enter.get(), v_time_enter.get()))
        self.button.grid(row=1, column=2, padx=1)

        # 返回函数发生错误的文本信息
        error_text = Label(self.frame, textvariable=self.error_text, fg='red', font='微软雅黑 -10 bold')
        error_text.grid(row=2, sticky='W')

    def __click_entry(self,event):
        if self.v_name.get() == u'默认以时间命名':
            self.v_name.set('')
            self.v_name_enter.configure(fg='#000000')
        elif self.v_name.get() == '':
            self.v_name_enter.configure(fg='#000000')

    def __begin_quit(self, name, recordtime):
        # 格式化视频名称
        if name == '':
            full_v_name = ''+self.v_suffix_box.get()
            self.v_name.set(u'默认以时间命名')
            self.v_name_enter.configure(fg='#A9A9A9')
        elif name == u'默认以时间命名':
            full_v_name = ''+self.v_suffix_box.get()
        else:
            full_v_name = name+self.v_suffix_box.get()

        print(Record.record_status)
        global threadBegin
        phone_id = TopView.get_current_id()         # 获取选择手机的id

        if Record.record_status == 0:
            self.button.configure(state='disable')          # 设置按钮不可用
            threadBegin = threading.Thread(target=Record.begin_record, kwargs={'phone_id': phone_id, 'videoname': full_v_name, 'TIME': recordtime})
            threadBegin.setDaemon(True)
            threadBegin.start()

            time.sleep(3)               # 为了等错误反馈回来
            self.error_text.set(Record.return_text)

            self.button.configure(state='enable')

            if Record.record_status not in [0,1]:
                Record.set_status(0)
                self.button.configure(text='开始录制')
                return

            self.button.configure(text='结束录制')

        elif Record.record_status == 1:
            self.button.configure(state='disable')          # 设置按钮不可用
            thread = threading.Thread(target=Record.quit_record)
            thread.start()
            thread.join()

            threadBegin.join()          # 等待录制的线程彻底结束

            self.error_text.set(Record.return_text)
            if Record.record_status != 1:
                Record.set_status(0)

            self.button.configure(state='enable')

            self.button.configure(text='开始录制')
        else:
            self.error_text.set(Record.return_text)
            Record.set_status(0)


if __name__ == '__main__':
    mainWindow()