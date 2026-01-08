# Diff for: `source\_remoteClient\server.py`

**Source 2025.3.x jp**: `F:\nvda\gh\beta\source\_remoteClient\server.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\_remoteClient\server.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\_remoteClient\\server.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\_remoteClient\\server.py"
index 3a9b296..aa6fdb0 100644
--- "a/F:\\nvda\\gh\\beta\\source\\_remoteClient\\server.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\_remoteClient\\server.py"
@@ -25,27 +25,25 @@
 """
 
 import os
-import shutil
 import socket
 import ssl
-import tempfile
 import time
 from datetime import datetime, timedelta, timezone
 from pathlib import Path
 from select import select
 from itertools import count
-from typing import Any, Final, cast
+from typing import Any, Final
 
 import cffi  # noqa # required for cryptography
 from cryptography import x509
 from cryptography.hazmat.primitives import hashes, serialization
 from cryptography.hazmat.primitives.asymmetric import rsa
 from cryptography.x509.oid import NameOID
-from NVDAState import WritePaths, shouldWriteToDisk
 from logHandler import log
 
 from . import configuration
 from .protocol import RemoteMessageType
+from .secureDesktop import getProgramDataTempPath
 from .serializer import JSONSerializer
 
 
@@ -58,39 +56,42 @@ class RemoteCertificateManager:
 	:ivar fingerprintPath: Path to the fingerprint file
 	"""
 
-	CERT_DIR: Final[Path] = Path(WritePaths.remoteAccessDir, "localRelay")
-	CERT_PATH: Final[Path] = CERT_DIR / "NvdaRemoteRelay.pem"
-	KEY_PATH: Final[Path] = CERT_DIR / "NvdaRemoteRelay.key"
-	FINGERPRINT_PATH: Final[Path] = CERT_DIR / "NvdaRemoteRelay.fingerprint"
-	CERT_DURATION_DAYS: Final[int] = 365
-	CERT_RENEWAL_THRESHOLD_DAYS: Final[int] = 30
+	CERT_FILE = "NvdaRemoteRelay.pem"
+	KEY_FILE = "NvdaRemoteRelay.key"
+	FINGERPRINT_FILE = "NvdaRemoteRelay.fingerprint"
+	CERT_DURATION_DAYS = 365
+	CERT_RENEWAL_THRESHOLD_DAYS = 30
 
-	def __init__(self):
-		"""Initialize the certificate manager."""
-		self.__cert: bytes | None = None
-		self.__key: bytes | None = None
-		self.__fingerprint: str | None = None
+	def __init__(self, certDir: Path | None = None):
+		"""Initialize the certificate manager.
+
+		:param certDir: Directory to store certificate files, defaults to program data temp path
+		"""
+		self.certDir: Path = certDir or getProgramDataTempPath()
+		self.certPath: Path = self.certDir / self.CERT_FILE
+		self.keyPath: Path = self.certDir / self.KEY_FILE
+		self.fingerprintPath: Path = self.certDir / self.FINGERPRINT_FILE
 
 	def ensureValidCertExists(self) -> None:
 		"""Ensures a valid certificate and key exist, regenerating if needed."""
 		log.info("Checking certificate validity")
+		os.makedirs(self.certDir, exist_ok=True)
+
 		if self._filesExist():
 			try:
 				self._validateCertificate()
 				return
 			except Exception as e:
-				log.debug(f"Certificate validation failed: {e}", exc_info=True)
-		else:
-			log.debug("No certificate exists.")
+				log.warning(f"Certificate validation failed: {e}", exc_info=True)
 
 		self._generateSelfSignedCert()
 
 	def _filesExist(self) -> bool:
-		"""Check if certificate, key and fingerprint files exist."""
-		return self.CERT_PATH.is_file() and self.KEY_PATH.is_file() and self.FINGERPRINT_PATH.is_file()
+		"""Check if both certificate and key files exist."""
+		return self.certPath.is_file() and self.keyPath.is_file()
 
 	def _validateCertificate(self) -> None:
-		"""Validates the existing certificate, key and fingerprint.
+		"""Validates the existing certificate and key.
 
 		:raises ValueError: If the current date/time is outside the certificate's validity period, or if the certificate is approaching expiration.
 		:raises OSError: If the certificate or private key files cannot be opened.
@@ -98,7 +99,7 @@ def _validateCertificate(self) -> None:
 		:raises TypeError: If the private key is encrypted.
 		"""
 		# Load and validate certificate
-		with open(self.CERT_PATH, "rb") as f:
+		with open(self.certPath, "rb") as f:
 			certData = f.read()
 			cert = x509.load_pem_x509_certificate(certData)
 
@@ -113,28 +114,8 @@ def _validateCertificate(self) -> None:
 			raise ValueError("Certificate is approaching expiration")
 
 		# Verify private key can be loaded
-		with open(self.KEY_PATH, "rb") as f:
-			keyData = f.read()
-			privKey = cast(rsa.RSAPrivateKey, serialization.load_pem_private_key(keyData, password=None))
-		pubKey = cast(rsa.RSAPublicKey, cert.public_key())
-
-		# Verify that the private key and certificate match
-		privNumbers = privKey.private_numbers()
-		if pubKey.public_numbers().n != privNumbers.p * privNumbers.q:
-			raise ValueError("Invalid key: n != pq")
-		if privKey.public_key() != pubKey:
-			raise ValueError("The certificate and private keys do not match.")
-
-		with open(self.FINGERPRINT_PATH, "r") as f:
-			fingerprintData = f.read().strip()
-
-		# Check that fingerprints match
-		if cert.fingerprint(hashes.SHA256()).hex() != fingerprintData:
-			raise ValueError("Fingerprints do not match.")
-
-		self.__cert = certData
-		self.__key = keyData
-		self.__fingerprint = fingerprintData
+		with open(self.keyPath, "rb") as f:
+			serialization.load_pem_private_key(f.read(), password=None)
 
 	def _generateSelfSignedCert(self) -> None:
 		"""Generates a self-signed certificate and private key."""
@@ -188,21 +169,23 @@ def _generateSelfSignedCert(self) -> None:
 
 		# Calculate fingerprint
 		fingerprint = cert.fingerprint(hashes.SHA256()).hex()
-		# Calculate private key data
-		keyData = privateKey.private_bytes(
+		# Write private key
+		with open(self.keyPath, "wb") as f:
+			f.write(
+				privateKey.private_bytes(
 					encoding=serialization.Encoding.PEM,
 					format=serialization.PrivateFormat.PKCS8,
 					encryption_algorithm=serialization.NoEncryption(),
+				),
 			)
-		# Calculate certificate data
-		certData = cert.public_bytes(serialization.Encoding.PEM)
 
-		# Store data on self
-		self.__key = keyData
-		self.__cert = certData
-		self.__fingerprint = fingerprint
-		# Attempt to persist
-		self._persistCertificate()
+		# Write certificate
+		with open(self.certPath, "wb") as f:
+			f.write(cert.public_bytes(serialization.Encoding.PEM))
+
+		# Save fingerprint
+		with open(self.fingerprintPath, "w") as f:
+			f.write(fingerprint)
 
 		# Add to trusted certificates in config
 		config = configuration.getRemoteConfig()
@@ -213,60 +196,26 @@ def _generateSelfSignedCert(self) -> None:
 
 		log.info(f"Generated new self-signed certificate for NVDA Remote. Fingerprint: {fingerprint}")
 
-	def _persistCertificate(self) -> None:
-		if self.__key is None or self.__cert is None or self.__fingerprint is None:
-			raise RuntimeError("A certificate must be loaded in order to persist it.")
-		if not shouldWriteToDisk():
-			log.debug("Not persisting certificate, as shouldWriteToDisk returned False.")
-			return
-		try:
-			os.makedirs(self.CERT_DIR, exist_ok=True)
-		except Exception:
-			log.debug("Unable to create {self.CIRT_DIR}. Not persisting certificates.", exc_info=True)
-			return
-		for path in self.KEY_PATH, self.CERT_PATH, self.FINGERPRINT_PATH:
-			if path.is_dir():
-				try:
-					shutil.rmtree(path)
-				except Exception:
-					log.debug("Unable to remove {path}. Not persisting certificates.", exc_info=True)
-					return
-		try:
-			with (
-				open(self.KEY_PATH, "wb") as keyFile,
-				open(self.CERT_PATH, "wb") as certFile,
-				open(self.FINGERPRINT_PATH, "wt") as fingerprintFile,
-			):
-				keyFile.write(self.__key)
-				certFile.write(self.__cert)
-				fingerprintFile.write(self.__fingerprint)
-		except Exception:
-			log.debug("Unable to persist certificate.", exc_info=True)
-
 	def getCurrentFingerprint(self) -> str | None:
 		"""Get the fingerprint of the current certificate."""
-		return self.__fingerprint
+		try:
+			if self.fingerprintPath.is_file():
+				with open(self.fingerprintPath, "r") as f:
+					return f.read().strip()
+		except Exception as e:
+			log.warning(f"Error reading fingerprint: {e}", exc_info=True)
+		return None
 
 	def createSSLContext(self) -> ssl.SSLContext:
 		"""Creates an SSL context using the certificate and key."""
-		if self.__key is None or self.__cert is None:
-			raise RuntimeError("A certificate must be loaded to create an SSL context.")
 		context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
 		# Load our certificate and private key
-		with tempfile.NamedTemporaryFile("w+b", delete=False) as f:
-			f.write(self.__key)
-			if not self.__key.endswith(b"\n"):
-				f.write(b"\n")
-			f.write(self.__cert)
-			# OpenSSL will choke if the file is open, so close it manually
-			# We don't exit the context manager, as that would (potentially) delete the file
-			f.close()
-			context.load_cert_chain(f.name)
+		context.load_cert_chain(
+			certfile=str(self.certPath),
+			keyfile=str(self.keyPath),
+		)
 		# Trust our own CA for server verification
-			context.load_verify_locations(cafile=f.name)
-			# Explicitly delete the file, just to be sure
-			# Exiting the context manager should do this, but it may be left up to the OS to decide when to delete it
-			os.unlink(f.name)
+		context.load_verify_locations(cafile=str(self.certPath))
 		# Require client cert verification
 		context.verify_mode = ssl.CERT_NONE  # Don't require client certificates
 		context.check_hostname = False  # Don't verify hostname since we're using self-signed certs
@@ -300,6 +249,7 @@ def __init__(
 		password: str,
 		bindHost: str = "",
 		bindHost6: str = "[::]:",
+		certDir: Path | None = None,
 	):
 		"""Initialize the relay server.
 
@@ -307,10 +257,11 @@ def __init__(
 		:param password: Channel password for client authentication
 		:param bindHost: IPv4 address to bind to, defaults to all interfaces
 		:param bindHost6: IPv6 address to bind to, defaults to all interfaces
+		:param certDir: Directory to store certificate files, defaults to None
 		"""
 		self.port = port
 		self.password = password
-		self.certManager = RemoteCertificateManager()
+		self.certManager = RemoteCertificateManager(certDir)
 		self.certManager.ensureValidCertExists()
 
 		# Initialize other server components

```