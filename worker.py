from mylib.http import HTTPResponse, HTTPRequest, MIME_TYPES
import os
from mylib.read_file import read_file


def worker(socket, handler, document_root):
	socket.listen(3)

	while True:

		conn, addr = socket.accept()
		handler(conn, document_root, addr[0])

