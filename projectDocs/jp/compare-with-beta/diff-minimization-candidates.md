# 差分最小化候補リスト

**生成日時**: 2026-01-09 11:17:52

## 概要

このレポートは、projectDocs/jp/compare-with-beta/generated/ 内のMarkdownファイルを解析して、
JP PATCHマーカーがない差分を特定し、本家版の変更を適用する候補をリストアップしたものです。

### 統計

- **JP PATCHマーカーがない差分**: 6 ファイル
- **JP PATCHマーカーがある差分**: 47 ファイル（保持すべきJP固有の変更）

## 優先順位の説明

1. **優先度1**: 明らかなマージ漏れ（例: screenCurtain統合）
2. **優先度2**: 明らかなマージ漏れ（例: registry.pyのリファクタリング）
3. **優先度3**: コード変更（要確認）
4. **優先度4**: ログメッセージの更新
5. **優先度5**: Copyright更新（低優先度）
6. **優先度6**: その他の変更（要確認）

## 適用候補（優先順位順）

### 🔴 **最優先**: `tests\unit\test_visionEnhancementProviders\test_magnificationAPI.py`

- **優先度**: 1
- **理由**: 明らかなマージ漏れ: screenCurtain統合
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: screenCurtain_merge_missing

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\tests\\unit\\test_visionEnhancementProviders\\test_magnificationAPI.py" "b/F:\\nvda\\gh\\alphajp-260109\\tests\\unit\\test_visionEnhancementProviders\\test_magnificationAPI.py"
index ec86c75..fe46b23 100644
--- "a/F:\\nvda\\gh\\beta\\tests\\unit\\test_visionEnhancementProviders\\test_magnificationAPI.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\tests\\unit\\test_visionEnhancementProviders\\test_magnificationAPI.py"
@@ -7,17 +7,15 @@

 import unittest

-from screenCurtain._screenCurtain import TRANSFORM_BLACK
-from winBindings import magnification
-from winBindings.magnification import MAGCOLOREFFECT
+from visionEnhancementProviders.screenCurtain import Magnification, TRANSFORM_BLACK, MAGCOLOREFFECT


 class _Test_MagnificationAPI(unittest.TestCase):
 	def setUp(self):
-		self.assertTrue(magnification.MagInitialize())
+		self.assertTrue(Magnification.MagInitialize())

 	def tearDown(self):
-		self.assertTrue(magnification.MagUninitialize())
+		self.assertTrue(Magnification.MagUninitialize())


 class Test_ScreenCurtain(_Test_MagnificationAPI):
@@ -34,7 +32,7 @@ def _isIdentityMatrix(self, magTransformMatrix: MAGCOLOREFFECT) -> bool:

 	def setUp(self):
 		super().setUp()
-		resultEffect = magnification.MagGetFullscreenColorEffect()
+		resultEffect = Magnification.MagGetFullscreenColorEffect()
 		if not self._isIdentityMatrix(resultEffect):
 			# If the resultEffect is not the identity matrix, skip the test.
 			# This is because a full screen colour effect is already set external to testing.
@@ -45,9 +43,9 @@ def setUp(self):
 		return

 	def test_setAndConfirmBlackFullscreenColorEffect(self):
-		result = magnification.MagSetFullscreenColorEffect(TRANSFORM_BLACK)
+		result = Magnification.MagSetFullscreenColorEffect(TRANSFORM_BLACK)
 		self.assertTrue(result)
-		resultEffect = magnification.MagGetFullscreenColorEffect()
+		resultEffect = Magnification.MagGetFullscreenColorEffect()
 		for i in range(5):
 			for j in range(5):
 				with self.subTest(i=i, j=j):
@@ -60,9 +58,9 @@ def test_setAndConfirmBlackFullscreenColorEffect(self):

 class Test_Mouse(_Test_MagnificationAPI):
 	def test_MagShowSystemCursor(self):
