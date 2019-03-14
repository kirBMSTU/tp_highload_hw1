import socket
import threading
from worker import worker
from handler import handler
import os
from mylib.cfg_parser import get_config_params
from mylib.thread_pool import ThreadPool


CONFIG = os.environ['CONFIG']  # '/etc/httpd.conf'
cfg = get_config_params(CONFIG)
if not cfg:
	exit('correct config expected')

DOCUMENT_ROOT = cfg['document_root']
THREAD_LIMIT = int(cfg['thread_limit'])

sock = socket.socket()
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', 80))

conn_counter = 0

sock.listen(10)

thread_pool = ThreadPool(thread_number=THREAD_LIMIT, target=worker, args=(sock, handler, DOCUMENT_ROOT))
thread_pool.start()

sock.close()



