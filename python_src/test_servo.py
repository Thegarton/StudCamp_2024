from xr_i2c import I2c
import time

i2c = I2c()

max_angles = [130, 40, 85, 30] # 1 4 3 2
get_object_angles = [45, 160, 85, 60] # 1 4 3 2
getup_object_angles = [130, 160, 85, 30] #160 ??

buf = [0xff, 0x01, 8, 100, 0xff]
i2c.writedata(i2c.mcu_address, buf)


'''Исходное положение манипулятора (вверх)'''


# for num, angle in enumerate(max_angles):

#     buf = [0xff, 0x01, num+1, angle, 0xff]
#     i2c.writedata(i2c.mcu_address, buf)

#     # if time.time() - time_start == 1000:
#     #     break

#     print(num)

# time.sleep(1)


# '''Взять объект'''

# for num, angle in enumerate(get_object_angles):

#     if num+1 == 2:
#         angle = max_angles[1]

#     buf = [0xff, 0x01, num+1, angle, 0xff]
#     i2c.writedata(i2c.mcu_address, buf)

# time.sleep(1)

# for num, angle in enumerate(get_object_angles):

#     buf = [0xff, 0x01, num+1, angle, 0xff]
#     i2c.writedata(i2c.mcu_address, buf)

# time.sleep(1)

# '''Поднять объект'''

# for num, angle in enumerate(get_object_angles):

#     #if num+1 == 4:
#     #    angle = get_object_angles[3] + 30
#     if num+1 == 1:
#         angle = max_angles[0]

#     buf = [0xff, 0x01, num+1, angle, 0xff]
#     i2c.writedata(i2c.mcu_address, buf)

# time.sleep(0.7)

# for num, angle in enumerate(getup_object_angles):

#     buf = [0xff, 0x01, num+1, angle, 0xff]
#     i2c.writedata(i2c.mcu_address, buf)
