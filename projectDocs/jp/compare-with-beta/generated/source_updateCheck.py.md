# Diff for: `source\updateCheck.py`

**Source 2025.3.x jp**: `F:\nvda\gh\beta\source\updateCheck.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\updateCheck.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\updateCheck.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\updateCheck.py"
index c95eda7..0bf9878 100644
--- "a/F:\\nvda\\gh\\beta\\source\\updateCheck.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\updateCheck.py"
@@ -18,7 +18,6 @@
 	Tuple,
 )
 from uuid import uuid4
-from winBindings import crypt32
 
 import garbageHandler
 import globalVars
@@ -72,16 +71,11 @@
 from utils.tempFile import _createEmptyTempFileForDeletingFile
 from dataclasses import dataclass
 
-from utils import _deprecate
-
-__getattr__ = _deprecate.handleDeprecations(
-	_deprecate.MovedSymbol("CERT_USAGE_MATCH", "winBindings.crypt32"),
-	_deprecate.MovedSymbol("CERT_CHAIN_PARA", "winBindings.crypt32"),
-)
-
 
 #: The URL to use for update checks.
-_DEFAULT_CHECK_URL = "https://api.nvaccess.org/nvdaUpdateCheck"
+# BEGIN JP PATCH (Japanese update server URL)
+_DEFAULT_CHECK_URL = "https://www.nvda.jp/updateCheck/"
+# END JP PATCH
 #: The time to wait between checks.
 CHECK_INTERVAL = 86400  # 1 day
 #: The time to wait before retrying a failed check.
@@ -213,10 +207,10 @@ def checkForUpdate(auto: bool = False) -> UpdateInfo | None:
 		"versionType": buildVersion.updateVersionType,
 		"osVersion": winVersionText,
 		# Check if the architecture is the most common: "AMD64"
-		# Available values of PROCESSOR_ARCHITECTURE found in:
+		# Available values of PROCESSOR_ARCHITEW6432 found in:
 		# https://docs.microsoft.com/en-gb/windows/win32/winprog64/wow64-implementation-details
-		"x64": os.environ["PROCESSOR_ARCHITECTURE"] == "AMD64",
-		"osArchitecture": os.environ["PROCESSOR_ARCHITECTURE"],
+		"x64": os.environ.get("PROCESSOR_ARCHITEW6432") == "AMD64",
+		"osArchitecture": os.environ.get("PROCESSOR_ARCHITEW6432"),
 	}
 
 	if auto and allowUsageStats:
@@ -1085,8 +1079,33 @@ def terminate():
 		autoChecker = None
 
 
+# These structs are only complete enough to achieve what we need.
+class CERT_USAGE_MATCH(ctypes.Structure):
+	_fields_ = (
+		("dwType", ctypes.wintypes.DWORD),
+		# CERT_ENHKEY_USAGE struct
+		("cUsageIdentifier", ctypes.wintypes.DWORD),
+		("rgpszUsageIdentifier", ctypes.c_void_p),  # LPSTR *
+	)
+
+
+class CERT_CHAIN_PARA(ctypes.Structure):
+	_fields_ = (
+		("cbSize", ctypes.wintypes.DWORD),
+		("RequestedUsage", CERT_USAGE_MATCH),
+		("RequestedIssuancePolicy", CERT_USAGE_MATCH),
+		("dwUrlRetrievalTimeout", ctypes.wintypes.DWORD),
+		("fCheckRevocationFreshnessTime", ctypes.wintypes.BOOL),
+		("dwRevocationFreshnessTime", ctypes.wintypes.DWORD),
+		("pftCacheResync", ctypes.c_void_p),  # LPFILETIME
+		("pStrongSignPara", ctypes.c_void_p),  # PCCERT_STRONG_SIGN_PARA
+		("dwStrongSignFlags", ctypes.wintypes.DWORD),
+	)
+
+
 def _updateWindowsRootCertificates():
 	log.debug("Updating Windows root certificates")
+	crypt = ctypes.windll.crypt32
 	with requests.get(
 		# We must specify versionType so the server doesn't return a 404 error and
 		# thus cause an exception.
@@ -1099,27 +1118,27 @@ def _updateWindowsRootCertificates():
 		# Get the server certificate.
 		cert = response.raw.connection.sock.getpeercert(True)
 	# Convert to a form usable by Windows.
-	certCont = crypt32.CertCreateCertificateContext(
+	certCont = crypt.CertCreateCertificateContext(
 		0x00000001,  # X509_ASN_ENCODING
 		cert,
 		len(cert),
 	)
 	# Ask Windows to build a certificate chain, thus triggering a root certificate update.
 	chainCont = ctypes.c_void_p()
-	crypt32.CertGetCertificateChain(
+	crypt.CertGetCertificateChain(
 		None,
 		certCont,
 		None,
 		None,
 		ctypes.byref(
-			crypt32.CERT_CHAIN_PARA(
-				cbSize=ctypes.sizeof(crypt32.CERT_CHAIN_PARA),
-				RequestedUsage=crypt32.CERT_USAGE_MATCH(),
+			CERT_CHAIN_PARA(
+				cbSize=ctypes.sizeof(CERT_CHAIN_PARA),
+				RequestedUsage=CERT_USAGE_MATCH(),
 			),
 		),
 		0,
 		None,
 		ctypes.byref(chainCont),
 	)
-	crypt32.CertFreeCertificateChain(chainCont)
-	crypt32.CertFreeCertificateContext(certCont)
+	crypt.CertFreeCertificateChain(chainCont)
+	crypt.CertFreeCertificateContext(certCont)

```