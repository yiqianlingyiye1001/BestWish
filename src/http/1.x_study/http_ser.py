import socket

# 简单的 HTTP/1.0 和 1.1 服务端
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(('127.0.0.1', 8080))
    s.listen()
    print("HTTP Server listening on port 8080...")
    while True:
        conn, addr = s.accept()
        with conn:
            # 接收客户端请求
            request = conn.recv(4096)
            print("--- Received Request ---")
            print(request.decode('utf-8'))

            # 构造响应
            body = "Hello, Wireshark!"
            response = (
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: text/plain\r\n"
                f"Content-Length: {len(body)}\r\n"
                "Connection: keep-alive\r\n"  # 测试长连接
                "\r\n"
                f"{body}"
            )
            conn.sendall(response.encode('utf-8'))