... (残り 8 行)
```

#### 確認事項

- [ ] 本家版の変更内容を確認
- [ ] JP固有の機能に影響がないか確認
- [ ] ビルド・型チェック・テストを実行
- [ ] 問題なければ本家版の変更を適用

---

### ⚫ **要確認**: `tests\system\libraries\NvdaLib.py`

- **優先度**: 6
- **理由**: その他の変更（要確認）
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: unknown

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\tests\\system\\libraries\\NvdaLib.py" "b/F:\\nvda\\gh\\alphajp-260109\\tests\\system\\libraries\\NvdaLib.py"
index 7bae843..5d2697d 100644
--- "a/F:\\nvda\\gh\\beta\\tests\\system\\libraries\\NvdaLib.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\tests\\system\\libraries\\NvdaLib.py"
@@ -100,12 +100,15 @@ def findInstalledNVDAPath(self) -> _Optional[str]:
 		NVDAFilePath = _pJoin(_expandvars("%PROGRAMFILES%"), "nvda", "nvda.exe")
 		legacyNVDAFilePath = _pJoin(_expandvars("%PROGRAMFILES%"), "NVDA", "nvda.exe")
 		exeErrorMsg = f"Unable to find installed NVDA exe. Paths tried: {NVDAFilePath}, {legacyNVDAFilePath}"
-		try:
-			opSys.file_should_exist(NVDAFilePath)
+		# Check if file exists before using file_should_exist to avoid early failure during import
+		import os
+		if os.path.isfile(NVDAFilePath):
 			return NVDAFilePath
-		except AssertionError:
-			# Older versions of NVDA (<=2020.4) install the exe in NVDA\nvda.exe
-			opSys.file_should_exist(legacyNVDAFilePath, exeErrorMsg)
+		elif os.path.isfile(legacyNVDAFilePath):
+			return legacyNVDAFilePath
+		else:
+			# If neither file exists, raise error with helpful message
+			opSys.file_should_exist(NVDAFilePath, exeErrorMsg)
 			return legacyNVDAFilePath

 	def ensureInstallerPathsExist(self):
```

#### 確認事項

- [ ] 本家版の変更内容を確認
- [ ] JP固有の機能に影響がないか確認
- [ ] ビルド・型チェック・テストを実行
- [ ] 問題なければ本家版の変更を適用

---

### ⚫ **要確認**: `tests\unit\test_braille\test_brailleDisplayDrivers.py`

- **優先度**: 6
- **理由**: その他の変更（要確認）
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: unknown

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\tests\\unit\\test_braille\\test_brailleDisplayDrivers.py" "b/F:\\nvda\\gh\\alphajp-260109\\tests\\unit\\test_braille\\test_brailleDisplayDrivers.py"
index 2e2a9f8..eafe5b1 100644
--- "a/F:\\nvda\\gh\\beta\\tests\\unit\\test_braille\\test_brailleDisplayDrivers.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\tests\\unit\\test_braille\\test_brailleDisplayDrivers.py"
@@ -5,6 +5,8 @@

 """Unit tests for braille display drivers."""

+import sysconfig
+import sys
 from brailleDisplayDrivers import seikantk
 import unittest
 import braille
@@ -178,6 +180,14 @@ def test_identifiers(self):
 					self.assertRegex(gesture, braille.BrailleDisplayGesture.ID_PARTS_REGEX)


+@unittest.skipUnless(
+	sysconfig.get_platform() == "win32",
+	"BRLTTY is only supported on 32-bit Windows",
+)
+@unittest.skipUnless(
+	sys.version_info.major == 3 and sys.version_info.minor == 11,
+	"Skipping brlapi tests unless Python 3.11",
+)
 class TestBRLTTY(unittest.TestCase):
 	"""Tests the integrity of the bundled brlapi module."""
