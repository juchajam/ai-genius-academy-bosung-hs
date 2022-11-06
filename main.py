import cv2
import threading
import serial

map = cv2.imread("map-opencv/map.jpeg")
savi = cv2.imread("map-opencv/savi.jpeg")
hsv = cv2.cvtColor(savi, cv2.COLOR_BGR2HSV)

ser = serial.Serial("COM7", baudrate=9600)

h, w = map.shape[:2]

y_lt = 37.61151
x_lt = 126.86943
y_rb = 37.44652
x_rb = 127.17842

x_diff = x_rb - x_lt
y_diff = y_lt - y_rb

def show():
    while True:
        while True:
            try:
                y_input = float(input("위도(37.44652N ~ 37.61151N) : "))
                if 37.44652 <= y_input <= 37.61151:
                    break
                print("37.44652N ~ 37.61151N 사이의 값을 입력하세요!")
            except ValueError:
                print("숫자 값을 입력하세요!")

        while True:
            try:
                x_input = float(input("경도(126.86943E ~ 127.17842E) : "))
                if 126.86943 <= x_input <= 127.17842:
                    break
                print("126.86943E ~ 127.17842E 사이의 값을 입력하세요!")
            except ValueError:
                print("숫자 값을 입력하세요!")

        x = int((x_input - x_lt) * w / x_diff)
        y = int((y_lt - y_input) * h / y_diff)

        print(savi[y][x].tolist())

        cv2.circle(map, (x, y), 25, savi[y][x].tolist(), -1)
        point = hsv[y][x][0]
        print(point)
        if 30 < point <= 60:
            ser.write('1'.encode())
        elif 15 < point <= 30:
            ser.write('2'.encode())
        elif 10 < point <= 15:
            ser.write('3'.encode())
        elif 0 <= point <= 10 or 170 < point <= 180:
            ser.write('4'.encode())
        else:
            ser.write('0'.encode())
        
        
map_thread = threading.Thread(target=show)
map_thread.daemon = True
map_thread.start()

while True:
    cv2.imshow("map", map)
    if cv2.waitKey(33) == 27:
        break

cv2.destroyAllWindows()
ser.close()