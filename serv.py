from mylib.http import HTTPResponse, HTTPRequest
import socket
from datetime import datetime
import calendar as c
import os

DOCUMENT_ROOT = 'temp/'

mime_types = {
	'html': 'text/html',
	'css': 'text/css',
	'js': 'application/javascript',
	'jpg': 'image/jpeg',
	'jpeg': 'image/jpeg',
	'png': 'image/png',
	'gif': 'image/gif',
	'swf': 'application/x-shockwave-flash'
}

sock = socket.socket()
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', 8080))

conn_counter = 0

while True:
	sock.listen(1)

	conn, addr = sock.accept()

	conn_counter += 1

	print('connected {}th client, ip: {}'.format(conn_counter, str(addr)))

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

	resp.add_header('Content-Type', 'text/html; charset=utf-8')
	# html = """
	# 	<html>
	# 		<head>
	# 			<title>HighLoad</title>
	# 		</head>
	# 		<body>
	# 			<h1>Мой хттп сервер</h1>
	# 			<hr>
	# 			<h2>Вы {}й клиент</h2>
	# 			<a href="/">Перезагрузить страницу</a>
	# 		</body>
	# 	</html>""".format(conn_counter+1)
	#
	# resp.add_body(html)

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
			print(req.path, req.file_type)
			handle = open(os.path.join(DOCUMENT_ROOT, 'test.txt'), "r")

			result = ''
			while True:
				data = handle.read(1024)
				result += data

				if not data:
					handle.close()
					break

			resp.add_body(result)

		conn.send(resp.to_bytes_string())
		break

	conn.close()

	print('connection closed\n\n\n\n\n')

print('end server')
sock.close()

