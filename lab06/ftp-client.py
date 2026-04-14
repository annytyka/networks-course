import socket
import os


class FTPClient:
    def __init__(self):
        self.control = None
        self.data = None


    def _send(self, cmd):
        self.control.send((cmd + "\r\n").encode())


    def _recv(self):
        return self.control.recv(4096).decode()

    
    def _pasv(self):
        self._send("PASV")
        resp = self._recv()
        print(resp)

        start = resp.find("(")
        end = resp.find(")")
        nums = resp[start + 1:end].split(",")

        ip = ".".join(nums[:4])
        port = int(nums[4]) * 256 + int(nums[5])

        return ip, port


    def connect(self, host, port=21):
        self.control = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.control.connect((host, port))
        print(self.control.recv(1024).decode())


    def login(self, user, password):
        self._send(f"USER {user}")
        print(self._recv())

        self._send(f"PASS {password}")
        print(self._recv())


    def list_files(self):
        ip, port = self._pasv()

        self.data = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.data.connect((ip, port))

        self._send("LIST")
        print(self._recv())

        print(self.data.recv(4096).decode())

        print(self._recv())
        self.data.close()


    def upload(self, local, remote):
        if not os.path.exists(local):
            print("File not found")
            return

        ip, port = self._pasv()

        self.data = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.data.connect((ip, port))

        self._send(f"STOR {remote}")
        print(self._recv())

        with open(local, "rb") as f:
            self.data.sendall(f.read())

        self.data.close()
        print(self._recv())


    def download(self, remote, local):
        ip, port = self._pasv()

        self.data = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.data.connect((ip, port))

        self._send(f"RETR {remote}")
        print(self._recv())

        with open(local, "wb") as f:
            while True:
                data = self.data.recv(4096)
                if not data:
                    break
                f.write(data)

        self.data.close()
        print(self._recv())


if __name__ == "__main__":
    ftp = FTPClient()

    ftp.connect("ftp.dlptest.com", 21)
    ftp.login("dlpuser", "rNrKYTX9g7z3RgJRmxWuGHbeu")

    while True:
        cmd = input("ftp> ").split()

        if cmd[0] == "list":
            ftp.list_files()

        elif cmd[0] == "upload":
            ftp.upload(cmd[1], cmd[2])

        elif cmd[0] == "download":
            ftp.download(cmd[1], cmd[2])

        elif cmd[0] == "exit":
            break