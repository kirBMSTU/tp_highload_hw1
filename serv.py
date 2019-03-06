import socket
import threading
from worker import worker
import os
from mylib.cfg_parser import get_config_params


CONFIG = os.environ['CONFIG']  # '/etc/httpd.conf'
cfg = get_config_params(CONFIG)
if not cfg:
	exit('correct config expected')

DOCUMENT_ROOT = cfg['document_root']
THREAD_LIMIT = cfg['thread_limit']

sock = socket.socket()
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', 8080))

conn_counter = 0

sock.listen(3)

while True:

	conn, addr = sock.accept()
	conn_counter += 1

	# по идее вот тут суем conn в тред и полетели
	handler = threading.Thread(target=worker, args=(conn, conn_counter, DOCUMENT_ROOT, addr[0]))
	handler.start()


print('end server')
sock.close()



