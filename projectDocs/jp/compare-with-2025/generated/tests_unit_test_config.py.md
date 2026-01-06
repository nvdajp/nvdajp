# Diff for: `tests\unit\test_config.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\tests\unit\test_config.py`  
**Current**: `F:\nvda\gh\alphajp\tests\unit\test_config.py`

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\tests\\unit\\test_config.py" "b/F:\\nvda\\gh\\alphajp\\tests\\unit\\test_config.py"
index 723ca4d789..2912e5445d 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\tests\\unit\\test_config.py"
+++ "b/F:\\nvda\\gh\\alphajp\\tests\\unit\\test_config.py"
@@ -32,11 +32,12 @@
 	_upgradeConfigFrom_8_to_9_cellBorders,
 	_upgradeConfigFrom_8_to_9_showMessages,
 	_upgradeConfigFrom_8_to_9_tetherTo,
-	upgradeConfigFrom_13_to_14,
 	upgradeConfigFrom_9_to_10,
 	upgradeConfigFrom_11_to_12,
+	upgradeConfigFrom_13_to_14,
 	upgradeConfigFrom_16_to_17,
 	upgradeConfigFrom_17_to_18,
+	upgradeConfigFrom_18_to_19,
 )
 from config.configFlags import (
 	NVDAKey,
@@ -45,6 +46,7 @@
 	ReportCellBorders,
 	TetherTo,
 	OutputMode,
+	ReportSpellingErrors,
 )
 from utils.displayString import (
 	DisplayStringEnum,
@@ -895,7 +897,7 @@ def test_update_FeatureFlag_defaultValue_fromValueOfDefault(self):
 
 
 class Config_AggregatedSection_pollution(unittest.TestCase):
-	"""Ënsure that config profiles don't get polluted with overridden values equal to the base config"""
+	"""Ensure that config profiles don't get polluted with overridden values equal to the base config"""
 
 	def setUp(self):
 		manager = ConfigManager()
@@ -1161,3 +1163,57 @@ def test_dotPadAlreadyExcluded(self):
 		upgradeConfigFrom_17_to_18(profile)
 		expected = ["dotPad", "hidBrailleStandard"]
 		self.assertEqual(profile["braille"]["auto"]["excludedDisplays"], expected)
+
+
+class Config_upgradeProfileSteps_upgradeProfileFrom_18_to_19(unittest.TestCase):
+	def test_DefaultProfile_Unmodified(self):
+		"""reportSpellingErrors unmodified."""
+		configString = "[documentFormatting]"
+		profile = _loadProfile(configString)
+		upgradeConfigFrom_18_to_19(profile)
+		with self.assertRaises(KeyError):
+			profile["documentFormatting"]["reportSpellingErrors"]
+		with self.assertRaises(KeyError):
+			profile["documentFormatting"]["reportSpellingErrors2"]
+
+	def test_defaultProfile_reportSpellingErrors_false(self):
+		"""reportSpellingErrors set to False."""
+		configString = """
+		[documentFormatting]
+		reportSpellingErrors = False
+		"""
+		profile = _loadProfile(configString)
+		upgradeConfigFrom_18_to_19(profile)
+		with self.assertRaises(KeyError):
+			profile["documentFormatting"]["reportSpellingErrors"]
+		self.assertEqual(
+			profile["documentFormatting"]["reportSpellingErrors2"],
+			ReportSpellingErrors.OFF.value,
+		)
+
+	def test_defaultProfile_reportSpellingErrors_true(self):
+		"""reportSpellingErrors set to True."""
+		configString = """
+		[documentFormatting]
+		reportSpellingErrors = True
+		"""
+		profile = _loadProfile(configString)
+		upgradeConfigFrom_18_to_19(profile)
+		with self.assertRaises(KeyError):
+			profile["documentFormatting"]["reportSpellingErrors"]
+		self.assertEqual(
+			profile["documentFormatting"]["reportSpellingErrors2"],
+			ReportSpellingErrors.SPEECH.value,
+		)
+
+	def test_defaultProfile_reportSpellingErrors_invalid(self):
+		"""reportSpellingErrors set to a non-boolean value."""
+		configString = """
+		[documentFormatting]
+		reportSpellingErrors = notABool
+		"""
+		profile = _loadProfile(configString)
+		upgradeConfigFrom_18_to_19(profile)
+		self.assertEqual(profile["documentFormatting"]["reportSpellingErrors"], "notABool")
+		with self.assertRaises(KeyError):
+			profile["documentFormatting"]["reportSpellingErrors2"]

```