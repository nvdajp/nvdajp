import sys
from typing import Any, Optional

try:
    # Importing tests.unit triggers the unit test harness initialization
    import tests.unit  # noqa: F401
    import languageHandler
    import config
    import braille

    lang = languageHandler.getLanguage()
    conf_any: Any = config.conf  # type: ignore[reportAttributeAccessIssue]
    braille_conf: Any = conf_any["braille"]  # type: ignore[reportIndexIssue]
    table = braille_conf.get("translationTable") if hasattr(braille_conf, "get") else None

    handler: Optional[Any] = getattr(braille, "handler", None)
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
except Exception as e:
    print(f"[diag] error: {e}")
    sys.exit(0)
