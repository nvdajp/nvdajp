# 日本語入力メソッド（IME/TSF）の実装

## 概要

nvdajp では、日本語入力メソッド（IME）と Text Services Framework (TSF) のサポートにおいて、本家版にはない日本語固有の機能を実装しています。これらの変更は `nvdaHelper/remote/ime.cpp` と `nvdaHelper/remote/tsf.cpp` に含まれています。

## ファイル構成

- **`nvdaHelper/remote/ime.cpp`**: IMM (Input Method Manager) API を使用した日本語 IME サポート
- **`nvdaHelper/remote/tsf.cpp`**: TSF (Text Services Framework) API を使用した日本語入力サポート

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
- 変換文字列と compAttr 文字列をタブ文字（`L'\t'`）で区切る
- compAttr 文字列は各文字の変換状態を表す数字の文字列（例: `L"222221111000"`）

### `tsf.cpp` の変更

#### 1. TSF 表示属性取得関数の追加

##### `getDispAttrFromRangeWithShift()`

```cpp
// BEGIN JP PATCH (Japanese TSF display attribute support)
bool getDispAttrFromRangeWithShift(
	ITfProperty *pProp,
	ITfCategoryMgr *pCategoryMgr,
	ITfDisplayAttributeMgr *pDispMgr,
	ITfRange *pRange,
	TfEditCookie ec,
	long shiftStart,
	long shiftEnd,
	TF_DISPLAYATTRIBUTE *pDispAttr
)
```

**機能**: TSF の表示属性を、指定された範囲をシフトして取得する

**用途**: 日本語 TSF の変換状態を文字単位で取得するためのヘルパー関数

##### `getDispAttrFromRange()`

```cpp
HRESULT getDispAttrFromRange(ITfContext *pContext,
							 ITfRange *pRange,
							 TfEditCookie ec,
							 wchar_t *jpAttrBuf,
							 long jpAttrLen)
```

**機能**: TSF の表示属性を文字列として取得する

**データ形式**: 
- `jpAttrBuf` に各文字の変換状態を表す数字の文字列を格納
- 例: `L"222221111000"`
- 各数字の意味:
  - `0`: TF_ATTR_INPUT (入力中)
  - `1`: TF_ATTR_TARGET_CONVERTED (変換対象・変換済み)
  - `2`: TF_ATTR_CONVERTED (変換済み)
  - `3`: TF_ATTR_TARGET_NOTCONVERTED (変換対象・未変換)
  - `4`: TF_ATTR_INPUT_ERROR (入力エラー)
  - `5`: TF_ATTR_FIXEDCONVERTED (確定変換済み)

#### 2. `OnEndEdit` での表示属性通知

```cpp
// BEGIN JP PATCH (Japanese TSF display attribute support)
//nvdaControllerInternal_inputCompositionUpdate(buf,selStart,selEnd,0);
constexpr long jpAttrLen = 256;
wchar_t jpAttrBuf[jpAttrLen];
HRESULT hr = getDispAttrFromRange(pCtx, pRange, cookie, jpAttrBuf, jpAttrLen);
if (hr == S_OK) {
	wchar_t jpBuf[513];
	wcscpy(jpBuf, buf);
	wcscat(jpBuf, L"\t");
	wcscat(jpBuf, jpAttrBuf);
	nvdaControllerInternal_inputCompositionUpdate(jpBuf,selStart,selEnd,0);
} else {
	nvdaControllerInternal_inputCompositionUpdate(buf,selStart,selEnd,0);
}
// END JP PATCH
```

**変更内容**: TSF の変換文字列に表示属性情報を追加して通知

**データ形式**: 
- 変換文字列と表示属性文字列をタブ文字（`L'\t'`）で区切る
- 例: `L"変換文字列\t222221111000"`

**フォールバック**: `getDispAttrFromRange()` が失敗した場合は、表示属性なしで通知

## マージ時の注意事項

これらのファイルは、本家版のマージ時に上書きされる可能性があります。マージ後は、以下の点を確認してください：

1. **`ime.cpp`**:
   - `lastOpenStatus` の初期値が `false` になっているか
   - `getCompositionString()` 関数が `#else` ブロック（compAttr 追加版）を使用しているか

2. **`tsf.cpp`**:
   - `getDispAttrFromRangeWithShift()` 関数が存在するか
   - `getDispAttrFromRange()` 関数が存在するか
   - `OnEndEdit()` 関数内で `jpAttrBuf` を使用しているか

## 関連ファイル

- `nvdaHelper/remote/ime.h`: IME 関連のヘッダー
- `nvdaHelper/remote/tsf.h`: TSF 関連のヘッダー
- `source/inputComposition.py`: Python 側での入力変換処理
- `source/languageHandler.py`: 言語処理（日本語固有の処理を含む）

## 参考資料

- Windows IME API: [ImmGetCompositionString function](https://learn.microsoft.com/en-us/windows/win32/api/imm/nf-imm-immgetcompositionstringw)
- Windows TSF API: [Text Services Framework](https://learn.microsoft.com/en-us/windows/win32/tsf/text-services-framework)
- 日本語版の設定: `source/gui/settingsDialogs.py` の `LanguageSettingsPanel`

## 変更履歴

- 2025-12-30: x64 Python 3.13 移行時に、betajp ブランチから日本語版固有の変更を復元

