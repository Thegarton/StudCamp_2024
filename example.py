import socket
import time

print('Host:')
host = input()
port = 2001


def send_command(command):
    try:
        # Создаем сокет
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(f"Соединение с {host}:{port}")

        # Устанавливаем соединение
        s.connect((host, port))
        print(f"Отправка команды: {command}")

        # Отправляем команду
        s.sendall(command)

        # Добавляем небольшую задержку между отправками команд
        time.sleep(1)

        return True
    except socket.error as e:
        print(f"Ошибка сокета: {e}")
        return False
    finally:
        # Закрываем соединение
        s.close()
        print("Соединение закрыто")


s = input().split()
while len(s)==3:
    command = [69] + [int(i, 16) for i in s] + [69]
    result = send_command(bytes(command))
    print('Команда отправлена: ', result)
    s = input().split()
else:
    print('done!')

#command1 = b'\xff\x40\x00\x05\xff'  # Пример отправки команды
#result = send_command(command1)
#print('Команда на установку цвета отправлена: ', result)

#command1 = b'\xff\x40\x01\x05\xff'  # Пример отправки команды
#result = send_command(command1)
#print('Команда на установку цвета отправлена: ', result)
