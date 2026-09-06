# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2021 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

"""This module provides custom asserts for system tests."""

from robot.libraries.BuiltIn import BuiltIn

builtIn: BuiltIn = BuiltIn()


# In Robot libraries, class name must match the name of the module. Use caps for both.
class AssertsLib:
	@staticmethod
	def strings_match(actual, expected, ignore_case=False, comparison="speech", message=""):
		message += "\n" if message else ""
		# Include expected text in robot test report so that the actual behavior
		# can be determined entirely from the report, even when the test passes.
		builtIn.log(
			f"{message}assert {comparison} string matches (ignore case: {ignore_case}):  '{expected}'",
			level="INFO",
		)
		try:
			builtIn.should_be_equal_as_strings(
				actual,
				expected,
				msg=f"{message}{comparison} Actual != Expected",
				ignore_case=ignore_case,
			)
		except AssertionError:
			# Occasionally on assert failure the repr of the string makes it easier to determine the differences.
			builtIn.log(
				f"repr of ({comparison}) actual vs expected (ignore_case={ignore_case}):\n{actual!r}\nvs\n{expected!r}",
				level="DEBUG",
			)
			raise

	@staticmethod
	def string_contains_strings(
		actual: str,
		expectedSubStrings: list[str],
		ignore_case: bool = False,
		comparison: str = "speech",
		message: str = "",
	):
		message += "\n" if message else ""
		# Include expected text in robot test report so that the actual behavior
		# can be determined entirely from the report, even when the test passes.
		builtIn.log(
			f"{message}assert {comparison} string matches (ignore case: {ignore_case}):  '{expectedSubStrings}'",
			level="INFO",
		)
		try:
			for subString in expectedSubStrings:
				builtIn.should_contain(
					actual,
					subString,
					msg=f"{message}{comparison} Actual != Expected",
					ignore_case=ignore_case,
				)
		except AssertionError:
			# Occasionally on assert failure the repr of the string makes it easier to determine the differences.
			builtIn.log(
				f"repr of ({comparison}) actual vs expected (ignore_case={ignore_case}):\n{actual!r}\nvs\n{subString!r}",
				level="DEBUG",
			)
			raise

	@staticmethod
	def strings_match_any(
		actual,
		expectedOptions: list[str],
		ignore_case: bool = False,
		comparison: str = "speech",
		message: str = "",
	):
		"""Assert that actual matches any one of the expectedOptions."""
		message += "\n" if message else ""
		builtIn.log(
			f"{message}assert {comparison} string matches one of (ignore case: {ignore_case}):  {expectedOptions}",
			level="INFO",
		)
		for option in expectedOptions:
			if ignore_case:
				if actual.casefold() == option.casefold():
					return
			else:
				if actual == option:
					return
		# None matched – fail with a message showing all options
		builtIn.log(
			f"repr of ({comparison}) actual vs expected options (ignore_case={ignore_case}):\n{actual!r}\nvs\n{[repr(o) for o in expectedOptions]}",
			level="DEBUG",
		)
		builtIn.fail(
			f"{message}{comparison} Actual != any Expected option.\n"
			f"Actual:\n{actual}\n\nExpected one of:\n" + "\n---\n".join(expectedOptions),
		)

	@staticmethod
	def speech_matches(actual, expected, ignore_case=False, message=""):
		AssertsLib.strings_match(actual, expected, ignore_case, comparison="speech", message=message)

	@staticmethod
	def speech_contains(
		actual: str,
		expectedSpeechParts: list[str],
		ignore_case: bool = False,
		message: str = "",
	):
		AssertsLib.string_contains_strings(
			actual,
			expectedSpeechParts,
			ignore_case,
			comparison="speech",
			message=message,
		)

	@staticmethod
	def braille_matches(actual, expected, ignore_case=False, message=""):
		AssertsLib.strings_match(actual, expected, ignore_case, comparison="braille", message=message)

	@staticmethod
	def braille_contains(
		actual: str,
		expectedBrailleParts: list[str],
		ignore_case: bool = False,
		message: str = "",
	):
		AssertsLib.string_contains_strings(
			actual,
			expectedBrailleParts,
			ignore_case,
			comparison="braille",
			message=message,
		)
