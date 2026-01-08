# Diff for: `ci\scripts\mozillaSyms.py`

**Source**: `F:\nvda\gh\beta\ci\scripts\mozillaSyms.py`  
**Current**: `F:\nvda\gh\alphajp-260109\ci\scripts\mozillaSyms.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\ci\\scripts\\mozillaSyms.py" "b/F:\\nvda\\gh\\alphajp-260109\\ci\\scripts\\mozillaSyms.py"
index 763d254..ec6f391 100644
--- "a/F:\\nvda\\gh\\beta\\ci\\scripts\\mozillaSyms.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\ci\\scripts\\mozillaSyms.py"
@@ -13,10 +13,10 @@
 import requests
 
 SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))
-REPO_ROOT = os.path.dirname(os.path.dirname(SCRIPT_DIR))
-DUMP_SYMS = os.path.join(REPO_ROOT, "dump_syms.exe")
-NVDA_SOURCE = os.path.join(REPO_ROOT, "source")
+DUMP_SYMS = os.path.join(os.path.dirname(SCRIPT_DIR), "miscDeps", "tools", "dump_syms.exe")
+NVDA_SOURCE = os.path.join(os.path.dirname(SCRIPT_DIR), "source")
 NVDA_LIB = os.path.join(NVDA_SOURCE, "lib")
+NVDA_LIB64 = os.path.join(NVDA_SOURCE, "lib64")
 ZIP_FILE = os.path.join(SCRIPT_DIR, "mozillaSyms.zip")
 URL = "https://symbols.mozilla.org/upload/"
 
@@ -28,10 +28,10 @@
 	"nvdaHelperRemote.dll",
 ]
 DLL_FILES = [
-	os.path.join(NVDA_LIB, arch, dll)
+	f
 	for dll in DLL_NAMES
-	# We need symbols for all supported architectures.
-	for arch in ("x86", "x64", "arm64", "arm64ec")
+	# We need both the 32 bit and 64 bit symbols.
+	for f in (os.path.join(NVDA_LIB, dll), os.path.join(NVDA_LIB64, dll))
 ]
 
 

```