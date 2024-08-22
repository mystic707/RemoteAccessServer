import socket
import threading

# 전역 클라이언트 목록
clients = []

def broadcast(message):
    for client_socket in clients:
        try:
            client_socket.send(message.encode('utf-8'))
        except:
            # 오류가 발생한 클라이언트는 목록에서 제거
            clients.remove(client_socket)

def handle_client(client_socket):
    global clients
    clients.append(client_socket)
    print(f"Client connected: {client_socket}")

    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(f"Received message: {message}")

            # 메시지를 모든 클라이언트에게 브로드캐스트
            broadcast(message)
        except ConnectionResetError:
            break

    print(f"Client disconnected: {client_socket}")
    clients.remove(client_socket)
    client_socket.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('10.10.113.81', 12345))
    server.listen(5)
    print("Server listening on port 12345")

    while True:
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr}")

        # 각 클라이언트 연결을 새로운 스레드에서 처리
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    main()