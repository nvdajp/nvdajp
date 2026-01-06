# Diff for: `source\gui\addonStoreGui\viewModels\addonList.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\gui\addonStoreGui\viewModels\addonList.py`  
**Current**: `F:\nvda\gh\alphajp\source\gui\addonStoreGui\viewModels\addonList.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\gui\\addonStoreGui\\viewModels\\addonList.py" "b/F:\\nvda\\gh\\alphajp\\source\\gui\\addonStoreGui\\viewModels\\addonList.py"
index 375ddff476..df16cc8b52 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\gui\\addonStoreGui\\viewModels\\addonList.py"
+++ "b/F:\\nvda\\gh\\alphajp\\source\\gui\\addonStoreGui\\viewModels\\addonList.py"
@@ -3,17 +3,21 @@
 # This file is covered by the GNU General Public License.
 # See the file COPYING for more details.
 
+from abc import abstractmethod
 from dataclasses import dataclass
 from enum import Enum
 
 from locale import strxfrm
 from typing import (
+	Any,
 	FrozenSet,
 	Generic,
 	List,
 	Optional,
 	TYPE_CHECKING,
+	Protocol,
 	TypeVar,
+	cast,
 )
 
 from requests.structures import CaseInsensitiveDict
@@ -35,10 +39,12 @@
 
 
 if TYPE_CHECKING:
-	# Remove when https://github.com/python/typing/issues/760 is resolved
-	from _typeshed import SupportsLessThan  # noqa: F401
 	from .store import AddonStoreVM
 
+	class _SupportsLessThan(Protocol):
+		@abstractmethod
+		def __lt__(self, other: Any) -> bool: ...
+
 
 @dataclass
 class _AddonListFieldData:
@@ -307,7 +313,10 @@ def getAddonFieldText(self, index: int, field: AddonListField) -> Optional[str]:
 
 	def _getAddonFieldText(self, listItemVM: AddonListItemVM, field: AddonListField) -> str:
 		assert field in AddonListField
-		if field is AddonListField.currentAddonVersionName:
+		if (
+			field is AddonListField.currentAddonVersionName
+			and listItemVM.model._addonHandlerModel is not None
+		):
 			return listItemVM.model._addonHandlerModel.version
 		if field is AddonListField.availableAddonVersionName:
 			return listItemVM.model.addonVersionName
@@ -405,13 +414,15 @@ def _columnSortChoices(self) -> list[str]:
 			)
 		return columnChoices
 
-	def _getFilteredSortedIds(self) -> List[str]:
-		def _getSortFieldData(listItemVM: AddonListItemVM) -> "SupportsLessThan":
+	def _getFilteredSortedIds(self) -> list[str]:
+		def _getSortFieldData(listItemVM: AddonListItemVM) -> "_SupportsLessThan":
 			if self._sortByModelField == AddonListField.publicationDate:
 				if getattr(listItemVM.model, "submissionTime", None):
+					listItemVM = cast(AddonListItemVM[_AddonStoreModel], listItemVM)
 					return listItemVM.model.submissionTime
 				return 0
 			if self._sortByModelField == AddonListField.installDate:
+				listItemVM = cast(AddonListItemVM[_AddonManifestModel], listItemVM)
 				return listItemVM.model.installDate
 			return strxfrm(self._getAddonFieldText(listItemVM, self._sortByModelField))
 

```