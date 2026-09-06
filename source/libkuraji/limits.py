# limits.py
# Copyright (C) 2026 Takuya Nishimoto
# License: BSD 3-Clause. See LICENSE.

import functools
import os

DEFAULT_MAX_INPUT_CHARS = 65536


class InputTooLongError(ValueError):
	"""Raised when input text exceeds the configured character limit."""


@functools.cache
def get_max_input_chars() -> int | None:
	"""Return the max input length, or None when unlimited.

	Override with LIBKURAJI_MAX_INPUT_CHARS. A value of 0 disables the limit.

	The value is resolved once and memoized: this runs on every translate
	call (i.e. on every braille rendering), so the environment is read only
	on the first call. Call ``get_max_input_chars.cache_clear()`` to re-read
	the environment (e.g. from tests that mutate it at runtime).
	"""
	raw = os.environ.get("LIBKURAJI_MAX_INPUT_CHARS", "").strip()
	if not raw:
		return DEFAULT_MAX_INPUT_CHARS
	limit = int(raw)
	if limit == 0:
		return None
	if limit < 0:
		raise ValueError("LIBKURAJI_MAX_INPUT_CHARS must be non-negative")
	return limit


def enforce_max_input_length(text: str) -> None:
	"""Reject inputs that exceed the configured character limit."""
	limit = get_max_input_chars()
	if limit is not None and len(text) > limit:
		raise InputTooLongError(f"input length {len(text)} exceeds limit of {limit} characters")
