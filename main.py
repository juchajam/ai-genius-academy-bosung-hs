import cv2
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

def mouse_callback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        longitude = x * x_diff / w + x_lt
        latitude = y_lt - (y * y_diff / h) 
        print(longitude, latitude)

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

cv2.namedWindow("map")
cv2.setMouseCallback("map", mouse_callback)

while True:
    cv2.imshow("map", map)
    if cv2.waitKey(33) == 27:
        break

cv2.destroyAllWindows()
ser.close()
