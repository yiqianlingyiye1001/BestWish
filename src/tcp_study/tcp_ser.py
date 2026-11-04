import socket

# 创建 TCP socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 绑定本地回环地址和端口
server.bind(('127.0.0.1', 9999))
# 开始监听
server.listen(1)
print("服务端已启动，等待连接...")

# 阻塞等待客户端连接（这里发生第一次和第三次握手）
conn, addr = server.accept()
print(f"已连接到客户端: {addr}")
print(f"{conn}")


# 接收数据
data = conn.recv(1024)
print(f"收到消息: {data.decode()}")

# 关闭连接（这里发生四次挥手）
conn.close()
server.close()
print("服务端关闭")