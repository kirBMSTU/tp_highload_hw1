from mylib.http import HTTPResponse, HTTPRequest, MIME_TYPES
import os
import time

def worker(conn, id, document_root):
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
				handle = open(os.path.join(document_root, req.path), "rb")

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