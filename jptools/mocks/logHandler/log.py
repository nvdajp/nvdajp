def debug(s, prefix="DEBUG"):
	try:
		print(f"{prefix} {s}")
	except UnicodeEncodeError:
		try:
			print(f"{prefix} {s.encode('utf-8')}")
		except Exception as e:
			print(f"{prefix} {repr(e)}")


def info(s):
	debug(s, prefix="INFO")