```

#### 確認事項

- [ ] 本家版の変更内容を確認
- [ ] JP固有の機能に影響がないか確認
- [ ] ビルド・型チェック・テストを実行
- [ ] 問題なければ本家版の変更を適用

---

### ⚫ **要確認**: `tests\unit\test_braille\test_routing.py`

- **優先度**: 6
- **理由**: その他の変更（要確認）
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: unknown

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\tests\\unit\\test_braille\\test_routing.py" "b/F:\\nvda\\gh\\alphajp-260109\\tests\\unit\\test_braille\\test_routing.py"
index 32fff42..6f38237 100644
--- "a/F:\\nvda\\gh\\beta\\tests\\unit\\test_braille\\test_routing.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\tests\\unit\\test_braille\\test_routing.py"
@@ -48,6 +48,14 @@ def setUp(self):
 		api.setReviewPosition(caret)
 		braille.handler.handleReviewMove()

+	@unittest.skip(
+		"See projectDocs/jp/test-routing-failures.md for details. "
+		"Investigation revealed that even when ReviewCursorManagerRegion is reverted to upstream's "
+		"empty class implementation, these tests still fail in the nvdajp branch. This suggests "
+		"the issue may not be solely due to nvdajp-specific code, but could involve test "
+		"preconditions, environment differences, or other factors. These tests are temporarily "
+		"skipped pending further investigation."
+	)
 	def test_moveCaret_never_moveReviewAndActivate(self):
 		"""Test that routing action on a cell will move the review cursor when routing changes the position,
 		whereas it should activate the current position when the review cursor is already at that position.
@@ -78,6 +86,14 @@ def test_moveCaret_never_moveReviewAndActivate(self):
 		caret = self.cm.makeTextInfo(textInfos.POSITION_CARET)
 		self.assertEqual(caret, self.caret)

+	@unittest.skip(
+		"See projectDocs/jp/test-routing-failures.md for details. "
+		"Investigation revealed that even when ReviewCursorManagerRegion is reverted to upstream's "
+		"empty class implementation, these tests still fail in the nvdajp branch. This suggests "
+		"the issue may not be solely due to nvdajp-specific code, but could involve test "
+		"preconditions, environment differences, or other factors. These tests are temporarily "
+		"skipped pending further investigation."
+	)
 	def test_moveCaret_never_instantActivate(self):
 		"""Test that routing action on a cell will activate the current position
 		when the review cursor is already at that position.
@@ -97,6 +113,14 @@ def test_moveCaret_never_instantActivate(self):
 		caret = self.cm.makeTextInfo(textInfos.POSITION_CARET)
 		self.assertEqual(caret, self.caret)

+	@unittest.skip(
+		"See projectDocs/jp/test-routing-failures.md for details. "
+		"Investigation revealed that even when ReviewCursorManagerRegion is reverted to upstream's "
+		"empty class implementation, these tests still fail in the nvdajp branch. This suggests "
+		"the issue may not be solely due to nvdajp-specific code, but could involve test "
+		"preconditions, environment differences, or other factors. These tests are temporarily "
+		"skipped pending further investigation."
+	)
 	def test_moveCaret_always_moveReviewAndActivate(self):
 		"""Test that routing action on a cell will move the review cursor when routing changes the position,
 		whereas it should activate the current position when the review cursor is already at that position.
@@ -127,6 +151,14 @@ def test_moveCaret_always_moveReviewAndActivate(self):
... (残り 14 行)
```

#### 確認事項

- [ ] 本家版の変更内容を確認
- [ ] JP固有の機能に影響がないか確認
- [ ] ビルド・型チェック・テストを実行
- [ ] 問題なければ本家版の変更を適用

---

### ⚫ **要確認**: `tests\unit\test_remote\test_remoteClient.py`

- **優先度**: 6
- **理由**: その他の変更（要確認）
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: unknown

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\tests\\unit\\test_remote\\test_remoteClient.py" "b/F:\\nvda\\gh\\alphajp-260109\\tests\\unit\\test_remote\\test_remoteClient.py"
index e5df9c4..ce524b7 100644
--- "a/F:\\nvda\\gh\\beta\\tests\\unit\\test_remote\\test_remoteClient.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\tests\\unit\\test_remote\\test_remoteClient.py"
@@ -9,8 +9,6 @@
 from _remoteClient.connectionInfo import ConnectionInfo, ConnectionMode
 from _remoteClient.protocol import RemoteMessageType
 from gui.message import ReturnCode
-from keyboardHandler import KeyboardInputGesture
-from utils.security import post_sessionLockStateChanged


 # Fake implementations for testing
