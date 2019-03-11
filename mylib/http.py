# в случае если не установлен код и статус ответа, он будет 200 OK
from urllib import parse
import re


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
		result = '{} {}\r\n'.format(self.http_version, self.status)
		for key, value in self.headers.items():
			result += '{}: {}\r\n'.format(key, value)

		if self.body:
			if type(self.body) == bytes:
				return result.encode() + b'\r\n' + self.body
			else:
				result += '\r\n\r\n' + self.body
		else:
			result += '\r\n\r\n'

		return result.encode()

	def set_default(self):
		self.set_status(200, 'OK')
		self.add_header('Connection', 'Closed')
		self.add_header('Server', 'kirServer 0.1')

		from datetime import datetime
		import calendar as c

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
		self.add_header('Date', date_header)
		return self


class HTTPRequest:
	def __init__(self, data):
		self.data = data
		self.error = None
		self.method = None
		self.headers = {}
		self.path = ''
		self.file_type = ''
		self.query_params = ''
		self._process()

	@staticmethod
	def _decode_url_symbol(encoded):
		# print('URLDECODED: {}'.format(re.sub(r'%(0-9A-Fa-f)', self._decode_url_symbol, self.path)))

		return chr(int(encoded, 16))

	def _process(self):
		pattern = re.compile(r'(GET|HEAD|POST|OPTIONS|PUT|PATCH|DELETE|TRACE|CONNECT) /([A-Za-z0-9%][A-Za-z0-9%.\-_/ ]*)(\??.*) HTTP')
		params = re.findall(pattern, self.data)
		if params:
			self.method, self.path, self.query_params = params[0]
			self.path = parse.unquote(self.path)

			if self.path in ['', '/', ' ']:
				self.path = 'index.html'

			if re.findall(r'/\.\.', self.path):
				self.error = 'Root directory escape'

			self.file_type = self.path.split('.')[-1]
		else:
			self.error = 'Unknown method'

	def __getitem__(self, key):
		return self.headers.get(key)


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
