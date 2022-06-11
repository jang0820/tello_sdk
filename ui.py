##參考 https://github.com/dji-sdk/Tello-Python/tree/master/Tello_Video 進行修改
import tkinter as tki
from tkinter import Toplevel, Scale
import threading
import time

class TelloUI(object):
    def __init__(self, tello):
        self.tello = tello #
        self.thread = None #
        self.distance = 10 #預設移動距離10cm
        self.degree = 20  #預設轉動角度

        self.root = tki.Tk() #建立視窗
        self.panel = None
        self.btn_start = tki.Button(self.root, text='開啟tello控制面板', relief='raised', command=self.openCmdWindow)
        self.btn_start.pack(side='bottom', fill='both', expand=1, padx=10, pady=5)
        self.root.wm_title('tello控制器')
        self.root.wm_protocol('WM_DELETE_WINDOW', self.on_close)

        self.sending_command_thread = threading.Thread(target = self._sendingCommand) #執行_sendingCommand函式
            
    def _sendingCommand(self):
        while True:
            self.tello.send_command('command')        
            time.sleep(5)
   
    def openCmdWindow(self):
        panel = Toplevel(self.root)
        panel.wm_title('tello控制面板')
        text0 = tki.Label(panel,
                          text='首先設定每次移動距離與旋轉角度，\n'
                               '使用兩側拉桿調整想要的距離與角度後，\n'
                               '點選中間的「設定距離」按鈕與「設定角度」按鈕。',
                          font='Helvetica 10 bold'
                          )
        text0.pack(side='top')

        text1 = tki.Label(panel, text='使用鍵盤控制tello空拍機，說明如下。\n'
                          'w - 向上移動\t\tArrow Up - 向前移動\n'
                          's - 向下移動\t\tArrow Down -向後移動\n'
                          'a - 逆時針旋轉\t\tArrow Left - 向左移動\n'
                          'd - 順時針旋轉\t\tArrow Right - 向右移動',
                          justify='left')
        text1.pack(side='top')

        self.btn_flipl = tki.Button(panel, text='電池電量', relief='raised', command=self.telloBat)
        self.btn_flipl.pack(side='bottom', fill='both', expand=1, padx=10, pady=5)

        self.btn_flipl = tki.Button(panel, text='向左翻滾', relief='raised', command=self.telloFlip_l)
        self.btn_flipl.pack(side='bottom', fill='both', expand=1, padx=10, pady=5)

        self.btn_flipr = tki.Button(panel, text='向右翻滾', relief='raised', command=self.telloFlip_r)
        self.btn_flipr.pack(side='bottom', fill='both', expand=1, padx=10, pady=5)

        self.btn_flipf = tki.Button(panel, text='向前翻滾', relief='raised', command=self.telloFlip_f)
        self.btn_flipf.pack(side='bottom', fill='both', expand=1, padx=10, pady=5)

        self.btn_flipb = tki.Button(panel, text='向後翻滾', relief='raised', command=self.telloFlip_b)
        self.btn_flipb.pack(side='bottom', fill='both', expand=1, padx=10, pady=5)

        self.btn_landing = tki.Button(panel, text='降落', relief='raised', command=self.telloLanding)
        self.btn_landing.pack(side='bottom', fill='both', expand=1, padx=10, pady=5)

        self.btn_takeoff = tki.Button(panel, text='起飛', relief='raised', command=self.telloTakeOff)
        self.btn_takeoff.pack(side='bottom', fill='both', expand=1, padx=10, pady=5)

        # binding arrow keys to drone control
        self.tmp_f = tki.Frame(panel, width=100, height=2)
        self.tmp_f.bind('<KeyPress-w>', self.on_keypress_w)
        self.tmp_f.bind('<KeyPress-s>', self.on_keypress_s)
        self.tmp_f.bind('<KeyPress-a>', self.on_keypress_a)
        self.tmp_f.bind('<KeyPress-d>', self.on_keypress_d)
        self.tmp_f.bind('<KeyPress-Up>', self.on_keypress_up)
        self.tmp_f.bind('<KeyPress-Down>', self.on_keypress_down)
        self.tmp_f.bind('<KeyPress-Left>', self.on_keypress_left)
        self.tmp_f.bind('<KeyPress-Right>', self.on_keypress_right)
        self.tmp_f.pack(side='bottom', fill='x', expand=1)
        self.tmp_f.focus_set()

        self.distance_bar = Scale(panel, from_=1, to=100, tickinterval=10, label='距離(cm)')
        self.distance_bar.set(5)
        self.distance_bar.pack(side='left')

        self.btn_distance = tki.Button(panel, text='設定距離', relief='raised', command=self.updateDistancebar,)
        self.btn_distance.pack(side='left', fill='both', expand=1, padx=10, pady=5)

        self.degree_bar = Scale(panel, from_=1, to=360, tickinterval=10, label='角度')
        self.degree_bar.set(10)
        self.degree_bar.pack(side='right')

        self.btn_distance = tki.Button(panel, text='設定角度', relief='raised', command=self.updateDegreebar)
        self.btn_distance.pack(side='right', fill='both', expand=1, padx=10, pady=5)

    def telloTakeOff(self):
        return self.tello.takeoff()                

    def telloLanding(self):
        return self.tello.land()

    def telloBat(self):
        return self.tello.get_battery()

    def telloFlip_l(self):
        return self.tello.flip('l')

    def telloFlip_r(self):
        return self.tello.flip('r')

    def telloFlip_f(self):
        return self.tello.flip('f')

    def telloFlip_b(self):
        return self.tello.flip('b')

    def telloCW(self, degree):
        return self.tello.rotate_cw(degree)

    def telloCCW(self, degree):
        return self.tello.rotate_ccw(degree)

    def telloMoveForward(self, distance):
        return self.tello.move_forward(distance)

    def telloMoveBackward(self, distance):
        return self.tello.move_backward(distance)

    def telloMoveLeft(self, distance):
        return self.tello.move_left(distance)

    def telloMoveRight(self, distance):
        return self.tello.move_right(distance)

    def telloUp(self, dist):
        return self.tello.move_up(dist)

    def telloDown(self, dist):
        return self.tello.move_down(dist)

    def updateDistancebar(self):
        self.distance = int(self.distance_bar.get())
        print(f'reset distance to {self.distance:.1f}')

    def updateDegreebar(self):
        self.degree = self.degree_bar.get()
        print(f'reset degree to {self.degree}')

    def on_keypress_w(self, event):
        print(f'up {self.distance} cm')
        self.telloUp(self.distance)

    def on_keypress_s(self, event):
        print(f'down {self.distance} cm')
        self.telloDown(self.distance)

    def on_keypress_a(self, event):
        print(f'ccw {self.degree} degree')
        self.tello.rotate_ccw(self.degree)

    def on_keypress_d(self, event):
        print(f'cw {self.degree} cm')
        self.tello.rotate_cw(self.degree)

    def on_keypress_up(self, event):
        print(f'forward {self.distance} cm')
        self.telloMoveForward(self.distance)

    def on_keypress_down(self, event):
        print(f'backward {self.distance} cm')
        self.telloMoveBackward(self.distance)

    def on_keypress_left(self, event):
        print(f'left {self.distance} cm')
        self.telloMoveLeft(self.distance)

    def on_keypress_right(self, event):
        print(f'right {self.distance} cm')
        self.telloMoveRight(self.distance)

    def on_close(self):
        del self.tello  #呼叫tello的__del__，關閉socket
        self.root.quit()

