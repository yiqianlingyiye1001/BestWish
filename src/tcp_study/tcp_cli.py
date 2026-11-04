import socket
import time

# 创建 TCP socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 发起连接（这里发起第一次握手，收到第二次握手，发出第三次握手）
client.connect(('127.0.0.1', 9999))
print("已连接到服务端")

# 发送数据
client.sendall(b"Hello, TCP!")
print("消息已发送")

# 稍微停顿一下，保证挥手包不乱
time.sleep(1)

# 关闭连接（发起四次挥手）
client.close()
print("客户端关闭")