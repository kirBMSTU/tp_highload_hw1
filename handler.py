from mylib.http import HTTPResponse, HTTPRequest, MIME_TYPES
import os
from mylib.read_file import read_file


def handler(conn, document_root, ip):
	resp = HTTPResponse().set_default()

	while True:
		data = conn.recv(1024)
		if not data:
			break

		req = HTTPRequest(data.decode("utf-8"))
		# print('{} -- [{}] \"{} {}\"'.format(str(ip), resp.headers['Date'], req.method, req.path))  # access.log

		if req.error == 'Unknown method':
			resp.set_status(400, 'Bad Request')
		elif req.error == 'Root directory escape':
			resp.set_status(403, 'Forbidden')
		elif req.method not in ['GET', 'HEAD']:
			resp.set_status(405, 'Method Not Allowed')
		else:

			full_path = os.path.join(document_root, req.path)
			if not os.path.exists(full_path):
				resp.set_status(404, 'Not Found')
				conn.send(resp.to_bytes_string())
				break

			if os.path.isdir(full_path):
				full_path_index = os.path.join(full_path, 'index.html')
				if os.path.exists(full_path_index):
					full_path = full_path_index
					req.file_type = 'html'
				else:
					resp.set_status(403, 'Forbidden')
					conn.send(resp.to_bytes_string())
					break

			result = read_file(full_path)

			if req.method == 'GET':
				resp.add_body(result)

			if req.file_type in MIME_TYPES.keys():
				resp.add_header('Content-Type', '{}'.format(MIME_TYPES[req.file_type]))
			else:
				resp.add_header('Content-Type', '{}'.format('text/plain'))

			resp.add_header('Content-Length', len(result))

		conn.send(resp.to_bytes_string())
		break

	conn.close()
