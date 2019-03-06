def read_file(full_path):
	import os

	handle = open(full_path, "rb")

	result = b''
	while True:
		file_data = handle.read(1024)
		result += file_data

		if not file_data:
			break

	handle.close()

	return result
