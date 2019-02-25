# в случае если не установлен код и статус ответа, он будет 200 OK


class HTTPResponse:
	def __init__(self):
		self.headers = {}
		self.body = None
		self.status = '200 OK'
		self.http_version = 'HTTP/1.1'

	def set_http_version(self, http_version):
		self.http_version = http_version

	def set_status(self, code, status):
		self.status = '{} {}'.format(code, status)

	def add_header(self, header, value):
		self.headers.update({header: value})

	def add_body(self, body):
		self.body = body

	def to_bytes_string(self):
		result = '{} {}\n'.format(self.http_version, self.status)
		for key, value in self.headers.items():
			result += '{}: {}\n'.format(key, value)

		if self.body:
			if type(self.body) == bytes:
				return result.encode() + b'\n\n' + self.body
			else:
				result += '\n\n' + self.body

		return result.encode()


class HTTPRequest:
	def __init__(self, data):
		self.data = data
		self.error = None
		self.method = None
		self.headers = {}
		self.path = ''
		self.file_type = ''
		self._process()

	def _process(self):
		import re

		pattern = re.compile(r'(GET|HEAD|POST|OPTIONS|PUT|PATCH|DELETE|TRACE|CONNECT) /(.*) HTTP')
		params = re.findall(pattern, self.data)

		if params:
			self.method, self.path = params[0]
			if self.path in ['', '/', ' ']:
				self.path = 'index.html'
			self.file_type = self.path.split('.')[-1]
		else:
			self.error = 'Unknown method'

	def __getitem__(self, key):
		return self.headers.get(key)
