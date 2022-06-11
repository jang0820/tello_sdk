#參考 https://github.com/dji-sdk/Tello-Python/tree/master/Tello_Video 進行修改
import tello
from ui import TelloUI


def main():
    drone = tello.Tello('', 8890)
    controller = TelloUI(drone)
    controller.root.mainloop()


if __name__ == '__main__':
    main()
