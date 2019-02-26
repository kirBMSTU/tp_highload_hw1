import socket
import threading
from worker import worker
import os


DOCUMENT_ROOT = os.environ['DOCUMENT_ROOT']  # 'temp/'


sock = socket.socket()
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', 8080))

conn_counter = 0

sock.listen(3)

while True:

	conn, addr = sock.accept()
	conn_counter += 1
	print('connected {}th client, ip: {}'.format(conn_counter, str(addr)))

	# по идее вот тут суем conn в тред и полетели
	handler = threading.Thread(target=worker, args=(conn, conn_counter, DOCUMENT_ROOT))
	handler.start()


print('end server')
sock.close()



