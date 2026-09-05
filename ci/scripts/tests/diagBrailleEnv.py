import sys
from collections.abc import Mapping
from typing import Any, cast

try:
	# Importing tests.unit triggers the unit test harness initialization
	import braille
	import config
	import languageHandler

	import tests.unit  # noqa: F401

	lang = languageHandler.getLanguage()
	# Treat config.conf as a mapping for diagnostics; avoid over‑promising concrete types
	conf_map: Mapping[str, Any] = cast(Mapping[str, Any], config.conf)  # type: ignore[reportAttributeAccessIssue]
	braille_conf: Any = conf_map.get("braille")
	table = braille_conf.get("translationTable") if hasattr(braille_conf, "get") else None

	handler: Any | None = getattr(braille, "handler", None)
	dims = getattr(handler, "displayDimensions", None)
	disp = getattr(handler, "buffer", None)
	size = getattr(disp, "displaySize", None)
	print(f"[diag] language={lang}")
	print(f"[diag] translationTable={table}")
	if dims is not None:
		rows = getattr(dims, "numRows", None)
		cols = getattr(dims, "numCols", None)
		print(f"[diag] displayDimensions rows={rows} cols={cols}")
	else:
		print("[diag] displayDimensions=None")
	print(f"[diag] buffer.displaySize={size}")
except Exception as e:  # noqa: BLE001
	print(f"[diag] error: {e}")
	sys.exit(0)