@@ -21,14 +19,6 @@ def __init__(self):
 	def terminate(self):
 		pass

-	def setClipboardText(self, *a, **k): ...
-	def speak(self, *a, **k): ...
-	def cancelSpeech(self, *a, **k): ...
-	def pauseSpeech(self, *a, **k): ...
-	def beep(self, *a, **k): ...
-	def playWave(self, *a, **k): ...
-	def display(self, *a, **k): ...
-

 class FakeMenu:
 	def __init__(self):
@@ -42,7 +32,6 @@ def Check(self, value):
 			self.checked = value

 	def handleConnected(self, *args, **kwargs): ...
-	def handleConnecting(self, *a, **k): ...


 class FakeTransport:
@@ -242,60 +231,6 @@ def test_disconnect(self):
 			self.client.disconnect()
 		fakeControl.close.assert_called_once()

-	def test_lockWhileSendingKeys(self):
-		# the `onConnectedAsLeader` method is decorated with `alwaysCallAfter`.
-		# This causes issues here, so unwrap it.
-		with patch(
-			"_remoteClient.client.RemoteClient.onConnectedAsLeader",
-			rcClient.RemoteClient.onConnectedAsLeader.__wrapped__,
-		):
-			connInfo = ConnectionInfo(
-				hostname="localhost",
-				mode=ConnectionMode.LEADER,
... (残り 47 行)
```

#### 確認事項

- [ ] 本家版の変更内容を確認
- [ ] JP固有の機能に影響がないか確認
- [ ] ビルド・型チェック・テストを実行
- [ ] 問題なければ本家版の変更を適用

---

### ⚫ **要確認**: `tests\unit\test_winVersion.py`

- **優先度**: 6
- **理由**: その他の変更（要確認）
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: unknown

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\tests\\unit\\test_winVersion.py" "b/F:\\nvda\\gh\\alphajp-260109\\tests\\unit\\test_winVersion.py"
index 4dbe9e9..47e80ce 100644
--- "a/F:\\nvda\\gh\\beta\\tests\\unit\\test_winVersion.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\tests\\unit\\test_winVersion.py"
@@ -89,7 +89,7 @@ def test_winVerUnknownBuildToReleaseName(self):
 	def test_winVerProcessorArchitecture(self):
 		# See if processor architecture matches what Windows says.
 		# Use os.environ to guard against platform.machine() giving odd results.
-		actualArchitecture = os.environ["PROCESSOR_ARCHITECTURE"]
+		actualArchitecture = os.environ.get("PROCESSOR_ARCHITEW6432", os.environ["PROCESSOR_ARCHITECTURE"])
 		self.assertEqual(winVersion.getWinVer().processorArchitecture, actualArchitecture)

 	def test_winVerUnknownWin11BuildToReleaseName(self):
```

#### 確認事項

- [ ] 本家版の変更内容を確認
- [ ] JP固有の機能に影響がないか確認
- [ ] ビルド・型チェック・テストを実行
- [ ] 問題なければ本家版の変更を適用

---

## 注意事項

1. **各変更を小さな単位で適用**: 一度に複数のファイルを変更しない
2. **各変更後に検証**: ビルド・型チェック・単体テストを実行
3. **問題があれば即座にロールバック**: Gitで簡単に戻せるように、各変更を個別のコミットにする
4. **JP PATCHマーカーがある差分は保持**: これらはJP固有の変更なので、本家版の変更を適用しない

## 次のステップ

1. 優先度1-2のファイルから順に確認・適用
2. 各ファイルについて：
   - 本家版のファイルを確認: `F:\nvda\gh\beta\tests\unit\test_winVersion.py`
   - 現在のファイルを確認: `source\tests\unit\test_winVersion.py`
   - 差分を確認: projectDocs/jp/compare-with-beta/generated/source_tests_unit_test_winVersion_py.md
   - 本家版の変更を適用
   - ビルド・型チェック・テストを実行
   - 問題なければコミット

## 参考

- 元の比較結果: `projectDocs/jp/compare-with-beta/summary.md`
- ファイル一覧: `projectDocs/jp/compare-with-beta/file-list.md`
