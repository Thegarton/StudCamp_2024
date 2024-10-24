import socket
import time
import cv2
import numpy as np

from test_move import RobotDirection
from ctrl_servo import CTRL_Servo


# Подключение к камере
cap = cv2.VideoCapture(0)
go = RobotDirection()
control_s = CTRL_Servo()

control_s.standart_pose()

MIDDLE_X_IMAGE = 320

class PIDController:
    def __init__(self, Kp, Ki, Kd, setpoint=0):
        self.Kp = Kp  # Пропорциональный коэффициент
        self.Ki = Ki  # Интегральный коэффициент
        self.Kd = Kd  # Дифференциальный коэффициент
        self.setpoint = setpoint  # Желаемая цель (напр., центр кубика)

        self.previous_error = 0  # Ошибка на предыдущем шаге
        self.integral = 0  # Интегральная сумма ошибок
        self.last_time = time.time()  # Время последнего вызова

    def update(self, current_value):
        # Шаг 1: Вычисляем ошибку
        error = current_value - self.setpoint

        # Шаг 2: Вычисляем разницу времени
        current_time = time.time()
        delta_time = current_time - self.last_time
        delta_error = error - self.previous_error

        # Шаг 3: Пропорциональная составляющая
        P = self.Kp * error

        # Шаг 4: Интегральная составляющая
        self.integral += error * delta_time
        I = self.Ki * self.integral

        # Шаг 5: Дифференциальная составляющая
        D = 0
        if delta_time > 0:
            D = self.Kd * (delta_error / delta_time)

        # Шаг 6: Рассчитываем итоговое значение управления
        output = P + I + D

        # Шаг 7: Сохраняем предыдущие значения для следующего шага
        self.previous_error = error
        self.last_time = current_time

        return output
    
    
pid = PIDController(Kp=0.3, Ki=0.0, Kd=0.01, setpoint=320)


def calculate_steering_angle(target_position):
    steering_angle = pid.update(target_position)
    steering_angle = max(-100, min(100, steering_angle))

    return steering_angle


def calculate_speed(current_position, target_position, K1):
    error_a = (target_position[0] - current_position[0])*3.14/4
    error_r = np.linalg.norm(target_position - current_position)

    #print("ERRORS")
    # print("ANGLE:",error_a,"DISTANCE: ",error_r)

    speed = K1 * error_r * np.cos(error_a)
    speed = max(0, min(100, speed))
 
    return speed


current_position = np.array([0.0, 0.0])
position_with_label = np.array([0.0, 0.0])


def find_red_cube(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_red1 = np.array([0, 70, 50])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 70, 50])
    upper_red2 = np.array([180, 255, 255])

    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask = cv2.bitwise_or(mask1, mask2)

    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) > 0:
        largest_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour)
        return (x, y, w, h)
    else:
        return None
    
coordinates_red_cube = 320
    
    
try:
    while coordinates_red_cube != None:
        ret, frame = cap.read()
        if not ret:
            break

        coordinates_red_cube = find_red_cube(frame)

        if coordinates_red_cube != None:
            x, y, h, w = find_red_cube(frame)
            # cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            position_with_label = x
            # print(x + w/2)

        _, buffer = cv2.imencode('.jpg', frame)
        data = buffer.tobytes()

        # print(find_red_cube(frame))

        # if type(position_with_label) == int:
        #     steering_angle = 10
        #     speed = 0
        # else:
        steering_angle = float(calculate_steering_angle(position_with_label))
        speed = 60
            # speed = calculate_speed(current_position, position_with_label, K1)
        # print(steering_angle, speed)
        print()

        go.forward_with_angle(speed, steering_angle)

except KeyboardInterrupt:
    go.stop()

go.stop()
control_s.take_cube()
time.sleep(2)
control_s.drop_object()