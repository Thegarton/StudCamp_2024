"""
Исходный код для управления роботом с видео на Raspberry Pi через WiFi
Автор: Sence
Авторские права: XiaoR Technology (Shenzhen XiaoErGeek Technology Co., Ltd. www.xiao-r.com); Форум WiFi Robot Network www.wifi-robots.com
Этот код можно свободно изменять, но запрещено использовать его в коммерческих целях!
Код защищен авторским правом на программное обеспечение, при обнаружении нарушения будет подан иск!
"""
"""
@version: python3.7
@Author  : xiaor
@Explain : Управление двигателем
@contact :
@Time    : 2020/05/09
@File    : xr_motor.py
@Software: PyCharm
"""
from builtins import float, object

import os
import xr_gpio as gpio
import xr_config as cfg

from xr_configparser import HandleConfig
path_data = os.path.dirname(os.path.realpath(__file__)) + '/data.ini'
cfgparser = HandleConfig(path_data)


class RobotDirection(object):
	def __init__(self):
		pass

	def set_speed(self, num, speed):
		"""
		Установить скорость двигателя, num указывает на левую или правую сторону, 1 - левая, 2 - правая, 
		speed указывает на заданное значение скорости (0-100)
		"""
		# print(speed)
		if num == 1:  # Регулировка левой стороны
			gpio.ena_pwm(speed)
		elif num == 2:  # Регулировка правой стороны
			gpio.enb_pwm(speed)

	def motor_init(self):
		"""
		Получить сохранённую скорость робота
		"""
		print("Получение сохранённой скорости робота")
		speed = cfgparser.get_data('motor', 'speed')
		cfg.LEFT_SPEED = speed[0]
		cfg.RIGHT_SPEED = speed[1]
		print(speed[0])
		print(speed[1])

	def save_speed(self):
		"""
		Сохранить текущую скорость двигателя
		"""
		speed = [0, 0]
		speed[0] = cfg.LEFT_SPEED
		speed[1] = cfg.RIGHT_SPEED
		cfgparser.save_data('motor', 'speed', speed)

	def m1m2_forward(self):
		# Установить прямое вращение двигателей M1 и M2
		gpio.digital_write(gpio.IN1, True)
		gpio.digital_write(gpio.IN2, False)

	def m1m2_reverse(self):
		# Установить обратное вращение двигателей M1 и M2
		gpio.digital_write(gpio.IN1, False)
		gpio.digital_write(gpio.IN2, True)

	def m1m2_stop(self):
		# Остановить двигатели M1 и M2
		gpio.digital_write(gpio.IN1, False)
		gpio.digital_write(gpio.IN2, False)

	def m3m4_forward(self):
		# Установить прямое вращение двигателей M3 и M4
		gpio.digital_write(gpio.IN3, True)
		gpio.digital_write(gpio.IN4, False)

	def m3m4_reverse(self):
		# Установить обратное вращение двигателей M3 и M4
		gpio.digital_write(gpio.IN3, False)
		gpio.digital_write(gpio.IN4, True)

	def m3m4_stop(self):
		# Остановить двигатели M3 и M4
		gpio.digital_write(gpio.IN3, False)
		gpio.digital_write(gpio.IN4, False)

	def back(self):
		"""
		Установить направление движения робота на вперед
		"""
		self.set_speed(1, cfg.LEFT_SPEED)
		self.set_speed(2, cfg.RIGHT_SPEED)
		self.m1m2_forward()
		self.m3m4_forward()

	def forward(self):
		"""
		Установить направление движения робота на назад
		"""
		self.set_speed(1, cfg.LEFT_SPEED)
		self.set_speed(2, cfg.RIGHT_SPEED)
		self.m1m2_reverse()
		self.m3m4_reverse()

	def left(self):
		"""
		Установить направление движения робота на поворот налево
		"""
		self.set_speed(1, cfg.LEFT_SPEED)
		self.set_speed(2, cfg.RIGHT_SPEED)
		self.m1m2_reverse()
		self.m3m4_forward()

	def right(self):
		"""
		Установить направление движения робота на поворот направо
		"""
		self.set_speed(1, cfg.LEFT_SPEED)
		self.set_speed(2, cfg.RIGHT_SPEED)
		self.m1m2_forward()
		self.m3m4_reverse()

	def stop(self):
		"""
		Установить направление движения робота на остановку
		"""
		self.set_speed(1, 0)
		self.set_speed(2, 0)
		self.m1m2_stop()
		self.m3m4_stop()

	def forward_with_angle(self, speed, angle):
		"""
		Установить движение вперед с углом
		"""
		angle = angle-100

		angle = min(100, angle)
		angle = max(-100, angle)
		
		speed2 = round(speed*(1-abs(angle)/50))
		
		if angle > 0: 
			self.set_speed(2, speed)  # левая сторона
			self.set_speed(1, abs(speed2))  # правая сторона
			
			self.m3m4_reverse()  # левая сторона? 
			if speed2 > 0: 
				self.m1m2_reverse()  # правая сторона? 
			else: 
				self.m1m2_forward()  # правая сторона? 
		
		else: 
			self.set_speed(2, abs(speed2))  # левая сторона
			self.set_speed(1, speed)  # правая сторона
			
			self.m1m2_reverse()  # правая сторона? 
			if speed2 > 0: 
				self.m3m4_reverse()  # левая сторона? 
			else: 
				self.m3m4_forward()  # левая сторона?
