import socket

def send_request(version):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('127.0.0.1', 8080))
        # 构造请求
        request = (
            f"GET / HTTP/{version}\r\n"
            "Host: 127.0.0.1:8080\r\n"
            "User-Agent: PythonSocket\r\n"
            f"Connection: {'keep-alive' if version == '1.1' else 'close'}\r\n"
            "\r\n"
        )
        s.sendall(request.encode('utf-8'))
        # 接收响应
        response = s.recv(4096)
        print(f"--- HTTP/{version} Response ---")
        print(response.decode('utf-8'))

# 测试 HTTP/1.0
send_request("1.0")
# 测试 HTTP/1.1
send_request("1.1")