import re


def read_cfg(path):
	handle = open(path, "rb")

	result = b''
	while True:
		file_data = handle.read(1024)
		result += file_data

		if not file_data:
			handle.close()
			break

	return result.decode("utf-8")


def parse_cfg(data):
	result = {}

	if not data:
		return result

	pattern = re.compile(r'^([A-Za-z0-9._]*) ([A-Za-z0-9._/]*)', re.MULTILINE)
	params = re.findall(pattern, data)
	if params:
		for pair in params:
			result[pair[0]] = pair[1]
		return result
	else:
		return result


def get_config_params(path):
	data = read_cfg(path)
	return parse_cfg(data)
