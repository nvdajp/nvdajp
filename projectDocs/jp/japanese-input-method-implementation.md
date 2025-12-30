# 日本語入力メソッド（IME/TSF）の実装

## 概要

nvdajp では、日本語入力メソッド（IME）と Text Services Framework (TSF) のサポートにおいて、本家版にはない日本語固有の機能を実装しています。これらの変更は `nvdaHelper/remote/ime.cpp` と `nvdaHelper/remote/tsf.cpp` に含まれています。

## ファイル構成

* **`nvdaHelper/remote/ime.cpp`**: IMM (Input Method Manager) API を使用した日本語 IME サポート
* **`nvdaHelper/remote/tsf.cpp`**: TSF (Text Services Framework) API を使用した日本語入力サポート

## 日本語版固有の変更

### `ime.cpp` の変更

#### 1. IME 開閉状態の追跡 (`lastOpenStatus`)

```cpp
// BEGIN JP PATCH (Japanese IME open status tracking)
static BOOL lastOpenStatus=false;
// END JP PATCH
```

**変更内容**: `lastOpenStatus` の初期値を `false` に設定

**理由**: 日本語 IME の開閉状態を正しく追跡するため。初期値を `false` にすることで、IME が初めて開かれたときに正しく通知されます。

**影響**: `handleOpenStatus()` 関数で、IME の開閉状態が変更されたときに `nvdaControllerInternal_IMEOpenStatusUpdate()` を呼び出して NVDA に通知します。

#### 2. 変換属性（compAttr）の追加 (`getCompositionString`)

```cpp
// BEGIN JP PATCH (Japanese IME composition string with compAttr)
#if 0
// シンプルな実装（本家版）
static WCHAR* getCompositionString(HIMC imc, DWORD index) {
	// ...
}
#else
// 日本語版固有の実装（compAttr を追加）
static WCHAR* getCompositionString(HIMC imc, DWORD index) {
	// 変換文字列を取得
	// タブ文字（L'\t'）で区切って compAttr 文字列を追加
	// 例: L"変換文字列\t222221111000"
	// 0: not converted (未変換)
	// 1: selected (選択中)
	// 2: not selected (未選択)
}
#endif
// END JP PATCH
```

**変更内容**: `#if 0` ブロックを無効化し、`#else` ブロック（compAttr を追加する実装）を有効化

**理由**: 日本語 IME の変換状態（未変換、選択中、未選択など）を NVDA に通知するため。これにより、ユーザーは変換候補の状態を音声や点字で確認できます。

**データ形式**:

	wcscat(jpBuf, L"\t");
	wcscat(jpBuf, jpAttrBuf);

	nvdaControllerInternal_inputCompositionUpdate(jpBuf,selStart,selEnd,0);
} else {


// END JP PATCH
**変更内容**: TSF の変換文字列に表示属性情報を追加して通知

**データ形式**:

* 変換文字列と表示属性文字列をタブ文字（`L'\t'`）で区切る
* 例: `L"変換文字列\t222221111000"`

## マージ時の注意事項

   * `lastOpenStatus` の初期値が `false` になっているか
   * `getCompositionString()` 関数が `#else` ブロック（compAttr 追加版）を使用しているか
2. **`tsf.cpp`**:
   * `getDispAttrFromRangeWithShift()` 関数が存在するか
   * `getDispAttrFromRange()` 関数が存在するか
   * `OnEndEdit()` 関数内で `jpAttrBuf` を使用しているか

nvdajp では、ATOK（日本語入力システム）の UI コメント機能をサポートしています。

* **`source/NVDAObjects/IAccessible/__init__.py`**: ATOK の `findExtraOverlayClasses` を呼び出す処理


#### `ATOKxxUIComment` クラス

```python
class ATOKxxUIComment(IAccessible):

	def _get_name(self):
		return name


	def event_show(self):
		if not (
			config.conf["keyboard"]["nvdajpEnableKeyEvents"]

		):
			return
		api.setNavigatorObject(self)
		speech.cancelSpeech()

		time.sleep(0.2)
		speech.speakMessage(self.name)
		(left, top, width, height) = self.location


		x = left + (width // 2)
		y = top + (height // 2)
		winUser.setCursorPos(x, y)


```


**条件**:

* `nvdajpEnableKeyEvents` が有効
* `announceSelectedCandidate` が有効

**動作**:

* UI コメントが表示されたときにビープ音を鳴らす
* コメントの内容を音声で読み上げる
* マウスカーソルをコメントウィンドウの中央に移動
#### `findExtraOverlayClasses` 関数

	if windowClassName.endswith("UIComment"):
		clsList.append(ATOKxxUIComment)
```
**機能**: ウィンドウクラス名が `"UIComment"` で終わる場合に `ATOKxxUIComment` クラスを適用します。

#### `IAccessible.__init__.py` での呼び出し

```python
elif windowClassName[:5] in ("ATOK2", "ATOK3"):
	from . import atok
	atok.findExtraOverlayClasses(self, clsList)

**機能**: ウィンドウクラス名が `"ATOK2"` または `"ATOK3"` で始まる場合に ATOK のオーバーレイクラスを検索します。
マージ後は、以下の点を確認してください：

1. **`source/NVDAObjects/IAccessible/atok.py`** が存在するか

## 関連ファイル

* `nvdaHelper/remote/ime.h`: IME 関連のヘッダー
* `nvdaHelper/remote/tsf.h`: TSF 関連のヘッダー
* `source/inputComposition.py`: Python 側での入力変換処理
* `source/languageHandler.py`: 言語処理（日本語固有の処理を含む）
* `source/NVDAObjects/IAccessible/atok.py`: ATOK UI コメント対応

## 参考資料

* 日本語版の設定: `source/gui/settingsDialogs.py` の `LanguageSettingsPanel`

## 変更履歴

