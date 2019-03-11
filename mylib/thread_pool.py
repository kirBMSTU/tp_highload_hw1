import threading


class ThreadPool:
	def __init__(self, thread_number, target, args):
		self.thread_number = thread_number
		self.target = target
		self.args = args

		self.pool = []

		self._prepare()

	def _prepare(self):
		for i in range(self.thread_number):
			new_thread = threading.Thread(target=self.target, args=self.args)
			self.pool.append(new_thread)

	def start(self):
		for thread in self.pool:
			thread.start()

		for thread in self.pool:
			thread.join()
