from mylib.http import HTTPResponse, HTTPRequest
import socket
from datetime import datetime
import calendar as c
import os
import threading


def worker(conn):
	resp = HTTPResponse().set_default()
	while True:
		data = conn.recv(1024)
		if not data:
			break

		req = HTTPRequest(data.decode("utf-8"))

		if req.error == 'Unknown method':
			resp.set_status(400, 'Bad Request')
		elif req.method not in ['GET', 'HEAD']:
			resp.set_status(405, 'Method Not Allowed')
		else:
			try:
				handle = open(os.path.join(DOCUMENT_ROOT, req.path), "rb")

				result = b''
				while True:
					file_data = handle.read(1024)
					result += file_data

					if not file_data:
						handle.close()
						break

				resp.add_body(result)

				if req.file_type in MIME_TYPES.keys():
					resp.add_header('Content-Type', '{}; charset=utf-8'.format(MIME_TYPES[req.file_type]))
				else:
					resp.add_header('Content-Type', '{}; charset=utf-8'.format('text/plain'))

				resp.add_header('Content-Length', len(result))

			except FileNotFoundError:
				resp.set_status(404, 'Not Found')

		conn.send(resp.to_bytes_string())
		break

	conn.close()

	print('connection closed\n\n\n\n\n')


DOCUMENT_ROOT = 'temp/'

MIME_TYPES = {
	'html': 'text/html',
	'css': 'text/css',
	'js': 'application/javascript',
	'jpg': 'image/jpeg',
	'jpeg': 'image/jpeg',
	'png': 'image/png',
	'gif': 'image/gif',
	'swf': 'application/x-shockwave-flash',
	'txt': 'text/plain'
}

sock = socket.socket()
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', 8080))

conn_counter = 0


while True:
	sock.listen(10)

	conn, addr = sock.accept()
	conn_counter += 1
	print('connected {}th client, ip: {}'.format(conn_counter, str(addr)))

	# по идее вот тут суем conn в тред и полетели
	# handler = threading.Thread(target=worker, args=(conn,))
	worker(None)


	resp = HTTPResponse()
	resp.set_status(200, 'OK')
	resp.add_header('Connection', 'Closed')
	resp.add_header('Server', 'kirServer 0.1')

	now = datetime.utcnow()
	date_header = '{}, {} {} {} {:02d}:{:02d}:{:02d} GMT'.format(
		c.day_abbr[now.weekday()],
		now.day,
		c.month_abbr[now.month],
		now.year,
		now.hour,
		now.minute,
		now.second
	)
	resp.add_header('Date', date_header)

	while True:
		data = conn.recv(1024)
		if not data:
			break

		req = HTTPRequest(data.decode("utf-8"))

		if req.error == 'Unknown method':
			resp.set_status(400, 'Bad Request')
		elif req.method not in ['GET', 'HEAD']:
			resp.set_status(405, 'Method Not Allowed')
		else:
			try:
				handle = open(os.path.join(DOCUMENT_ROOT, req.path), "rb")

				result = b''
				while True:
					data = handle.read(1024)
					result += data

					if not data:
						handle.close()
						break

				resp.add_body(result)

				if req.file_type in MIME_TYPES.keys():
					resp.add_header('Content-Type', '{}; charset=utf-8'.format(MIME_TYPES[req.file_type]))
				else:
					resp.add_header('Content-Type', '{}; charset=utf-8'.format('text/plain'))

				resp.add_header('Content-Length', len(result))

			except FileNotFoundError:
				resp.set_status(404, 'Not Found')

		conn.send(resp.to_bytes_string())
		break

	conn.close()

	print('connection closed\n\n\n\n\n')

print('end server')
sock.close()



