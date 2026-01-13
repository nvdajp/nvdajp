from synthDriverHandler import SynthDriver  # type: ignore


class SynthDriver(SynthDriver):  # type: ignore
	@classmethod
	def check(cls) -> bool:
		return False
