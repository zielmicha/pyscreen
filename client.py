import socket
import sys
import atexit

CLR = '\x1B[1J\x1B[1;1H'

sock = socket.socket(socket.AF_UNIX)
sock.connect(sys.argv[1])
f = sock.makefile('w+')

sys.stdout.write('\x1B[?1049h')

atexit.register(sys.stdout.write, '\x1B[?1049l')

while True:
    l = f.readline().strip()
    if not l:
        break
    cmd = l.split()[0]
    args = l.split()[1:]
    if cmd == 'clr':
        sys.stdout.write(CLR)
    elif cmd == 'ch':
        sys.stdout.write(args[0].decode('hex'))
    elif cmd == 'newline':
        sys.stdout.write('\n')
    elif cmd == 'flush':
        sys.stdout.flush()
