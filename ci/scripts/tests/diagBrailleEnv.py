import sys

try:
    # Importing tests.unit triggers the unit test harness initialization
    import tests.unit  # noqa: F401
    import languageHandler
    import config
    import braille

    lang = languageHandler.getLanguage()
    table = config.conf["braille"].get("translationTable")
    dims = braille.handler.displayDimensions
    disp = getattr(braille.handler, "buffer", None)
    size = getattr(disp, "displaySize", None)
    print(f"[diag] language={lang}")
    print(f"[diag] translationTable={table}")
    print(f"[diag] displayDimensions rows={dims.numRows} cols={dims.numCols}")
    print(f"[diag] buffer.displaySize={size}")
except Exception as e:
    print(f"[diag] error: {e}")
    sys.exit(0)

