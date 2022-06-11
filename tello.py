#參考 https://github.com/dji-sdk/Tello-Python/tree/master/Tello_Video 進行修改
import socket
import threading

class Tello(object):

    def __init__(self, local_ip, local_port, command_timeout=.3,  tello_ip='192.168.10.1', tello_port=8889):
        self.abort_flag = False  #將命令傳送給tello，若0.3秒後沒有回應，就會將此設定為True，不再等待回應
        self.command_timeout = command_timeout
        self.response = None

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  #使用UDP建立連線，連線空拍機(192.168.10.1:8889)
        self.tello_address = (tello_ip, tello_port)
        self.socket.bind((local_ip, local_port))

        self.receive_thread = threading.Thread(target=self._receive_thread)
        self.receive_thread.daemon = True
        self.receive_thread.start()

        self.socket.sendto(b'command', self.tello_address)  #發送command到tello，讓進入tello接收指令


    def __del__(self):
        self.socket.close()

    def _receive_thread(self):
        while True:
            try:
                self.response, _ = self.socket.recvfrom(512)
            except socket.error as exc:
                print(f'Caught exception socket.error : {exc}')

    def send_command(self, command):
        print(f'>>傳送指令: {command}')
        self.abort_flag = False
        timer = threading.Timer(self.command_timeout, self.set_abort_flag) #在command_timeout秒後執行set_abort_flag函式

        self.socket.sendto(command.encode('utf-8'), self.tello_address) #送出命令給tello

        timer.start()  #等待0.3秒後才執行set_abort_flag函式
        while self.response is None:
            if self.abort_flag is True:
                break
        timer.cancel() #停止計時
        
        if self.response is None:
            response = 'none_response'
        else:
            response = self.response.decode('utf-8')
            print(f'<<回應 {response}')
        self.response = None
        return response
    
    def set_abort_flag(self): #threading.Timer在0.3秒後執行此函式
        self.abort_flag = True

    def takeoff(self):
        return self.send_command('takeoff')

    def land(self):
        return self.send_command('land')

    def set_speed(self, speed):
        speed = int(speed) #單位為cm/sec
        return self.send_command(f'speed {speed}')

    def get_response(self):
        response = self.response
        return response

    def get_height(self):
        height = self.send_command('height?')
        height = str(height)
        height = filter(str.isdigit, height)
        try:
            height = int(height)
        except:
            pass
        return height

    def get_battery(self):
        battery = self.send_command('battery?')
        try:
            battery = int(battery)
        except:
            pass
        return battery

    def get_flight_time(self):
        flight_time = self.send_command('time?')
        try:
            flight_time = int(flight_time)
        except:
            pass
        return flight_time

    def get_speed(self):
        speed = self.send_command('speed?')
        try:
            speed = float(speed)
        except:
            pass
        return speed

    def move(self, direction, distance):
        distance = int(distance)  #單位為cm
        return self.send_command(f'{direction} {distance}')

    def move_backward(self, distance):
        return self.move('back', distance)

    def move_down(self, distance):
        return self.move('down', distance)

    def move_forward(self, distance):
        return self.move('forward', distance)

    def move_left(self, distance):
        return self.move('left', distance)

    def move_right(self, distance):
        return self.move('right', distance)

    def move_up(self, distance):
        return self.move('up', distance)

    def rotate_cw(self, degrees):
        return self.send_command(f'cw {degrees}')

    def rotate_ccw(self, degrees):
        return self.send_command(f'ccw {degrees}')

    def flip(self, direction):
        return self.send_command(f'flip {direction}')