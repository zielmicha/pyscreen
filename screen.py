import terminal
import threading
import socket
import time
import sys

class Server:
    def __init__(self, sock_path, term):
        self.term = term
        self.sock = socket.socket(socket.AF_UNIX)
        self.sock.bind(sock_path)

    def run(self):
        self.sock.listen(1)
        while True:
            client, addr = self.sock.accept()
            threading.Thread(target=self.handle, args=[client]).start()

    def handle(self, client):
        f = client.makefile('w+')
        while True:
            self.write_term(f)
            f.flush()
            time.sleep(0.1)

    def write_term(self, f):
        f.write('clr\n')
        for line in self.term.screen._data:
            for ch in line:
                f.write('ch %s\n' % ch.ch.encode('utf8').encode('hex'))
            f.write('newline\n')
        f.write('flush\n')

if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.exit('Usage: %s socket command...' % sys.argv[0])
    t = terminal.Terminal()
    serv = Server(sys.argv[1], t)
    threading.Thread(target=serv.run).start()
    t.main(sys.argv[2:])
